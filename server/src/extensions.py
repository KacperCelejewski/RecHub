from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()