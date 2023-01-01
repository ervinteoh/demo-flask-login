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
from flask_login import current_user
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidTokenError

from src.extensions import login_manager
from src.models import User, UserToken
from src.services.form import RegisterForm

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
    """Decorator to redirect pages if current user is authenticated."""

    @wraps(function)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in.", "success")
            return redirect(url_for("public.home"))
        return function(*args, **kwargs)

    return decorated_function


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
    token = user.get_access_token(UserToken.ACTIVATE_ACCOUNT)
    url = request.host_url.rstrip("/") + url_for("account.activate", token=token)
    user.send_mail("Activate your account", "account/activate", url=url)
    flash("An email has been sent to your inbox to activate your account.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/activate/<string:token>")
def activate(token):
    """Email verification."""
    try:
        user = User.verify_access_token(UserToken.ACTIVATE_ACCOUNT, token)
        user.update(is_active=True)
    except ExpiredSignatureError:
        message = "Activation link has expired. Please contact the administrator."
        flash(message, "danger")
        return redirect(url_for("public.home"))
    except (DecodeError, InvalidTokenError):
        abort(404)
    flash("Your account has been successfully activated.", "success")
    return redirect(url_for("public.home"))
