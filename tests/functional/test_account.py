"""This module defines the functional tests for the routes in
```account.py``` in the ```views``` package.
"""
import pytest
from flask import url_for
from freezegun import freeze_time
from webtest import TestApp

from src.database import db
from src.models.user import ERROR_EMAIL, ERROR_PASSWORD, ERROR_USERNAME, User, UserToken
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
        form.submit().follow()
        assert len(User.query.all()) == initial_count + 1
        # assert "<title>Login - Flask Login</title>" in res


class TestActivate:
    """Account activation route."""

    def test_valid_token(self, client: TestApp, user: User):
        """Activate account with valid token."""
        token = user.get_access_token(UserToken.ACTIVATE_ACCOUNT)
        client.get(url_for("account.activate", token=token)).follow()
        # assert "<title>Login - Flask Login</title>" in res

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
            client.get(url_for("account.activate", token=token)).follow()
            # assert "<title>Login - Flask Login</title>" in res
