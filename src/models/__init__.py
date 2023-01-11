"""This package defines model class which are associated by
user-defined Python classes with database tables, and instances of
those classes (objects) with rows in their corresponding tables by
SQLAlchemy Object Relational Mapper. With the help of another
extension ``Flask-Migration``, the model schemas are generated
to the ``migrations`` folder to be mapped directly to a defined
SQL database.

.. admonition:: Model Usage

    After creating, updating or deleting a model, run the command
    below to add a new migration to the database::

        $ flask db migrate

    To update the database to a newer migration version, run the
    following command::

        $ flask db upgrade
"""
from src.models.user import User, UserToken
