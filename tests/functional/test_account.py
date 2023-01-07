"""This module defines the functional tests for the routes in
```account.py``` in the ```views``` package.
"""
import pytest
from flask import url_for
from freezegun import freeze_time
from webtest import TestApp

from src.database import db
from src.models.user import (
    ERROR_EMAIL,
    ERROR_PASSWORD,
    ERROR_USERNAME,
    MAX_LOGIN_ATTEMPTS,
    User,
    UserToken,
)
from tests.factories import UserFactory


class TestRegisterPage:
    """Account registration page."""

    # Constant password for tests.
    password = "Pass123$"

    @pytest.fixture(name="form")
    def fixture_form(self, client: TestApp, user):
        """Form fixture with filled in user values."""
        db.session.delete(user)
        db.session.commit()
        res = client.get(url_for("account.register"))
        form = res.form
        for field in ["username", "first_name", "last_name", "email"]:
            form[field] = getattr(user, field)
        form["password"] = self.password
        form["confirm_password"] = self.password
        return form

    def test_username_invalid(self, form):
        """Register account with an invalid username."""
        form["username"] = "foo*&^"
        res = form.submit().follow()
        assert ERROR_USERNAME in res

    def test_username_taken(self, form):
        """Register account with a username that is already taken."""
        UserFactory(username=form["username"].value)
        res = form.submit().follow()
        assert "The username is already taken." in res

    def test_email_invalid(self, form):
        """Register account with an invalid email."""
        form["email"] = "email123"
        res = form.submit().follow()
        assert ERROR_EMAIL in res

    def test_email_taken(self, form):
        """Register account with an email that is already taken."""
        UserFactory(email=form["email"].value)
        res = form.submit().follow()
        assert "The email is already taken." in res

    def test_password_weak(self, form):
        """Register account with a weak password."""
        form["password"] = "weakpassword"
        res = form.submit().follow()
        assert ERROR_PASSWORD in res

    def test_confirm_password_mismatch(self, form):
        """Register account with mismatching passwords."""
        form["confirm_password"] = "Mismatch123!"
        response = form.submit().follow()
        assert "The passwords do not match each other" in response

    # pylint: disable=R0801
    @pytest.mark.parametrize(
        "field",
        [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ],
    )
    def test_field_empty(self, form, field):
        """Register account with a field left empty."""
        form[field] = ""
        res = form.submit().follow()
        assert "This field is required." in res

    def test_submit_valid_values(self, form):
        """Register account with valid values."""
        initial_count = len(User.query.all())
        res = form.submit().follow()
        assert len(User.query.all()) == initial_count + 1
        assert "<title>Login - Flask Login</title>" in res


class TestActivate:
    """Account activation route."""

    def test_valid_token(self, client: TestApp, user: User):
        """Activate account with valid token."""
        token = user.get_access_token(UserToken.ACTIVATE_ACCOUNT)
        res = client.get(url_for("account.activate", token=token)).follow()
        assert "<title>Login - Flask Login</title>" in res

    def test_invalid_token(self, client: TestApp):
        """Activate account with invalid token."""
        url = url_for("account.activate", token="random")
        res = client.get(url, expect_errors=True)
        assert 404 == res.status_int
        assert "<title>Page Not Found - Flask Login</title>" in res

    def test_expired_token(self, client: TestApp, user: User):
        """Activate account with expired token."""
        with freeze_time("2022-01-01 00:00:00"):
            token = user.get_access_token(UserToken.ACTIVATE_ACCOUNT, 10)
        with freeze_time("2022-01-01 00:11:00"):
            res = client.get(url_for("account.activate", token=token)).follow()
            assert "<title>Login - Flask Login</title>" in res


