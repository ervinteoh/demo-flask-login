"""This module define Google API related utility functions for mainly
for OAuth Access Google API in :file:`google.py` in the ``views``
package.
"""
# pylint: disable=missing-timeout
import json

import requests
from flask import Request
from oauthlib.oauth2 import WebApplicationClient

from src.settings import get_config

#: Google discovery url.
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

#: Application configurations.
CONFIG = get_config()

#: Google OAuth client.
client = WebApplicationClient(CONFIG.GOOGLE_CLIENT_ID)


def get_google_provider_config():
    """Get google provider configuration.

    :return: The received JSON response.
    :rtype: dict
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def prepare_request_uri(redirect_uri: str):
    """Prepare request URI.

    :param redirect_uri: The Google callback URI.
    :type redirect_uri: str
    :return: The request URI.
    :rtype: str
    """
    google_provider_config = get_google_provider_config()
    authorization_endpoint = google_provider_config["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=["openid", "email", "profile"],
    )
    return request_uri


def create_token_request(request: Request, code: str) -> requests.Response:
    """Create token request for Google Account.

    :param request: The current HTTPrequest object.
    :type request: Request
    :param code: The unique authorization code.
    :type code: str
    :return: The token to use with other URLs on behalf of the user.
    :rtype: requests.Response
    """
    google_provider_config = get_google_provider_config()
    token_endpoint = google_provider_config["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(CONFIG.GOOGLE_CLIENT_ID, CONFIG.GOOGLE_CLIENT_SECRET),
    )
    return token_response


def get_google_account_info(token: str) -> requests.Response:
    """Retrieve the google account information.

    :param token: The token to use with other URLs on behalf of the user.
    :type token: str
    :return: The google account info.
    :rtype: dict
    """
    google_provider_config = get_google_provider_config()
    client.parse_request_body_response(json.dumps(token.json()))
    userinfo_endpoint = google_provider_config["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    return userinfo_response
