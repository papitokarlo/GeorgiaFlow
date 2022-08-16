from questions import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1000), nullable = False, index=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    date_add = db.Column(db.DateTime, default = datetime.utcnow())
    comments = db.relationship('Comments', backref='question_comment')
    def __init__(self, question, user_id, date_add= datetime.utcnow()):
        self.question=question
        self.user_id = user_id
        
    def __repr__(self):
        return self.id
        

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
        return self.id



# news = Question("questmsnadnion" )
# news2= Question("questio22n")
# db.drop_all()
# db.create_all()
# db.session.add(news, news2)
# db.session.commit()
 