class TestLoginPage:
    """Account login page."""

    # Constant password for tests.
    password = "Pass123$"

    @pytest.fixture(name="form")
    def fixture_form(self, client: TestApp, user: User):
        """Form fixture with filled in user values."""
        user.update(password=self.password, is_active=True)
        res = client.get(url_for("account.login"))
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = self.password
        return form

    def test_username_not_taken(self, form):
        """Submit form with username that is not taken."""
        form["username"] = "random"
        res = form.submit().follow()
        assert "Invalid username or password" in res

    def test_password_incorrect(self, form):
        """Submit form with incorrect password for a registered
        account.
        """
        form["password"] = "incorrect"
        res = form.submit().follow()
        assert "Invalid username or password" in res

    def test_already_logged_in(self, form, client):
        """Visit page when account had already logged in."""
        res = form.submit().follow()
        res = client.get(url_for("account.login")).follow()
        assert "<title>Home - Flask Login</title>" in res

    def test_username_password_valid(self, form):
        """Submit form with correct username and password."""
        res = form.submit().follow()
        assert "<title>Home - Flask Login</title>" in res

    def test_login_email_valid(self, form, user: User):
        """Submit form with correct email and password."""
        form["username"] = user.email
        res = form.submit().follow()
        assert "<title>Home - Flask Login</title>" in res

    def test_inactive_account(self, form, user: User):
        """Submit form with inactive account username."""
        user.update(is_active=False)
        res = form.submit().follow()
        assert "Your account is not activated." in res

    def test_fail_on_last_attempt(self, form, user: User):
        """Submit form and fail to login on last attempt."""
        user.login_attempt = MAX_LOGIN_ATTEMPTS - 1
        form["password"] = "incorrect"
        res = form.submit().follow()
        message = "Your account has been locked due to multiple failed login attempts."
        assert message in res

    def test_account_locked(self, form, user: User):
        """Submit form for a locked account."""
        user.lock()
        res = form.submit().follow()
        message = "Your account has been locked due to multiple failed login attempts."
        assert message in res


class TestLogout:
    """Account logout."""

    # Constant password for tests.
    password = "Pass123$"

    @pytest.fixture(name="form")
    def fixture_form(self, client: TestApp, user: User):
        """Form fixture with filled in user values."""
        user.update(password=self.password, is_active=True)
        res = client.get(url_for("account.login"))
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = self.password
        return form

    def test_logged_in_account(self, form, client):
        """Logout a currently logged in account."""
        res = form.submit().follow()
        res = client.post(url_for("account.logout")).follow()
        assert "You have successfully logged out." in res
        assert "<title>Login - Flask Login</title>" in res

    def test_not_logged_in(self, client):
        """Logout when not logged in."""
        res = client.post(url_for("account.logout")).follow()
        assert "You have successfully logged out." not in res
        assert "<title>Login - Flask Login</title>" in res


class TestForgotPassword:
    """Forgot password page."""

    @pytest.fixture(name="form")
    def fixture_form(self, client: TestApp, user: User):
        """Form fixture with filled in user values."""
        res = client.get(url_for("account.forgot_password"))
        form = res.forms["forgotPasswordForm"]
        form["email"] = user.email
        return form

    def test_email_not_taken(self, form):
        """Submit form with email that is not taken."""
        form["email"] = "invalid@invalid.com"
        res = form.submit().follow()
        assert "There is no account registered with that email." in res

    def test_email_field_empty(self, form):
        """Submit form with email field left empty."""
        form["email"] = ""
        res = form.submit().follow()
        assert "This field is required." in res

    def test_email_invalid(self, form):
        """Submit form with invalid email."""
        form["email"] = "this_is_not_an_email"
        res = form.submit().follow()
        assert ERROR_EMAIL in res

    def test_email_valid(self, form):
        """Submit form with valid email."""
        res = form.submit().follow()
        assert "<title>Forgot Password - Flask Login</title>" in res
        assert "We have sent a password reset link to your email." in res


class TestPasswordReset:
    """Password reset page."""

    # Constant password for tests.
    password = "Pass123$"

    @pytest.fixture
    def form(self, client, user):
        """Form fixture."""
        token = user.get_access_token(UserToken.RESET_PASSWORD)
        res = client.get(url_for("account.password_reset", token=token))
        form = res.forms["passwordResetForm"]
        form["password"] = self.password
        form["confirm_password"] = self.password
        return form

    def test_password_weak(self, form):
        """Submit form with a weak password."""
        form["password"] = "weakpassword"
        form["confirm_password"] = "weakpassword"
        res = form.submit().follow()
        assert ERROR_PASSWORD in res

    def test_confirm_password_mismatch(self, form):
        """Submit form with mismatching passwords."""
        form["confirm_password"] = "Mismatch123!"
        res = form.submit().follow()
        assert "The passwords do not match each other" in res

    def test_password_valid(self, form):
        """Submit form with valid values."""
        res = form.submit().follow()
        assert User.query.one().check_password(self.password)
        assert "<title>Login - Flask Login</title>" in res
        assert "You have successfully reset your password." in res
