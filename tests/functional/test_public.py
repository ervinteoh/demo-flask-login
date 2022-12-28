"""This module defines the functional tests for the routes in
```public.py``` in the ```views``` package.
"""
import pytest
from webtest import TestApp

from src.views.public import blueprint


@blueprint.route("/exception")
def server_error():
    """Server error view."""
    raise Exception


@pytest.mark.usefixtures("db")
def test_visit_home_page(client: TestApp):
    """Visit home page.

    :param client: The test app client instance.
    :type client: TestApp
    """
    res = client.get("/")
    assert "<title>Home - Flask Login</title>" in res


@pytest.mark.usefixtures("db")
def test_visit_page_not_exist(client: TestApp):
    """Visit page that does not exist.

    :param client: The test app client instance.
    :type client: TestApp
    """
    res = client.get("/random", expect_errors=True)
    assert 404 == res.status_int
    assert "<title>Page Not Found - Flask Login</title>" in res


@pytest.mark.usefixtures("db")
def test_route_exception(client: TestApp):
    """Route raises exception.

    :param app: The application instance.
    :type app: Flask
    :param client: The test app client instance.
    :type client: TestApp
    """
    res = client.get("/exception", expect_errors=True)
    assert 500 == res.status_int
    assert "<title>Server Error - Flask Login</title>" in res
