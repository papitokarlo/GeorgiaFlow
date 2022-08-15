from questions import db
from datetime import datetime


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable = False, index=True)
    poster_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    date_add = db.Column(db.DateTime, default = datetime.utcnow())

    def __init__(self, question, poster_id, date_add= datetime.utcnow()):
        self.question=question
        self.poster_id = poster_id
        

# news = Question("questmsnadnion" )
# news2= Question("questio22n")
# db.drop_all()
# db.create_all()
# db.session.add(news, news2)
# db.session.commit()
 