from flask import Blueprint, render_template
from sqlalchemy import desc
from question.models import Post
api = Blueprint("api", __name__)

@api.route('/')
@api.route("/index")
def index():
    posts = Post.query.order_by(desc(Post.date_created)).all()
    return render_template('index.html', posts=posts)
