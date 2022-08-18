from datetime import datetime
from auth import app, db, login_manager
from flask import render_template, url_for, flash, request, redirect
from flask_login import login_required, logout_user, login_user, current_user
from .forms import RegistrateForm, LoginForm
from .models import Users, Question, Comments
from questions.forms import questionForm

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/user/<user_id>', methods=['GET', 'POST'])
def get_user(user_id):
    user = Users.query.filter_by(id = user_id).first()
    form = questionForm()
    if form.validate_on_submit():
        user = current_user.id
        question = Question(form.question.data, user)

        db.session.add(question)
        db.session.commit()
        flash('posted succesfuly')
        return render_template("profile.html", user = user, form=form)
    return render_template("profile.html", user = user, form=form)


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('გამოსული ხართ')
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('ავტორიზაცია წარმატებით დასრულდა')
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrateForm()

    if form.validate_on_submit():
         user = Users(form.fullname.data, form.email.data, datetime.utcnow(), form.password.data)

         db.session.add(user)
         db.session.commit()
         flash('რეგისტრაცია წარმატებით დასრულდა!')
         return redirect(url_for('login'))
    return render_template('register.html', form=form)