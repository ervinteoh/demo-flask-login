"""This module defines helper factories to create models with real data
to be used in the test cases. This allows for the functionalities to be
tested with real case data scenarios.
"""
# pylint: disable=too-few-public-methods
import factory
from factory.alchemy import SQLAlchemyModelFactory

from src.database import db
from src.models import user


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    class Meta:
        """Factory configuration."""

        model = user.User

    id = factory.Sequence(lambda n: n)
    username = factory.LazyAttribute(lambda x: f"{x.first_name}_{x.last_name}".lower())
    email = factory.LazyAttribute(
        lambda x: f"{x.first_name}.{x.last_name}@example.com".lower()
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker(
        "password",
        length=30,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )
    is_active = False
    login_attempt = 0
