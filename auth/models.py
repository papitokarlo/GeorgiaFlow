from auth import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from question.models import Post, Tag, Comment, Correct, Like


def name_capitalize(fullname):
    words=[]
    fullname = fullname.split()
    for word in fullname:
        new_word = word.capitalize()
        words.append(new_word)
    fullname  = ' '.join([str(elem) for elem in words])
    return fullname


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable = False, index=True)
    email = db.Column(db.String(100), nullable = False, unique = True, index=True)
    linkedin = db.Column(db.String(50),  nullable = False) 
    github = db.Column(db.String(45),  nullable = False) 
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    password_hash = db.Column(db.String(128)) 
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    tags = db.relationship('Tag', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    correct = db.relationship('Correct', backref='correct_user', passive_deletes=True)

    def __init__(self, fullname, email, linkedin, github,  password_hash, date_created=datetime.utcnow()):
        self.fullname = name_capitalize(fullname)
        self.email = email
        self.linkedin = linkedin
        self.github = github
        self.password_hash = generate_password_hash(password_hash)



    def __repr__(self):
        return self.fullname

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)