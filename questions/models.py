from questions import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    # tags = db.Column(db.String(1000), nullable = False)
    question = db.Column(db.String(1000), nullable = False, index=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    date_add = db.Column(db.DateTime, default = datetime.utcnow())
    comments = db.relationship('Comments', backref='question_comment')
    likes = db.relationship('Likes', backref='question_likes')

    def __init__(self, question, user_id, date_add= datetime.utcnow()):
        self.question=question
        self.user_id = user_id
        
    def __repr__(self):
        return self.question
        

class Comments(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000), nullable = False, index=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    date_add = db.Column(db.DateTime, default = datetime.utcnow())

    def __init__(self, comment, user_id, question_id, date_add= datetime.utcnow()):
        self.comment = comment
        self.user_id = user_id
        self.question_id = question_id

    def __repr__(self):
        return self.comment


class Likes(db.Model):
    __tablename__='likes'

    id = db.Column(db.Integer, primary_key=True)
    date_add = db.Column(db.DateTime, default = datetime.utcnow())
    user_id= db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))

    def __init__(self,  user_id, question_id, date_add= datetime.utcnow()):
        self.user_id=user_id
        self.question_id = question_id



# for j in range(1, 1000):
#     Question.query.filter_by(id=j).delete()
# db.session.commit()