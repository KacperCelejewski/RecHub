import json

import pytest
from flask import url_for

from src.models.user import User


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
