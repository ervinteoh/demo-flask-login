"""This module defines unit test cases for the wtforms defined in
``services`` package in :file:`form.py` module.
"""
import pytest

from src.database import db
from src.models.user import ERROR_EMAIL, ERROR_PASSWORD, ERROR_USERNAME, User
from src.services.form import RegisterForm
from tests.factories import UserFactory


@pytest.mark.usefixtures("db")
class TestRegisterForm:
    """Account registration form."""

    @pytest.fixture(name="form")
    def fixture_form(self, user: User):
        """Form fixture with filled in user values."""
        db.session.delete(user)
        db.session.commit()
        values = user.__dict__
        values["username"] = user.username
        values["password"] = "Pass123$"
        values["confirm_password"] = "Pass123$"
        return RegisterForm(**values)

    @pytest.mark.parametrize("character", list("$&+,:;=?@#|'<>^*()%!-"))
    def test_username_invalid_special_character(self, form: RegisterForm, character):
        """Submit form with invalid special character."""
        form.username.data = form.username.data + character
        assert form.validate() is False
        assert ERROR_USERNAME in form.username.errors

    def test_username_taken(self, form: RegisterForm):
        """Submit form with taken username."""
        UserFactory(username=form.username.data)
        assert form.validate() is False
        assert "The username is already taken." in form.username.errors

    @pytest.mark.parametrize("email", ["foo", "foo@", "foo@bar", "foo@bar."])
    def test_email_invalid_format(self, form: RegisterForm, email):
        """Submit form with invalid email."""
        form.email.data = email
        assert form.validate() is False
        assert ERROR_EMAIL in form.email.errors

    def test_email_taken(self, form: RegisterForm):
        """Submit form with taken email."""
        UserFactory(email=form.email.data)
        assert form.validate() is False
        assert "The email is already taken." in form.email.errors

    @pytest.mark.parametrize("password", ["P123$", "pass123$", "password$", "pass1234"])
    def test_password_weak_combination(self, form: RegisterForm, password):
        """Submit form with weak password."""
        form.password.data = password
        form.confirm_password.data = password
        assert form.validate() is False
        assert ERROR_PASSWORD in form.password.errors

    def test_password_too_long(self, form: RegisterForm):
        """Submit form with password exceeding maximum characters."""
        password = form.password.data * 31
        form.password.data = password
        form.confirm_password.data = password
        assert form.validate() is False
        assert "Field must be between 8 and 30 characters long." in form.password.errors

    def test_password_too_short(self, form: RegisterForm):
        """Submit form with password is below the required minimum
        character.
        """
        password = "Pa1$"
        form.password.data = password
        form.confirm_password.data = password
        assert form.validate() is False
        assert "Field must be between 8 and 30 characters long." in form.password.errors

    def test_confirm_password_on_mismatch(self, form: RegisterForm):
        """Submit form with mismatching password between the fields
        Password and Confirm Password.
        """
        form.confirm_password.data = "Random123!"
        assert form.validate() is False
        assert "The passwords do not match each other" in form.confirm_password.errors

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
    def test_field_required_empty(self, form: RegisterForm, field):
        """Submit form with an empty field."""
        getattr(form, field).data = None
        assert form.validate() is False
        assert "This field is required." in getattr(form, field).errors

    def test_submit_valid_values(self, form: RegisterForm):
        """Submit form with all valid values."""
        assert form.validate()
