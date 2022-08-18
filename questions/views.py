from flask import Flask, render_template, flash, redirect, url_for, request
from questions import app, login_manager, login_required, db
from sqlalchemy import desc
from flask_login import current_user
from .models import Question, Comments
from .forms import questionForm, commentForm


@app.route('/delete-question/<question_id>', methods=['GET', 'POST'])
@login_required
def delete_question(question_id):
    post = Question.query.filter_by(id=question_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Question deleted', category='success')
    return redirect(url_for('allQuestion'))

@app.route('/delete-comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted', category='success')
    return redirect(url_for('allQuestion'))


@app.route('/allQuestion', methods=['GET', 'POST'])
def allQuestion():
    questions = Question.query.order_by(desc(Question.date_add)).all()
    return render_template('allquestions.html', questions=questions)


@app.route('/questions/<question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return render_template('detail.html', question=question)


@app.route("/allQuestion/<question_id>", methods = ['GET', 'POST'])
@login_required
def add_comment(question_id):
    text =request.form.get('text')
    if text:
        user = current_user.id
        comment = Comments(text, user, question_id)    
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('allQuestion', question_id=question_id))

