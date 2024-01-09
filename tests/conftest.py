import os

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from application import application as app
from src.extensions import db
from src.models.user import User


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


@pytest.fixture
def create_user():
    """
    Fixture that creates a user with a given email and password.
    """
    user = User(
        name="John",
        surrname="Doe",
        email="sample@gmail.com",
        password_hashed="Sam222ssple123!",
    )
    return user


@pytest.mark.parametrize("email, password", [("sample@gmail.com", "Sam222ssple123!")])
@pytest.fixture
def register_user(client, create_user):
    """
    Fixture that registers a user.
    """
    create_user = create_user
    response = client.post(
        "/api/auth/register",
        json={
            "name": create_user.name,
            "surrname": create_user.surrname,
            "email": create_user.email,
            "password": create_user.password_hashed,
        },
    )
    return response


@pytest.fixture
def logged_in_user(client, register_user):
    """
    Fixture that logs in a user.
    """
    register_user = register_user

    response = client.post(
        "/api/auth/login",
        json={
            "email": "sample@gmail.com",
            "password": "Sam222ssple123!",
        },
    )
    return response
