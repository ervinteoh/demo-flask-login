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

    # Flask Mail server default to mail trap url.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.mailtrap.io")

    # Flask Mail port default to mail trap config.
    MAIL_PORT = os.environ.get("MAIL_PORT", 2525)

    # Flask Mail username authentication.
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")

    # Flask Mail password authentication.
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    # Flask Mail TLS default to mail trap config.
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)

    # Flask Mail SSL default to mail trap config.
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)

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
        database_url = os.environ.get("DATABASE_URL")
        return database_url or f"sqlite:///{self.DATABASE_URI}"


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

    #: Application environment set to TESTING.
    TESTING = True

    #: Disable CSRF protection for easier API development.
    WTF_CSRF_ENABLED = False


class ReleaseConfig(BaseConfig):
    """This is a subclass of :class:`BaseConfig` where each base
    configuration is inherited. The class overrides the configurations
    for production environment.
    """

    #: Set the database URI to a production database.
    DATABASE_URI = os.path.join(WORKING_DIR, "production.sqlite")

    # Flask Mail server default to mail trap url.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "send.smtp.mailtrap.io")


def get_config():
    """Get application configuration dependent on the environmental
    variables set. The environmental variable ``DEBUG`` should enable
    development environment while ``TESTING`` enables the testing
    environment.

    :return: The application configuration.
    :rtype: BaseConfig
    """
    if os.environ.get("FLASK_TESTING"):
        return TestingConfig()
    if os.environ.get("FLASK_DEBUG"):
        return DebugConfig()
    return ReleaseConfig()
