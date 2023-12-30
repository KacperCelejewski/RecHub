import pytest
from email_validator import EmailNotValidError

from src.models.user import PasswordNotValidError


def test_should_return_201_when_user_is_registered(client):
    import pickle

    from src.models.user import Password

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Johnt",
            "surrname": "Does",
            "email": "samplee@gmail.com",
            "password": "Sample123!",
        },
    )

    assert response.status_code == 201


def test_should_return_400_when_name_is_empty(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "",
            "surrname": "Doe",
            "email": "sample@gmail.com",
            "password": "Sample123!",
        },
    )
    assert response.status_code == 400


def test_should_return_400_when_surrname_is_empty(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "",
            "email": "sample@gmail.com",
            "password": "Sample123!",
        },
    )
    assert response.status_code == 400


def test_should_return_400_when_email_is_empty(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": "",
            "password": "Sample123!",
        },
    )

    assert response.status_code == 400


def test_should_return_400_when_password_is_empty(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": "sample@gmail.com",
            "password": "",
        },
    )
    assert response.status_code == 400


def test_should_return_400_when_password_has_no_uppercase(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": "sample@gmail.com",
            "password": "dode123!",
        },
    )

    assert response.status_code == 400


def test_should_return_400_when_password_has_no_lowercase(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": "sample@gmail.com",
            "password": "DODDIDEE123",
        },
    )

    assert response.status_code == 400


def test_should_return_400_when_password_has_no_digit(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": "sample@gmail.com",
            "password": "Doedoedoes!",
        },
    )

    assert response.status_code == 400


def test_should_return_400_when_password_has_no_special_char(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": "sample@gmail.com",
            "password": "Doe12345",
        },
    )
    assert response.status_code == 400


from flask import session


def test_login_with_valid_credentials(client, logged_in_user):
    logged_in_user = logged_in_user
    assert logged_in_user.is_authenticated is True

####
def test_login_with_missing_email(client, register_user):
    register_user = register_user
    response = client.post(
        "/api/auth/login",
        json={
            "password": register_user["password"],
            "email": "",
        },
    )
    assert response.json == {"message": "Missing email or password!"}
    assert response.status_code == 400
    


def test_login_with_missing_password(client, register_user):
    register_user = register_user

    response = client.post(
        "/api/auth/login",
        json={
            "email": "sample@gmail.com",
            "password": "",
        },
    )

    assert response.status_code == 400
    assert response.json == {"message": "Missing email or password!"}


def test_login_with_invalid_email(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "invalid@gmail.com",
            "password": "Sample123!",
        },
    )

    assert response.status_code == 404
    assert response.json == {"message": "User not found!"}


def test_login_with_invalid_password(client, register_user):
    register_user = register_user

    response = client.post(
        "/api/auth/login",
        json={
            "email": register_user["email"],
            "password": "InvalidPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.json == {"message": "Invalid password!"}


def test_should_return_200_when_user_is_logged_out(client, logged_in_user):
    logged_in_user = logged_in_user
    response = client.get("/api/auth/logout")
    response = client.get("/api/auth/logout")
    assert response.status_code == 200
    assert response.json == {"message": "User is not logged in!"}



def test_should_return_200_when_user_is_not_logged_in(client):

    response = client.get("/api/auth/logout")
    assert response.status_code == 200
    assert response.json == {"message": "User is not logged in!"}


def test_should_return_200_when_user_is_logged_in_and_wants_to_logout(client, logged_in_user):
    logged_in_user = logged_in_user
    response = client.get("/api/auth/is_logged")
    assert response.status_code == 200



def test_should_return_200_when_user_is_not_logged_in_and_wants_to_logout(client):
    
    response = client.get("/api/auth/is_logged")
    assert response.status_code == 200
    assert response.json == {"message": "User is not logged in!"}
