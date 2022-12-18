"""This module initializes the flask application instance by defining
factory functions which are executed by flask command line interface
with the following command::

    $ export FLASK_APP=src:create_app()
    $ flask run

The factory pattern enforces a top-down approach to the application
structure by avoiding circular imports. Use the following code to use
the application instance::

    from flask import current_app

The flask configuration settings are based in :file:`settings.py` which
are used depending on the environment set on ``FLASK_ENV``. Please read
:file:`settings.py` for more information.
"""
from flask import Flask

from src import extensions, settings
from src.views import public


def create_app() -> Flask:
    """The application factory function that initializes the
    application instance to be used by the Flask command line
    interface.

    .. seealso:: Refer to :file:`settings.py` for more information on
        Flask configuration settings.

    :return: Flask application instance.
    :rtype: Flask
    """
    app = Flask(__name__)
    config = settings.get_config(app)
    app.config.from_object(config)
    app.url_map.strict_slashes = False

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)

    return app


def register_extensions(app: Flask):
    """Register Flask extensions to the application instance
    from the extensions initialized in :file:`extensions.py`.

    :param app: The application instance.
    :type app: Flask
    """
    extensions.bcrypt.init_app(app)
    extensions.db.init_app(app)
    extensions.csrf_protect.init_app(app)
    # extensions.login_manager.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
    extensions.mail.init_app(app)
    extensions.jwt.init_app(app)
    app.extensions["mail"].debug = 0


def register_blueprints(app: Flask):
    """Register Flask blueprints from the blueprints initialized
    in the modules of the ``views`` package.

    :param app: The application instance.
    :type app: Flask
    """
    app.register_blueprint(public.blueprint)


def register_shellcontext(app: Flask):
    """Register shell context objects to be used in the Flask
    command line interface.

    :param app: The application instance.
    :type app: Flask
    """
    shell_context = {"db": extensions.db}

    app.shell_context_processor(lambda: shell_context)
