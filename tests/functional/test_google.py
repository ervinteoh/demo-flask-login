"""This module defines the functional tests for the routes in
```google.py``` in the ```views``` package.
"""
import pytest
from flask import request, url_for
from pytest_mock import MockerFixture
from requests import Response
from webtest import TestApp

from src.models import User
from tests.factories import UserFactory


def test_authenticate(client: TestApp, mocker: MockerFixture):
    """Google authenticate request."""
    base_url = request.host_url.rstrip("/")
    redirect_uri = base_url + url_for("google.callback")

    func_name = "src.services.google.prepare_request_uri"
    mock_prepare = mocker.patch(func_name, return_value="/something")

    res = client.get(url_for("google.authenticate"))

    mock_prepare.assert_called_once_with(redirect_uri)
    assert 'href="/something"' in res


def test_callback_email_not_verified(client: TestApp, mocker: MockerFixture):
    """Google callback view when account email is not verified."""
    mocker.patch("src.services.google.create_token_request")

    func_name = "src.services.google.get_google_account_info"
    mocker.patch(func_name, return_value=Response())

    return_value = {"email_verified": False}
    mocker.patch.object(Response, "json", return_value=return_value)

    res = client.get(url_for("google.callback", code=4), expect_errors=True)
    assert res.status_int == 400


def test_callback_user_found(client: TestApp, mocker: MockerFixture, user: User):
    """Google callback view when account exist in the database."""
    user.is_active = True
    mocker.patch("src.services.google.create_token_request")

    func_name = "src.services.google.get_google_account_info"
    mocker.patch(func_name, return_value=Response())

    return_value = user.__dict__
    return_value["email_verified"] = True
    mocker.patch.object(Response, "json", return_value=return_value)

    res = client.get(url_for("google.callback", code=4))
    assert user.is_authenticated
    assert 'href="/"' in res


@pytest.mark.usefixtures("db")
def test_callback_user_not_found(client: TestApp, mocker: MockerFixture):
    """Google callback view when account does not exist in the
    database.
    """
    mocker.patch("src.services.google.create_token_request")

    func_name = "src.services.google.get_google_account_info"
    mocker.patch(func_name, return_value=Response())

    user = UserFactory().save()
    user.delete()
    return_value = {
        "sub": user.username,
        "email": user.email,
        "given_name": user.first_name,
        "family_name": user.last_name,
        "email_verified": True,
    }
    mocker.patch.object(Response, "json", return_value=return_value)

    res = client.get(url_for("google.callback", code=4))
    assert User.query.filter_by(email=user.email).first().is_authenticated
    assert 'href="/"' in res
