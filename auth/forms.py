from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, validators, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired

class RegistrateForm(FlaskForm):
    fullname = StringField('Fulname', [InputRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email Address', [InputRequired(), validators.Length(min=6, max=35), Email()])
    password = PasswordField('New Password', [InputRequired(), validators.Length(min=6, max=35), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', [InputRequired(), validators.Length(min=6, max=35),])
    register = SubmitField("Register")


# class LoginForm(Form):
#     email = StringField("Enter your username", validators=[DataRequired()])
#     password = PasswordField('password', validators=[DataRequired()])
#     login = SubmitField("Login")