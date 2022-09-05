from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import  login_required, logout_user, login_user, current_user


from . import db
from .forms import RegistrateForm, LoginForm
from .models import User
from question.models import Post, Tag, Like
from question.forms import questionForm


auth = Blueprint("auth", __name__)

@auth.route('/sing-up', methods=['GET', 'POST'])
def signup():
    form = RegistrateForm()
    if form.validate_on_submit():
        
        user = User(form.fullname.data, form.email.data, form.linkedin.data, form.github.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created!')
        return redirect(url_for('api.index'))
    return render_template("signup.html", form = form)

    
@auth.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("api.index"))


@auth.route('/user/<user_id>', methods=['GET', 'POST'])
def get_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    tags = Tag.query.order_by(Tag.date_created).all()

    # posts = Post.query.order_by(Post.date_created).all()
    form = questionForm()

    # total_likes = 0
    # for likes in user.posts:

    if form.validate_on_submit():
        user = current_user.id
        tag_name = request.form.get('tag_name')

        if tag_name not in tags:     
            new_tag = Tag(tag_name, user)
            db.session.add(new_tag)
            db.session.commit() 

        post = Post(form.heading.data, form.text.data, user, tag_name)

        db.session.add(post)
        db.session.commit()
        flash('posted succesfuly')

        return render_template("profile.html", user = user, form=form, tags = tags)

    return render_template("profile.html", user = user, form=form, tags = tags)
