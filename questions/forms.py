from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField
from .models import Question
from wtforms.validators import Length

class questionForm(FlaskForm):

    question = StringField('Question', [Length(min=10, max=500)])
    ask = SubmitField("ASK")