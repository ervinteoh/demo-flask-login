"""This module is mainly for the web pages which are associated with
the user accounts. The pages includes the login, register and activate
accounts.
"""
from functools import wraps

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from src.extensions import login_manager
from src.models import User, UserToken
from src.services.form import (
    ForgotPasswordForm,
    LoginForm,
    RegisterForm,
    ResetPasswordForm,
)

blueprint = Blueprint("account", __name__, url_prefix="/account")


@login_manager.user_loader
def load_user(user_id):
    """User loader callback.

    :param user_id: The user id stored in the current session.
    :type user_id: int
    :return: The user instance of the current session.
    :rtype: User
    """
    return User.get_by_id(user_id)


def logged_in_redirect(function):
    """Redirect on logged in sessions."""

    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return function(*args, **kwargs)
        flash("You are already logged in.", "success")
        return redirect(url_for("public.home"))

    return decorated_function


def verify_token(token, token_type, message) -> User:
    """Verify access token.

    :param token: The JWT access token.
    :type token: str
    :param token_type: The user token type.
    :type token_type: UserToken
    :param message: The error message on expired.
    :type message: str
    :return: The user found on token verification.
    :rtype: User
    """
    try:
        user = User.verify_access_token(token_type, token)
    except ExpiredSignatureError:
        return flash(message, "danger")
    except (DecodeError, InvalidTokenError):
        abort(404)
    return user


@blueprint.route("/register")
@logged_in_redirect
def register():
    """Account registration page."""
    form = RegisterForm()
    if "formdata" in session:
        form = RegisterForm(**session["formdata"])
        form.validate()
        session.pop("formdata")

    return render_template("pages/auth/register.jinja", form=form)


@blueprint.route("/register", methods=["POST"])
@logged_in_redirect
def register_post():
    """Account registration post request."""
    form = RegisterForm()
    if not form.validate_on_submit():
        session["formdata"] = form.data
        return redirect(url_for("account.register"))

    user: User = User.create(
        username=form.username.data,
        email=form.email.data,
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        password=form.password.data,
    )
    send_activation(user.id)
    return redirect(url_for("account.login"))


@blueprint.route("/activate/<string:token>")
def activate(token):
    """Email verification."""
    expired_message = "Activation link has expired."
    success_message = "Your account has been successfully activated."
    user = verify_token(token, UserToken.ACTIVATE_ACCOUNT, expired_message)
    if user is not None:
        user.update(is_active=True)
        subject = "Your email address has been verified."
        url = request.host_url.rstrip("/") + url_for("account.login")
        user.send_mail(subject, "account/activated", url=url)
        flash(success_message, "success")
    return redirect(url_for("account.login"))


@blueprint.route("/login")
@logged_in_redirect
def login():
    """Account login page."""
    form = LoginForm()
    return render_template("pages/auth/login.jinja", form=form)


@blueprint.route("/login", methods=["POST"])
@logged_in_redirect
def login_post():
    """Account login post request."""
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember=True)
        flash("You have successfully logged in.", "success")
        redirect_url = request.args.get("next") or url_for("public.home")
        return redirect(redirect_url)

    message = "Invalid username or password"
    if form.user and not form.user.is_active:
        endpoint = "account.send_activation"
        activation_url = url_for(endpoint, user_id=form.user.id)
        message = "Click here to resend your activation email."
        html_link = f"""<a href="{activation_url}">{message}</a>"""
        message = f"Your account is not activated.<br>{html_link}"
    elif form.user and form.user.is_locked():
        message = """Your account has been locked due to multiple\
        failed login attempts."""
    flash(message, "danger")
    return redirect(url_for("account.login"))


@blueprint.route("/logout", methods=["POST"])
def logout():
    """Account sign out request."""
    if current_user.is_authenticated:
        flash("You have successfully logged out.", "success")
    logout_user()
    return redirect(url_for("account.login"))


@blueprint.route("/activate/send/<int:user_id>")
def send_activation(user_id):
    """Send email activation link."""
    user: User = User.get_by_id(user_id)
    token = user.get_access_token(UserToken.ACTIVATE_ACCOUNT)
    url = request.host_url.rstrip("/") + url_for("account.activate", token=token)
    subject = "Welcome to Flask Login, please verify your email address."
    user.send_mail(subject, "account/welcome", url=url)
    flash("An email has been sent to your inbox to activate your account.", "info")
    return redirect(url_for("account.login"))


@blueprint.route("/forgot-password")
def forgot_password():
    """Forgot password page."""
    form = ForgotPasswordForm()
    if "formdata" in session:
        form = ForgotPasswordForm(**session["formdata"])
        form.validate()
        session.pop("formdata")
    return render_template("pages/auth/forgot_password.jinja", form=form)


@blueprint.route("/forgot-password", methods=["POST"])
def forgot_password_post():
    """Forgot password post request."""
    form = ForgotPasswordForm()
    if not form.validate_on_submit():
        session["formdata"] = form.data
        return redirect(url_for("account.forgot_password"))

    user: User = User.query.filter_by(email=form.email.data).first()
    token = user.get_access_token(UserToken.RESET_PASSWORD)
    url = request.host_url.rstrip("/") + url_for("account.password_reset", token=token)
    subject = "Flask Login Password Reset"
    user.send_mail(subject, "account/password_reset", url=url, token_duration=120)
    flash("We have sent a password reset link to your email.", "info")
    return redirect(url_for("account.forgot_password"))


@blueprint.route("/password-reset/<string:token>")
def password_reset(token):
    """Password reset page."""
    expired_message = "Password reset link has expired."
    user = verify_token(token, UserToken.RESET_PASSWORD, expired_message)
    if user is None:
        return redirect(url_for("account.forgot_password"))
    form = ResetPasswordForm()
    if "formdata" in session:
        form = ResetPasswordForm(**session["formdata"])
        form.validate()
        session.pop("formdata")
    return render_template("pages/auth/password_reset.jinja", form=form)


@blueprint.route("/password-reset/<string:token>", methods=["POST"])
def password_reset_post(token):
    """Password reset post request."""
    expired_message = "Password reset link has expired."
    user = verify_token(token, UserToken.RESET_PASSWORD, expired_message)
    if user is None:
        return redirect(url_for("account.forgot_password"))
    form = ResetPasswordForm()
    if not form.validate_on_submit():
        session["formdata"] = form.data
        return redirect(url_for("account.password_reset", token=token))
    user.update(password=form.password.data)
    flash("You have successfully reset your password. ", "success")
    return redirect(url_for("account.login"))
