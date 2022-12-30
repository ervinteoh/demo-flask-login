"""This module defines the application configurations that are
customizable through environmental variables. The application
configurations are dependent of the application instance's environment
type. If installed, python-dotenv will be used to load environment
variables from :file:`.env` and :file:`.flaskenv` files.

Set ``FLASK_ENV`` environmental variable to ``production``, ``testing``
or ``development`` for environment type configuration respectively.
"""

import os
from abc import ABC, abstractmethod

from flask import Flask

#: This directory is the application directory where the code
#: entrypoint is located. Use this directory path to locate static
#: files located in the application code.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#: This directory is the root of the entire codebase where the
#: :file:`README.md` is located. Use this path to locate any files
#: external to the application code.
WORKING_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))


class BaseConfig(ABC):
    """This class initializes base configurations settings to be
    utilized by the Flask application. Use the following example code
    on the Flask application instance::

        app.config.from_object(...)

    .. note:: This class is an abstract class that does not specify the
        current application environment. Create subclasses that extends
        the :class:`BaseConfig` to override its base configurations for
        each environment type for the Flask application to be easily
        customizable by the environmental variable ``FLASK_ENV``.
    """

    # pylint: disable=too-few-public-methods, invalid-name

    #: A generated secret key to keep the client-side sessions secure.
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(24))

    #: The folder directory for static files.
    STATIC_FOLDER = "static"

    #: Disable SQLAlchemy logging messages.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #: The folder directory for jinja templates.
    TEMPLATES_FOLDER = "templates"

    @property
    @abstractmethod
    def DATABASE_URI(self):
        """This method is an abstract property to be used by
        :func:`SQLALCHEMY_DATABASE_URI` property method to initialize
        the Database Uniform Resource Identifier (URI) in the
        application configuration.

        :return: The Database URI.
        :rtype: str
        """

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """This method uses the `DATABASE_URI` abstract property to
        initialize the database URI for SQLAlchemy Database Uniform
        Resource Identifier(URI).

        :return: The Database URI.
        :rtype: str
        """
        return os.environ.get("DATABASE_URL", f"sqlite:///{self.DATABASE_URI}")


class DebugConfig(BaseConfig):
    """This is a subclass of :class:`BaseConfig` where each base
    configuration is inherited. The class overrides the configurations
    for development environment.
    """

    #: Set the database URI to a development database.
    DATABASE_URI = os.path.join(WORKING_DIR, "development.sqlite")

    #: Disable CSRF protection for easier API development.
    WTF_CSRF_ENABLED = False


class TestingConfig(BaseConfig):
    """This is a subclass of :class:`BaseConfig` where each base
    configuration is inherited. The class overrides the configurations
    for staging environment.
    """

    #: Set the database URI to in memory so the database is not
    #: persisted for temporary testing purposes.
    DATABASE_URI = ":memory:"

    #: Disable CSRF protection for easier API development.
    WTF_CSRF_ENABLED = False


class ReleaseConfig(BaseConfig):
    """This is a subclass of :class:`BaseConfig` where each base
    configuration is inherited. The class overrides the configurations
    for production environment.
    """

    #: Set the database URI to a production database.
    DATABASE_URI = os.path.join(WORKING_DIR, "production.sqlite")


def get_config(app: Flask):
    """Get application configuration dependent on the environmental
    variables set. The enviornmental variable ``DEBUG`` should enable
    development enviornment while ``TESTING`` enables the testing
    environment.

    :param app: Flask application instance.
    :type app: Flask
    :return: The application configuration.
    :rtype: BaseConfig
    """
    if app.config["DEBUG"]:
        return DebugConfig()
    if app.config["TESTING"]:
        return TestingConfig()
    return ReleaseConfig()
