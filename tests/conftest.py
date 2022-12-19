"""This module defines all reusable fixtures to be used in all
subsequent tests. Parameters are ``setup`` and ``teardown`` functions
in tests to reduce duplicate code in similar tests.

.. note:: This module contains reusable fixtures for every test type.
    In the event that a fixture would only be used in a specific test
    type, please include those in their respective conftest.
"""
# pylint: disable=invalid-name
import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src import create_app
from src.extensions import db as _db


@pytest.fixture(name="app")
def fixture_app() -> Flask:
    """This fixture return a Flask application instance with testing
    application context and testing environment enabled.

    :yield: The application instance.
    :rtype: Flask
    """
    os.environ["TESTING"] = "True"
    application = create_app()
    ctx = application.test_request_context()
    ctx.push()

    yield application

    ctx.pop()


@pytest.fixture(name="db")
def fixture_db(app: Flask) -> SQLAlchemy:
    """This fixture return a database instance within the Flask
    application context created in :func:`fixture_app`.

    :param app: The application instance.
    :type app: Flask
    :yield: The database instance.
    :rtype: SQLAlchemy
    """
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()
