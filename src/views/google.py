"""This module defines routes that handles OAuth 2.0 Google requests
for users to sign in to their account with Google."""
from flask import Blueprint, abort, redirect, request, url_for
from flask_login import login_user

from src.models import User
from src.services import google

blueprint = Blueprint("google", __name__, url_prefix="/google")


@blueprint.route("/authenticate")
def authenticate():
    """Google authenticate request."""
    base_url = request.host_url.rstrip("/")
    redirect_uri = base_url + url_for("google.callback")
    return redirect(google.prepare_request_uri(redirect_uri))


@blueprint.route("/callback")
def callback():
    """Google callback view."""
    code = request.args.get("code")
    token = google.create_token_request(request, code)
    user_info = google.get_google_account_info(token).json()

    if not user_info.get("email_verified"):
        return abort(400)

    email = user_info["email"]
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User.create(
            username=user_info["sub"],
            email=email,
            first_name=user_info["given_name"],
            last_name=user_info["family_name"],
            is_active=True,
        )
    login_user(user, remember=True)
    return redirect(url_for("public.home"))
