from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager


cors = CORS(resources={r'/*': {'origins': '*'}})
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
