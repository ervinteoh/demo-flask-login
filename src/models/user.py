"""This module defines the user model classes which are associated
with a single user account of the application. The classes defined
are directly associated with the :file:`account.py` in the ``views``
package for authentication and registration purposes.
"""
import re
from datetime import datetime, timedelta
from enum import Enum, auto

import sqlalchemy as sa
from flask import render_template
from flask_jwt_extended import create_access_token, decode_token
from flask_login import UserMixin
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from src.database import PrimaryKeyModel
from src.extensions import bcrypt
from src.services.mail import AttachmentIcon, send_mail

#: Username regex matching any string with only letters, numbers
#: fullstops and underscore.
REGEX_USERNAME = r"^[a-zA-Z0-9_.]*$"

#: Email regex for valid email format.
REGEX_EMAIL = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

#: Password regex that matches a string with length between 8 to 30,
#: with at least 1 uppercase, lowercase, number, and special character.
REGEX_PASSWORD = (
    r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$&+,:;=?@#|'<>.^*(){}%!_-]).{8,30})"
)

ERROR_USERNAME = (
    "Username is invalid. Please use only letters, numbers, fullstops and underscore."
)
ERROR_EMAIL = "Email is invalid. An example email would be example@company.com."
ERROR_PASSWORD = (
    "Password is too weak. Must be between 8 to 30 characters long. "
    "Please use at least 1 uppercase, lowercase, number, and special character."
)

#: Maximum amount of login attempts.
MAX_LOGIN_ATTEMPTS = 5

#: The lock duration in minutes.
LOCK_DURATION = 120

#: Mail template icon attachments.
MAIL_TEMPLATE_ICON = {
    "account/welcome": AttachmentIcon("IconEmail", "envelope.png"),
    "account/activated": AttachmentIcon("IconCheck", "circle-check.png"),
    "account/locked": AttachmentIcon("IconLock", "lock.png"),
    "account/password_reset": AttachmentIcon("IconKey", "key.png"),
}


class UserToken(Enum):
    """User access token type. This enum is used adjacent to the
    JWTtoken generation.
    """

    ACTIVATE_ACCOUNT = auto()
    RESET_PASSWORD = auto()


class User(PrimaryKeyModel, UserMixin):
    """User account database model.

    :param username: A unique username.
    :type username: str
    :param email: A unique email.
    :type email: str
    :param password: A strong password.
    :type password: str
    :param first_name: The user first name.
    :type first_name: str
    :param last_name: The user last name.
    :type last_name: str
    """

    __tablename__ = "user"
    _username = sa.Column("username", sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120), unique=True, nullable=False)
    _password = sa.Column("password", sa.LargeBinary(128), default=bytes("", "utf8"))
    first_name = sa.Column(sa.String(30))
    last_name = sa.Column(sa.String(30))

    #: The user account is active.
    is_active = sa.Column(sa.Boolean, default=False, nullable=False)

    #: The amount of failed login attempts.
    login_attempt = sa.Column(sa.Integer, default=0, nullable=False)

    #: The account locked datetime.
    lock_datetime = sa.Column(sa.DateTime(timezone=True))

    def __repr__(self):
        return f"User({self.id!r}, {self.username!r}, {self.email!r})"

    @hybrid_property
    def username(self) -> str:
        """Username accessor.

        :return: The username value.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, value: str):
        """Username mutator.

        :param value: The new value.
        :type value: str
        :raises ValueError: The new value is empty.
        :raises ValueError: The new value is invalid.
        """
        if not value:
            raise ValueError("Username can not be empty.")
        if not re.match(REGEX_USERNAME, value.lower()):
            raise ValueError(ERROR_USERNAME)
        self._username = value.lower()

    @validates("email")
    def validate_email(self, _, data: str):
        """Email mutate validator.

        :param data: The new value.
        :type data: str
        :raises ValueError: The new value is empty.
        :raises ValueError: The new value is invalid.
        :return: The new value.
        :rtype: str
        """

        if not data:
            raise ValueError("Email can not be empty.")
        if not re.match(REGEX_EMAIL, data):
            raise ValueError(ERROR_EMAIL)
        return data

    @hybrid_property
    def password(self) -> str:
        """Password accessor.

        :return: The new value.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, value: str):
        """Password mutator.

        :param value: The new value.
        :type value: str
        :raises ValueError: The new value is empty.
        :raises ValueError: The new value is invalid.
        """
        if not value:
            raise ValueError("Password can not be empty.")
        if not re.match(REGEX_PASSWORD, value):
            raise ValueError(ERROR_PASSWORD)
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value: str) -> bool:
        """Validate password matches.

        :param value: The password to validate.
        :type value: str
        :return: The password matches.
        :rtype: bool
        """
        return bcrypt.check_password_hash(self._password, value)

    def send_mail(self, subject: str, template: str, *args, **kwargs):
        """Send email notification to user.

        :param subject: The subject of the email.
        :type subject: str
        :param template: The name of the template.
        :type template: str
        """
        text = render_template(f"mail/{template}.txt", user=self, *args, **kwargs)
        html = render_template(f"mail/{template}.jinja", user=self, *args, **kwargs)
        send_mail(
            subject,
            sender=("Flask Login", "support@ervinteoh.com"),
            recipients=[self.email],
            text_body=text,
            html_body=html,
            attachments=[MAIL_TEMPLATE_ICON.get(template)],
        )

    def lock(self):
        """Lock the account and sends a notification to the user."""
        self.lock_datetime = datetime.utcnow()
        self.send_mail("Account Locked", "account/locked", lock_duration=LOCK_DURATION)

    def reset_login_attempt(self):
        """Reset the login attempt."""
        self.login_attempt = 0
        self.lock_datetime = None

    def increment_login_attempt(self):
        """Increment the failed login attempt."""
        self.login_attempt += 1
        if self.login_attempt >= MAX_LOGIN_ATTEMPTS:
            self.lock()

    def is_locked(self) -> bool:
        """The account is locked.

        :return: The account is locked.
        :rtype: bool
        """
        if self.lock_datetime is None:
            return False
        elapsed_time = datetime.utcnow() - self.lock_datetime
        time_delta = timedelta(minutes=LOCK_DURATION)
        return elapsed_time.total_seconds() < time_delta.total_seconds()

    def get_access_token(self, token_type: UserToken, expires_in=120) -> str:
        """Get user access token.

        :param token_type: User access token type.
        :type token_type: UserToken
        :param expires_in: The time in minutes until token expires,
            defaults to 120
        :type expires_in: int, optional
        :return: An encoded access token.
        :rtype: str
        """
        return create_access_token(
            str(self.id),
            expires_delta=timedelta(minutes=expires_in),
            additional_claims={"token_type": token_type.name},
        )

    @staticmethod
    def verify_access_token(token_type: UserToken, token: str) -> "User":
        """Retrieve the user object by verifying an access token.

        :param token_type: User access token type.
        :type token_type: UserToken
        :param token: The access token to verify.
        :type token: str
        :raises InvalidTokenError: The token is not the desired token
            type.
        :return: The user instance of the decoded token.
        :rtype: User
        """
        claims = decode_token(token)
        user_id = claims["sub"]
        if claims["token_type"] != token_type.name:
            raise InvalidTokenError
        return User.query.get(user_id)
