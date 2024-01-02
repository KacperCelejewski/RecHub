import json
from flask import url_for
import pytest
from src.models.user import User


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


def test_login_success(client, register_user):
    register_user = register_user
    response = client.post(
        "api/auth/login",
        json={"email": "sample@gmail.com", "password": "Sam222ssple123!"},
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["message"] == "User logged in!"


def test_login_missing_parameter(client, register_user):
    register_user = register_user
    response = client.post(
        "api/auth/login",
        json={"email": "sample@gmail.com", "password": ""},
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "Missing password parameter"


def test_login_user_not_found(client):
    response = client.post(
        "api/auth/login",
        json={"email": "sample@gmail.com", "password": "Sam222ssple123"},
    )
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "User not found!"


def test_login_invalid_password(client, register_user):
    register_user = register_user
    response = client.post(
        "api/auth/login",
        json={"email": "sample@gmail.com", "password": "WrongPassword123!"},
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "Invalid password!"
