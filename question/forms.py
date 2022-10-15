from flask_wtf import FlaskForm
from wtforms import  TextAreaField,  StringField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Length

from .models import Post, Tag
# [('Software', 'software'), ('Sales', 'sales')]
# tags - Tag.query.all()

# tag_choise = [('python', 'python'), ('flask', 'flask')]


class questionForm(FlaskForm):
    heading = StringField('heading', [Length(min=2, max=700), DataRequired(message='Question ')])
    # tag = StringField('Programming Language')
    text = TextAreaField('Question', [Length(min=2, max=1000), DataRequired(message='description')])
    ask = SubmitField("ASK")

class questionUpdateForm(FlaskForm):
    heading = StringField('heading', [Length(min=2, max=700), DataRequired(message='Question ')])
    # tag = StringField('Programming Language')
    text = StringField('Question', [Length(min=2, max=1000), DataRequired(message='description')])
    # ask = SubmitField("ASK")