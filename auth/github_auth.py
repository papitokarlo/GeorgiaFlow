from flask import Blueprint, render_template, flash, redirect, url_for, request, session, abort
from flask_login import login_user, current_user

from flask_dance.contrib.github import make_github_blueprint, github

from .models import User
from . import db

github_auth = Blueprint("github_auth", __name__)

github_blueprint = make_github_blueprint(client_id='fe175275f0cfaf40429f', client_secret='cf915e750efef9f8ff1308cd4748d7f0be8daf20')

# github_auth.register_blueprint(github_blueprint, url_prefix='/github_login')


@github_auth.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        print(account_info_json)
        return '<h1>Your Github name is {} '.format(account_info_json['login'])

    return '<h1>Request failed!</h1>'