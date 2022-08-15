from flask import Flask, render_template, flash, redirect, url_for
from questions import app, login_manager, login_required, db
from flask_login import current_user
from .models import Question
from .forms import questionForm

@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    form = questionForm()
    if form.validate_on_submit():
        poster = current_user.id
        print(poster)
        question = Question(form.question.data, poster)

        db.session.add(question)
        db.session.commit()
        flash('posted succesfuly')
        return redirect(url_for('index'))
    return render_template('question.html', form=form)