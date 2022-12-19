"""This module defines the functional tests for the routes in
```public.py``` in the ```views``` package.
"""
import pytest
from webtest import TestApp


@pytest.mark.usefixtures("db")
def test_visit_home_page(client: TestApp):
    """Visit home page.

    :param client: The test app client instance.
    :type client: TestApp
    """
    res = client.get("/")
    assert "<title>Home - Flask Login</title>" in res
