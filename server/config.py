import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
