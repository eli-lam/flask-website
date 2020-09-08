import os
import secrets
from threading import Thread
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from website import mail
from website import db
from website.models import User, Role


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/data/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='elilam.website@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    Thread(target=send_async_email, args=(current_app, msg)).start()


def find_or_create_role(name):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name)
        db.session.add(role)
    return role


def set_role(user_id, role):
    user = User.query.get_or_404(user_id)
    if role:
        user.roles.append(role)
    return user
