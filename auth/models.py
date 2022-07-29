from auth import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    date_add = db.Column(db.DateTime, default = datetime.utcnow())
    password_hash = db.Column(db.String(128)) 

    def __init__(self, fullname, email, date_add, password_hash):
        self.fullname = fullname
        self.email = email
        self.password_hash = generate_password_hash(password_hash)
        self.date_add = date_add


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        email = cls.query.filter_by(email=email).first()
        if email:
            return email
    
    def add_user(self):
        db.drop_all()
        db.create_all()
        db.session.add(self)
        db.session.commit()
# new = Users("zura befadze", "begadze.zy@gmail.com", datetime.utcnow(), "kasndansda")
# Users.add_user(new)
# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(user_id)