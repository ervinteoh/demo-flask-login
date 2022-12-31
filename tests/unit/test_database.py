"""This module defines unit test cases for the database utilities
defined in :file:`database.py`.
"""
import pytest
import sqlalchemy as sa
from pytest_mock import MockerFixture as Mocker
from sqlalchemy.exc import IntegrityError

from src.database import CRUDMixin, Model, PrimaryKeyModel, db


class MockModel(Model):
    """This class is a mock object utility for the test cases defined
    in :class:`TestCRUDMixin`.

    :param name: The user's name.
    :type name: str
    :param age: The user's age.
    :type age: int
    """

    name = sa.Column(sa.String(30), primary_key=True)
    age = sa.Column(sa.Integer)


class MockPKModel(PrimaryKeyModel):
    """This class is a mock object utility for the test cases defined
    in :class:`TestPrimaryKeyModel`.
    """


@pytest.mark.usefixtures("db")
class TestCRUDMixin:
    """Test :class:`CRUDMixin` abstract class."""

    @pytest.fixture(name="model")
    def fixture_model(self):
        """Model fixture."""
        return MockModel(name="James", age=21)

    def test_create_valid_attribute(self, mocker: Mocker, model: MockModel):
        """Create model with valid attributes."""
        mocker.patch.object(CRUDMixin, "save", return_value=model)
        result = MockModel.create(name=model.name, age=model.age)
        result.save.assert_called_once()
        assert result.name == model.name
        assert result.age == model.age
        assert result == model

    def test_create_invalid_attribute(self, mocker: Mocker):
        """Create model with invalid attributes."""
        mock_save = mocker.patch.object(CRUDMixin, "save")
        with pytest.raises(TypeError):
            MockModel.create(name="James", invalid=21)
            mock_save.assert_not_called()

    def test_update_valid_attribute(self, mocker: Mocker, model: MockModel):
        """Update model with valid attributes."""
        db.session.add(model)
        db.session.commit()
        mocker.patch.object(CRUDMixin, "save", return_value=model)
        model = model.update(name="John")
        model.save.assert_called_once()
        assert model.name == "John"

    def test_update_invalid_attribute(self, mocker: Mocker, model: MockModel):
        """Update model with invalid attributes."""
        db.session.add(model)
        db.session.commit()
        mocker.patch.object(CRUDMixin, "save", return_value=model)
        model = model.update(name="John", invalid=30)
        model.save.assert_called_once()
        assert model.name == "John"
        assert model.age != 30

    def test_save_instance(self, mocker: Mocker, model: MockModel):
        """Save model instance."""
        mocker.patch.object(db.session, "add")
        mocker.patch.object(db.session, "commit")
        model = model.save()
        db.session.add.assert_called_once_with(model)
        db.session.commit.assert_called_once()

    def test_save_invalid_instance(self, mocker: Mocker, model: MockModel):
        """Save invalid model instance."""

        def session_add(_):
            raise IntegrityError("Some error.", "params", "orig")

        mocker.patch.object(db.session, "add", side_effect=session_add)
        mocker.patch.object(db.session, "rollback")
        with pytest.raises(IntegrityError):
            model.save()
        db.session.rollback.assert_called_once()

    def test_delete_instance(self, mocker: Mocker, model: MockModel):
        """Delete model instance."""
        mocker.patch.object(db.session, "delete")
        mocker.patch.object(db.session, "commit")
        model.delete()
        db.session.delete.assert_called_once_with(model)
        db.session.commit.assert_called_once()

    def test_delete_instance_no_commit(self, mocker: Mocker, model: MockModel):
        """Delete model instance without commit."""
        mocker.patch.object(db.session, "delete")
        mocker.patch.object(db.session, "commit")
        model.delete(commit=False)
        db.session.delete.assert_called_once_with(model)
        db.session.commit.assert_not_called()


@pytest.mark.usefixtures("db")
class TestPrimaryKeyModel:
    """Test :class:`PrimaryKeyModel` abstract class."""

    @pytest.fixture(name="model")
    def fixture_model(self):
        """Model fixture."""
        return MockPKModel(id=1)

    def test_get_model_by_id_str(self, mocker: Mocker, model: MockPKModel):
        """Get model by a string id."""
        mock_get = mocker.patch("sqlalchemy.orm.Query.get")
        mock_get.return_value = model
        result = MockPKModel.get_by_id(1)
        mock_get.assert_called_with(1)
        assert result == model

    def test_get_model_by_id_int(self, mocker: Mocker, model: MockPKModel):
        """Get model by a string id."""
        mock_get = mocker.patch("sqlalchemy.orm.Query.get")
        mock_get.return_value = model
        result = MockPKModel.get_by_id("1")
        mock_get.assert_called_with(1)
        assert result == model

    def test_get_model_by_id_invalid_type(self):
        """Get model by invalid type."""
        assert MockPKModel.get_by_id(1.1) is None
