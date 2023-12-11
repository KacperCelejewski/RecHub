from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
login_manager = LoginManager()