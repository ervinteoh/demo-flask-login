"""This module is mainly for the web pages which are associated with
the user accounts. The pages includes the login, register and activate
accounts.
"""
from flask import Blueprint

from src.extensions import login_manager
from src.models import User

blueprint = Blueprint("account", __name__, url_prefix="/account")


@login_manager.user_loader
def load_user(user_id):
    """User loader callback.

    :param user_id: The user id stored in the current session.
    :type user_id: int
    :return: The user instance of the current session.
    :rtype: User
    """
    return User.get_by_id(user_id)
