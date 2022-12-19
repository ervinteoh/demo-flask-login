"""This module defines all reusable fixtures to be used in all
subsequent tests. Parameters are ``setup`` and ``teardown`` functions
in tests to reduce duplicate code in similar tests.

.. note:: This module contains reusable fixtures only for
    __functional__ tests. In the event that a fixture would only be
    used in another test type, please include those in their respective
    conftest.
"""
import pytest
from flask import Flask
from webtest import TestApp


@pytest.fixture
def client(app: Flask) -> TestApp:
    """This fixture returns a WSGI test client.

    :param app: The application instance.
    :type app: Flask
    :return:  The test app client instance.
    :rtype: TestApp
    """
    return TestApp(app)
