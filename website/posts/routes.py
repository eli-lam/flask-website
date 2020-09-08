from flask import (render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from flask_user import roles_required

from website import db
from website.models import Post, Comment
from website.posts.forms import PostForm, CommentForm
from flask import Blueprint

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@roles_required('admin')
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.blog'))
    return render_template('create_post.html', form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.order_by(Comment.timestamp.desc())
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post_id=post.id, author=current_user, content=form.content.data)
        save_comment(comment)
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('post.html', post=post, form=form, comments=comments)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.blog'))


def save_comment(comment):
    db.session.add(comment)
    db.session.commit()
    prefix = comment.parent.path + '.' if comment.parent else ''
    comment.path = prefix + '{:0{}d}'.format(comment.id, comment.N)
    db.session.commit()


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def new_reply(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    parent = Comment.query.get_or_404(comment_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post_id=post.id, author=current_user, content=form.content.data, parent=parent.id)
        save_comment(comment)
        flash('Your reply has been posted!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return redirect(url_for('posts.post', post_id=post.id))
