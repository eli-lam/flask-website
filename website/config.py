import os

class Config:
    SECRET_KEY = '8025761d655ceef3c0866aa89238c75e'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/data/site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    USER_ENABLE_CONFIRM_EMAIL = False  # Force users to confirm their email
    USER_EMAIL_SENDER_NAME = 'Elizabeth Lam'
    USER_EMAIL_SENDER_EMAIL = 'elilam.website@gmail.com'

