"""This module defines the user flask forms to be rendered in the
frontend through the routes. The forms are utilizing a third party
application called ``WTForms`` which allows for clean field definitions
and custom validators to be handled in the backend.

The forms can be rendered into HTML input within jinja with Flask
form functions. Additionally, the forms are able to validate the
values that are submitted.
"""
from flask_wtf import FlaskForm
from sqlalchemy import or_
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
    ValidationError,
)

from src.models.user import (
    ERROR_EMAIL,
    ERROR_PASSWORD,
    ERROR_USERNAME,
    REGEX_PASSWORD,
    REGEX_USERNAME,
    User,
)


class RegisterForm(FlaskForm):
    """Account registration form."""

    username = StringField(
        "Username",
        validators=[DataRequired(), Regexp(REGEX_USERNAME, message=ERROR_USERNAME)],
    )
    email = EmailField("Email", validators=[DataRequired(), Email(message=ERROR_EMAIL)])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=30),
            Regexp(REGEX_PASSWORD, message=ERROR_PASSWORD),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="The passwords do not match each other"),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username: str):
        """Validates username value on submit. This method
        automatically gets called during a ``validate`` or
        ``validate_on_submit`` call.

        :param username: The username value.
        :type username: str
        :raises ValidationError: The username has been taken.
        """
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("The username is already taken.")

    def validate_email(self, email: str):
        """Validates email value on submit. This method
        automatically gets called during a ``validate`` or
        ``validate_on_submit`` call.

        :param email: The email value.
        :type email: str
        :raises ValidationError: The email has been taken.
        """
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("The email is already taken.")


class LoginForm(FlaskForm):
    """Account login form."""

    username = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, extra_validators=None):
        """Validate the state of the form.

        :param extra_validators: A dict mapping field names to lists of
            extra validator methods to run. Extra validators run after
            validators passed when creating the field. If the form has
            validate_<fieldname>, it is the last extra validator,
            defaults to None
        :type extra_validators: list, optional
        :return: bool
        :rtype: The submitted form is valid.
        """
        if not super().validate(extra_validators):
            return False
        condition = or_(
            User.username == self.username.data.lower(),
            User.email == self.username.data,
        )
        self.user: User = User.query.filter(condition).first()
        if self.user is None:
            return False
        if self.user.lock_datetime and not self.user.is_locked():
            self.user.reset_login_attempt()
        if not self.user.check_password(self.password.data):
            self.user.increment_login_attempt()
            self.user.save()
            return False
        if not self.user.is_active or self.user.is_locked():
            return False
        self.user.update(login_attempt=0)
        return True
