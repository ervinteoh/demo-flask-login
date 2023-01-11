"""This module defines unit test cases for the database utilities
defined in ``models`` package in :file:`user.py` module.
"""
from datetime import datetime, timedelta

import pytest
from flask_jwt_extended import create_access_token, decode_token
from freezegun import freeze_time
from jwt.exceptions import InvalidTokenError
from pytest_mock import MockerFixture as Mocker

from src.models.user import LOCK_DURATION, MAX_LOGIN_ATTEMPTS, User, UserToken


@pytest.mark.usefixtures("db")
class TestUserModel:
    """Test :class:`User` abstract class."""

    def test_username_null(self, user: User):
        """Username is null."""
        with pytest.raises(ValueError):
            user.username = None

    @pytest.mark.parametrize("character", list("$&+,:;=?@#|'<>^*()%!-"))
    def test_username_invalid_special_character(self, user: User, character):
        """Username contains invalid character."""
        with pytest.raises(ValueError):
            user.username = user.username + character

    def test_email_null(self, user: User):
        """Email is null."""
        with pytest.raises(ValueError):
            user.email = None

    @pytest.mark.parametrize("email", ["foo", "foo@", "foo@bar", "foo@bar."])
    def test_email_invalid_format(self, user: User, email):
        """Email invalid format."""
        with pytest.raises(ValueError):
            user.email = email

    def test_password_null(self, user: User):
        """Password is null."""
        with pytest.raises(ValueError):
            user.password = None

    @pytest.mark.parametrize("password", ["P123$", "pass123$", "password$", "pass1234"])
    def test_password_weak(self, user: User, password):
        """Password with weak combination."""
        with pytest.raises(ValueError):
            user.password = password

    def test_check_password_success_match(self, user: User):
        """Check password match."""
        user.password = "Pass123$"
        assert user.check_password("Pass123$")

    def test_check_password_fail_mismatch(self, user: User):
        """Check password mismatch."""
        user.password = "Pass123$"
        assert not user.check_password("123Pass$")

    @freeze_time("2022-01-01")
    def test_lock(self, mocker: Mocker, user: User):
        """Lock user account."""
        mocker.patch.object(User, "send_mail")
        user.lock()
        assert user.lock_datetime == datetime.utcnow()
        user.send_mail.assert_called_once()

    def test_reset_login_attempt(self, user: User):
        """Reset login attempt."""
        user.reset_login_attempt()
        assert user.login_attempt == 0
        assert user.lock_datetime is None

    def test_increment_login_attempt_first(self, user: User):
        """Increment login on first attempt."""
        user.increment_login_attempt()
        assert user.login_attempt == 1
        assert user.lock_datetime is None

    def test_increment_login_attempt_last(self, mocker: Mocker, user: User):
        """Increment login on last attempt."""
        user.login_attempt = MAX_LOGIN_ATTEMPTS - 1
        mocker.patch.object(User, "lock")
        user.increment_login_attempt()
        assert user.login_attempt == 5
        user.lock.assert_called_once()

    def test_is_locked(self, user: User):
        """User account not locked."""
        assert not user.is_locked()

    @freeze_time("2022-01-01")
    def test_is_locked_expired(self, user: User):
        """Lock period after lock duration."""
        time_delta = timedelta(minutes=LOCK_DURATION) + timedelta(seconds=1)
        expired_time = datetime.utcnow() - time_delta
        user.lock_datetime = expired_time
        assert not user.is_locked()

    @freeze_time("2022-01-01")
    def test_is_locked_within_duration(self, user: User):
        """Lock period before lock duration."""
        expired_time = datetime.utcnow() - timedelta(minutes=LOCK_DURATION)
        user.lock_datetime = expired_time
        assert not user.is_locked()

    @pytest.mark.parametrize("token_type", ["ACTIVATE_ACCOUNT", "RESET_PASSWORD"])
    def test_get_access_token(self, user: User, token_type):
        """Get access token."""
        token = user.get_access_token(getattr(UserToken, token_type), 10)
        assert decode_token(token)["sub"] == str(user.id)
        assert decode_token(token)["token_type"] == token_type

    @pytest.mark.parametrize("token_type", ["ACTIVATE_ACCOUNT", "RESET_PASSWORD"])
    def test_verify_valid_access_token_type(self, user: User, token_type):
        """Verify access token with valid token type."""
        token = create_access_token(
            str(user.id),
            expires_delta=timedelta(minutes=10),
            additional_claims={"token_type": token_type},
        )
        token_type = getattr(UserToken, token_type)
        assert User.verify_access_token(token_type, token) == user

    def test_verify_incorrect_access_token_type(self, user: User):
        """Verify access token with incorrect token type."""
        token = create_access_token(
            str(user.id),
            expires_delta=timedelta(minutes=10),
            additional_claims={"token_type": "RANDOM"},
        )
        with pytest.raises(InvalidTokenError):
            User.verify_access_token(UserToken.ACTIVATE_ACCOUNT, token)
