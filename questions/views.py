from flask import Flask, render_template, flash, redirect, url_for, request
from questions import app, login_manager, login_required, db
from sqlalchemy import desc
from flask_login import current_user
from .models import Question, Comments
from .forms import questionForm, commentForm

@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    form = questionForm()
    if form.validate_on_submit():
        user = current_user.id
        print(user)
        question = Question(form.question.data, user)

        db.session.add(question)
        db.session.commit()
        flash('posted succesfuly')
        return redirect(url_for('index'))
    return render_template('question.html', form=form)

@app.route('/myQuestion', methods=['GET', 'POST'])
@login_required
def myQuestion():
    questions = Question.query.filter_by(user_id=current_user.id)
    return render_template('myquestions.html', questions=questions)

@app.route('/allQuestion', methods=['GET', 'POST'])
def allQuestion():
    questions = Question.query.order_by(desc(Question.date_add)).all()
    return render_template('allquestions.html', questions=questions)


@app.route("/allQuestion/<question_id>", methods = ['GET', 'POST'])
@login_required
def add_comment(question_id):
    text =request.form.get('text')
    if text:
        user = current_user.id
        comment = Comments(text, user, question_id)    
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('allQuestion'))


    
# @app.route('/create-comment<>', methods=['GET', 'POST'])
# @login_required
# def create_comment():
#     return redirect()
