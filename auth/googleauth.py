import os
import pathlib

from flask import Blueprint, render_template, flash, redirect, url_for, request, session, abort
from flask_login import login_user, current_user
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests

from .models import User
from . import db

google_auth = Blueprint("google_auth", __name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "576172265409-h3r15lj953drltvn5k3uoqqmemdjrpl1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/google-callback"
)

@google_auth.route("/google-callback")
def google_callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")

    email = id_info.get("email")
    fullname = id_info.get("name")
    password = id_info.get("password")

    if User.query.filter_by(email=email).first():

        user = User.query.filter_by(email=email).first()
        login_user(user)

        flash(f'{current_user.fullname} loged successfuly', category='success')

        next = request.args.get('next')
        if next == None or not next[0] == '/':
            next = url_for('api.index')
        return redirect(next)

    else:

        from werkzeug.security import generate_password_hash

        linkedin, github = 'None', 'None'
        password_hash = generate_password_hash('password')

        user = User(fullname, email, linkedin, github, password_hash)

        db.session.add(user)
        db.session.commit()
        login_user(user)   

    return redirect(url_for("api.index"))


@google_auth.route("/google-login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


print('en')