from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo, Length
from wtforms import ValidationError
from .models import Users

class RegistrateForm(FlaskForm):

    fullname = StringField('Fulname', [Length(min=4, max=25)])
    email = StringField('Email Address', [Length(min=6, max=35), Email()])
    password = PasswordField('New Password', [Length(min=6, max=35), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', [Length(min=6, max=35),])
    register = SubmitField("Register")

    def validate_email(self, email):
        if Users.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')

    # def validate_username(self, username):
    #     if Users.query.filter_by(username=self.username.data).first():
    #         raise ValidationError('Username has been registered')

class LoginForm(FlaskForm):

    email = StringField("Enter your email", validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField("Login")