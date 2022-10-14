import os
import pathlib

from flask import Blueprint, render_template, flash, redirect, url_for, request, session, abort
from flask_login import  login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests


from . import db
from .forms import RegistrateForm, LoginForm, UpdateForm, UpdatePasswordForm, ForgetForm
from .models import User
from question.models import Post, Tag, Like
from question.forms import questionForm


auth = Blueprint("auth", __name__)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "576172265409-h3r15lj953drltvn5k3uoqqmemdjrpl1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/google-callback"
)

@auth.route("/google-callback")
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

    # return id_info
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect(url_for("api.index"))

@auth.route("/google-login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@auth.route('/sing-up', methods=['GET', 'POST'])
def signup():
    tags = Tag.query.order_by(Tag.name).all()
    form = RegistrateForm()
    if form.validate_on_submit():
        
        user = User(form.fullname.data, form.email.data, form.linkedin.data, form.github.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created!')
        return redirect(url_for('api.index'))
    return render_template("signup.html", form = form, tags=tags)

    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    tags = Tag.query.order_by(Tag.name).all()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f'{current_user.fullname} loged successfuly', category='success')
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('api.index')

            return redirect(next)
        else:
            flash(f'user didnt find', category='error')
    return render_template('login.html', form=form, tags = tags)


@auth.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    forget_form = ForgetForm()
    if forget_form.validate_on_submit():        
        user =  User.query.filter_by(email=forget_form.email.data).first()
        if user is not None:
            if forget_form.confirm_password.data == forget_form.new_password.data:
                new_password_hash=forget_form.new_password.data
                user.password_hash = generate_password_hash(new_password_hash)
                db.session.commit()
                flash('Password changed succesfuly', category='success')
                return redirect(url_for('auth.login'))

            else:
                flash('Confrim password doesnt match', category='error')
                return redirect(url_for('auth.forget_password'))
        else:
            flash('User with this email didnot found', category='error')
            return redirect(url_for('auth.login'))
    return render_template('update.html', forget_form=forget_form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("api.index"))


@auth.route('/user/<user_id>', methods=['GET', 'POST'])
def get_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    tags = Tag.query.order_by(Tag.name).all()
    form = questionForm()
    
    total_likes = 0
    if user.posts:
        for post in user.posts: 
            for _ in post.likes:
                total_likes+=1    
    
    correct_answers = 0
    if user.comments:
        for comment in user.comments:
            if comment.corrects:
                correct_answers+=1

    if form.validate_on_submit():
        user = current_user.id
        tag_name = request.form.get('tag_name')

        if tag_name not in {tag.name for tag in tags}:  
            new_tag = Tag(tag_name, user)
            db.session.add(new_tag)
            db.session.commit()
        
        post = Post(form.heading.data, form.text.data, user, tag_name)
        db.session.add(post)
        db.session.commit()
        flash('posted succesfuly')

        return redirect(url_for('auth.get_user', user_id=user_id))

    return render_template("profile.html", user = user, form=form, tags=tags, total_likes = total_likes, correct_answers=correct_answers)



@auth.route("/update/<user_id>", methods=['GET', 'POST'])
@login_required
def update(user_id):
    tags = Tag.query.order_by(Tag.name).all()

    form = UpdateForm()
    
    if request.method=='POST':
        update_user = User.query.filter_by(id = user_id).first()
        update_user.fullname = form.fullname.data
        update_user.email = form.email.data
        update_user.github = form.github.data
        update_user.linkedin = form.linkedin.data

        db.session.commit()

        flash('Personal info updated succesfuly', category='success')

        return redirect(url_for('auth.get_user', user_id=user_id ))

    return render_template('update.html', form=form, tags = tags)


@auth.route("/update-password/<user_id>", methods=['GET', 'POST'])
@login_required
def update_password(user_id):
    
    tags = Tag.query.order_by(Tag.name).all()

    password_form = UpdatePasswordForm()

    if request.method=='POST':
        user = User.query.filter_by(id=user_id).first()
        if user is not None and user.check_password(password_form.old_password.data):

            if password_form.confirm_password.data == password_form.new_password.data and password_form.old_password.data != password_form.new_password.data:

                new_password_hash=password_form.new_password.data
                user.password_hash = generate_password_hash(new_password_hash)
                db.session.commit()
                flash('Password updated succesfuly', category='success')

                return redirect(url_for('auth.get_user', user_id=user_id ))

            elif password_form.old_password.data == password_form.new_password.data:
                flash('As it seems, you use old password, change it with new one ', category='error')
                return redirect(url_for('auth.update_password', user_id=user_id ))

            else:
                flash('Confrim password doesnt match', category='error')
                return redirect(url_for('auth.update_password', user_id=user_id ))

        else:
            flash('Old password doesnt match', category='error')
            return redirect(url_for('auth.update_password', user_id=user_id ))

    return render_template('update.html', password_form=password_form, tags=tags)


