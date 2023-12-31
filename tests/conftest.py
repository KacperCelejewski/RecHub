import os

import pytest
from flask import Flask

from flask_sqlalchemy import SQLAlchemy


from src.extensions import db
from src.models.user import User
from application import application as app


@pytest.fixture
def app_mock():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "TEST_SECRET_KEY"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_mock):
    return app_mock.test_client()


# @pytest.fixture
# def register_user(client):
#     user_data = {
#         "name": "John",
#         "surrname": "Doe",
#         "email": "johndoe@gmail.com",
#         "password": "Sam222ssple123!",
#     }

#     response = client.post("/api/auth/register", json=user_data)

#     assert response.json == {"message": "User registered!"}
#     assert response.status_code == 201

#     return user_data


# @pytest.fixture
# def logged_in_user(client, register_user):
#     register_user = register_user

#     login_data = {
#         "email": register_user["email"],
#         "password": register_user["password"],
#     }
#     response = client.post("/api/auth/login", json=login_data)

#     assert response.status_code == 200

#     user = User.query.filter_by(email=register_user["email"]).first()

#     yield user

#     db.session.delete(user)
#     db.session.commit()
