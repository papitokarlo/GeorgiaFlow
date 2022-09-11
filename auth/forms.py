from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField, URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL
from wtforms import ValidationError
from .models import User

class RegistrateForm(FlaskForm):

    fullname = StringField('Fulname', [Length(min=2, max=70), DataRequired(message='input your fullname')])
    email = StringField('Email Address', [Length(min=5, max=60), Email(message='Requeired type is : example@example.exe'), DataRequired(message='input your email')])
    linkedin = URLField('LinkedIn addres', [Length(min=6, max=70), URL(message='Requeired type is URL http/...'), DataRequired(message='input your linkedin account')])
    github = URLField('GitHub addres', [Length(min=6, max=70), URL(message='Requeired type is URL http/...'), DataRequired(message='input your github account')])
    password = PasswordField('New Password', [Length(min=6, max=35), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', [Length(min=6, max=35),])
    register = SubmitField("Register")

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')

    # def validate_username(self, username):
    #     if Users.query.filter_by(username=self.username.data).first():
    #         raise ValidationError('Username has been registered')

class LoginForm(FlaskForm):

    email = StringField("Enter your email", validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    login = SubmitField("Login")


class UpdateForm(FlaskForm):

    fullname = StringField('Fulname', [Length(min=2, max=70), DataRequired(message='input your fullname')])
    email = StringField('Email Address', [Length(min=5, max=60), Email(message='Requeired type is : example@example.exe'), DataRequired(message='input your email')])
    linkedin = URLField('LinkedIn addres', [Length(min=6, max=70), URL(message='Requeired type is URL http/...'), DataRequired(message='input your linkedin account')])
    github = URLField('GitHub addres', [Length(min=6, max=70), URL(message='Requeired type is URL http/...'), DataRequired(message='input your github account')])
    update = SubmitField("Register")

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')

class UpdatePasswordForm(FlaskForm):

    old_password = PasswordField('Old Password', [Length(min=6, max=35)])
    new_password = PasswordField('New Password', [Length(min=6, max=35), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', [Length(min=6, max=35),])
    update = SubmitField("UPDATE")
    

class ForgetForm(FlaskForm):
    email = StringField('Registred email', [Length(min=6, max=35), Email(message='Requeired type is : example@example.exe'), DataRequired(message='input your email')])
    new_password = PasswordField('New Password', [Length(min=6, max=35), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Repeat Password', [Length(min=6, max=35),])
    update = SubmitField("UPDATE")