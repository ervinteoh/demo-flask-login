"""This module defines unit test cases for the google utilities defined
defined in ``services`` package in :file:`google.py` module.
"""
from oauthlib.oauth2 import WebApplicationClient
from pytest_mock import MockerFixture

from src.services import google


def test_get_google_provider_config(mocker: MockerFixture):
    """Get google provider configuration."""
    mock_response = mocker.MagicMock()
    mock_get = mocker.patch("requests.get", return_value=mock_response)
    google.get_google_provider_config()
    mock_get.assert_called_once()
    mock_response.json.assert_called_once()


def test_prepare_request_uri(mocker: MockerFixture):
    """Prepare request URI."""
    authorization_endpoint = "value"
    google_provider_config = {"authorization_endpoint": authorization_endpoint}
    func_path = "src.services.google.get_google_provider_config"
    mocker.patch(func_path, return_value=google_provider_config)
    mock_prepare = mocker.patch.object(WebApplicationClient, "prepare_request_uri")

    redirect_uri = "https://example.com/google/callback"
    google.prepare_request_uri(redirect_uri)
    mock_prepare.assert_called_once_with(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=["openid", "email", "profile"],
    )


def test_create_token_request(mocker: MockerFixture):
    """Create token request for Google Account."""
    token_endpoint = "value"
    google_provider_config = {"token_endpoint": token_endpoint}
    func_path = "src.services.google.get_google_provider_config"
    mocker.patch(func_path, return_value=google_provider_config)

    token_response = ("token_url", "headers", "body")
    mock_prepare = mocker.patch.object(
        WebApplicationClient, "prepare_token_request", return_value=token_response
    )
    mock_post = mocker.patch("requests.post")

    request = mocker.MagicMock()
    request.url = "https://example.com/google"
    request.base_url = "https://example.com"
    code = "code"

    google.create_token_request(request, code)

    mock_prepare.assert_called_once_with(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    mock_post.assert_called_once_with(
        token_response[0],
        headers=token_response[1],
        data=token_response[2],
        auth=(google.CONFIG.GOOGLE_CLIENT_ID, google.CONFIG.GOOGLE_CLIENT_SECRET),
    )


def test_get_google_account_info(mocker: MockerFixture):
    """Retrieve the google account information."""
    userinfo_endpoint = "value"
    google_provider_config = {"userinfo_endpoint": userinfo_endpoint}
    func_path = "src.services.google.get_google_provider_config"
    mocker.patch(func_path, return_value=google_provider_config)

    token = mocker.MagicMock()
    mocker.patch("json.dumps", return_value=token)

    mock_get = mocker.patch("requests.get", return_value="account_info")
    mock_parse = mocker.patch.object(
        WebApplicationClient, "parse_request_body_response"
    )
    response = ("uri", "headers", "body")
    mocker.patch.object(WebApplicationClient, "add_token", return_value=response)

    result = google.get_google_account_info(token)

    mock_get.assert_called_once_with("uri", headers="headers", data="body")
    mock_parse.assert_called_once_with(token)
    assert result == "account_info"
