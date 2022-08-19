from auth import db, admin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from questions.models import Question, Comments, Likes

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200), nullable = False, index=True)
    email = db.Column(db.String(100), nullable = False, unique = True, index=True)
    date_add = db.Column(db.DateTime, default = datetime.utcnow())
    password_hash = db.Column(db.String(128)) 
    posts = db.relationship('Question', backref='user')
    comments = db.relationship('Comments', backref='comment_user')
    likes = db.relationship('Likes', backref='user_likes')


    def __init__(self, fullname, email, date_add, password_hash):
        self.fullname = fullname.upper()
        self.email = email
        self.password_hash = generate_password_hash(password_hash)
        self.date_add = date_add

    def __repr__(self):
        return self.fullname

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


admin.add_view(ModelView(Users, db.session))

# Users.query.filter_by(id=9).delete()
# db.session.commit()
  
# new = Users("zura befadze", "begadze.zy@gmail.com", datetime.utcnow(), "kasndansda")
# db.drop_all()
# db.create_all()
# db.session.add(new)
# db.session.commit()
