"""This module initializes all the Flask extensions used in the
application. The extension is initialized in the application instance
in the application factory method :func:`register_extensions`.

.. note:: Do not define any functions in this module. This module
    should only initialize the extensions required for the Flask
    application.
"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

#: Flask-Bcrypt is a Flask extension that provides bcrypt hashing
#: utilities for your application.
bcrypt = Bcrypt()

#: Cross-Site Request Forgery (CSRF) is an attack that forces
#: authenticated users to submit a request to a Web application against
#: which they are currently authenticated. CSRFProtect enables CSRF
#: protection globally across the Flask application.
csrf_protect = CSRFProtect()

#: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper
#: that gives application developers the full power and flexibility of
#: SQL. The extension compatibility ranges to widely known databases
#: such as SQLite, PostgreSQL, Microsoft SQL Server, Oracle, etc.
db = SQLAlchemy()

#: Flask-Migrate is an extension that handles SQLAlchemy database
#: migrations for Flask applications using Alembic. The database
#: operations are made available through the Flask command-line
#: interface. Execute `flask db --help` in the command line to find out
#: more.
migrate = Migrate()

#: Flask-Mail extension provides a simple interface to set up SMTP with
#: your Flask application and to send messages from your views and
#: scripts.
mail = Mail()

#: Flask-JWT-Extended is a user authentication package that provides
#: the create_access_token function for making new access JWTs. It also
#: provides the jwt_required decorator for protecting the API endpoints
#: (for checking whether users have logged in).
jwt = JWTManager()
