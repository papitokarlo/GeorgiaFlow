from question import db
from datetime import datetime


class Post(db.Model):

    __tablename__='post'

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(50), nullable = False, index=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    tags = db.Column(db.String, db.ForeignKey('tag.name', ondelete="CASCADE"), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)    
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

    def __init__(self, heading, text, author, tags,  date_created=datetime.utcnow()):
        self.heading = heading
        self.text = text        
        self.author = author
        self.tags = tags

    def __repr__(self):
        return self.heading

# post = Post('name', 'text')

# db.session.add(post)
# db.session.commit()

class Tag(db.Model):

    __tablename__='tag'

    id =db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable = False, unique=True, index=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, name, author, date_created = datetime.utcnow()):
        self.name=name
        self.author = author

    def __repr__(self):
        return self.name


class Comment(db.Model):

    __tablename__='comment'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, text, author, post_id, date_created = datetime.utcnow() ):
        self.text = text
        self.author = author
        self.post_id = post_id
        
    def __repr__(self):
        return self.text


class Like(db.Model):

    __tablename__='like'
     
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, author, post_id, date_created = datetime.utcnow()):
        self.author = author
        self.post_id = post_id