from flask import render_template, request, Blueprint
from website.models import Post
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('cover.html')


@main.route('/projects')
def projects():
    return render_template('projects.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('blog.html', posts=posts)
