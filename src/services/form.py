"""This module defines the user flask forms to be rendered in the
frontend through the routes. The forms are utilizing a third party
application called ``WTForms`` which allows for clean field definitions
and custom validators to be handled in the backend.

The forms can be rendered into HTML input within jinja with Flask
form functions. Additionally, the forms are able to validate the
values that are submitted.
"""
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
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
