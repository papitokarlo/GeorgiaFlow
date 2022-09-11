from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import  login_required, current_user
from flask import jsonify

from question import db

from .forms import questionUpdateForm
from .models import Post, Comment, Like, Tag, Correct

post = Blueprint("post", __name__)

@post.route('/post/<post_id>', methods=['GET', 'POST'])
def post_detail(post_id):

    tags = Tag.query.order_by(Tag.name).all()
    post = Post.query.filter_by(id=post_id).first()
    return render_template('detail.html', post=post, tags=tags)

@post.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', category='success')

    next = request.args.get('next')

    if next == None or not next[0] == '/':
        next = url_for('api.index')

    return redirect(next)


@post.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('post.post_detail', post_id = post_id ))


@post.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    post_id = comment.post.id
    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('post.post_detail', post_id = post_id ))


@post.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


@post.route("/edit-post/iditpost:<post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id ):
    post_update_form = questionUpdateForm()

    tags = Tag.query.order_by(Tag.date_created).all()
    update_post = Post.query.filter_by(id=post_id).first()
    if post_update_form.validate_on_submit():

        update_post.heading = post_update_form.heading.data
        update_post.tags = request.form.get('tag_name')
        update_post.text = post_update_form.text.data

        db.session.commit()
        flash('Personal info updated succesfuly', category='success')

        return redirect(url_for('post.post_detail', post_id=post_id ))
    return render_template('update.html', post_update_form=post_update_form, tags = tags, update_post=update_post )


@post.route("/tag-post/<tag_name>'sallpost:", methods=['GET', 'POST'])
def tag_posts(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first()
    tags = Tag.query.order_by(Tag.name).all()
    posts = Post.query.order_by(Post.date_created).all()
    return render_template('tags.html', tag = tag, tags=tags, posts=posts)


@post.route("/marck-as-correct/<comment_text><post_id><comment_id>", methods=['POST','GET'])
@login_required
def correct(comment_text, post_id, comment_id):
    post = Post.query.filter_by(id=post_id).first()
    comment = Comment.query.filter_by(id=comment_id).first()
    correct = Correct.query.filter_by(author=current_user.id, post_id=post_id, comment_id = comment_id ).first()

    if not comment:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif correct:
        db.session.delete(correct)
        db.session.commit()
    else:
        correct = Correct(current_user.id, post_id, comment_id)
        db.session.add(correct)
        db.session.commit()

    return redirect(url_for('post.post_detail', post_id = post_id))
