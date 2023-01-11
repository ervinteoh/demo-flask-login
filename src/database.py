"""This module define utilities to be used by :file:`models.py`. All
databases related utilities should be defined in this module including
any SQLAlchemy classes or functions overrides.
"""
import sqlalchemy as sa
from flask import current_app
from sqlalchemy.exc import IntegrityError

from src.extensions import db


class CRUDMixin:
    """This class contains methods to be inherited by other subclasses
    located in the package ``models``. The methods are generally used
    by database models similar to SQL operations. Namely, create,
    update, save and delete.

    .. note:: This is an abstract class.
    """

    @classmethod
    def create(cls, **kwargs) -> "CRUDMixin":
        """Create a new instance of the model.

        :return: The new model instance.
        :rtype: CRUDMixin
        """
        obj = cls(**kwargs)
        current_app.logger.info("Creating %s", obj)
        return obj.save()

    def update(self, commit=True, **kwargs) -> "CRUDMixin":
        """Update the model instance.

        :param commit: To commit the changes into the database,
            defaults to True
        :type commit: bool, optional
        :return: The model instance.
        :rtype: CRUDMixin
        """
        current_app.logger.info("Updating %s", self)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() if commit else self

    def save(self) -> "CRUDMixin":
        """Save the updated model instance into the database.

        :return: The model instance.
        :rtype: CRUDMixin
        """
        try:
            current_app.logger.info("Saving %s", self)
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            error_message = "An error occurred while saving"
            current_app.logger.exception("%s %s", error_message, self)
            db.session.rollback()
            raise
        return self

    def delete(self, commit=True) -> None:
        """Delete the model instance.

        :param commit: To commit the changes into the database,
            defaults to True
        :type commit: bool, optional
        """
        current_app.logger.info("Deleting %s", self)
        db.session.delete(self)
        return db.session.commit() if commit else None


class Model(CRUDMixin, db.Model):
    """Base abstract database model."""

    __abstract__ = True
    created_on = sa.Column(sa.DateTime, default=sa.func.now())
    updated_on = sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())


class PrimaryKeyModel(Model):
    """Primary key abstract database model."""

    __abstract__ = True
    id = sa.Column(sa.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id: int) -> "PrimaryKeyModel":
        """Get model by its model ID.

        :param record_id: The model ID.
        :type record_id: int
        :return: The model instance.
        :rtype: PrimaryKeyModel
        """
        validate_string = isinstance(record_id, str) and record_id.isdigit()
        validate_integer = isinstance(record_id, (int, float))
        return (
            cls.query.get(int(record_id))
            if any((validate_string, validate_integer))
            else None
        )
