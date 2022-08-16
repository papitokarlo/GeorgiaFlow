from flask_wtf import FlaskForm
from wtforms import  TextAreaField, SubmitField
from .models import Question
from wtforms.validators import Length


class questionForm(FlaskForm):
    question = TextAreaField('Question')
    ask = SubmitField("ASK")


class commentForm(FlaskForm):
    comment = TextAreaField('Answer')
    answer = SubmitField("comment")