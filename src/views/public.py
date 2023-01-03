"""This module is mainly for the static web pages such as Home, About
and Contact pages.
"""
from flask import Blueprint, render_template

blueprint = Blueprint("public", __name__)


@blueprint.route("/home")
@blueprint.route("/")
def home():
    """Home Page."""
    return render_template("pages/public/home.jinja")


@blueprint.route("/terms-of-service")
def terms_of_service():
    """Terms of Service Page."""
    return render_template("pages/public/terms_of_service.jinja")
