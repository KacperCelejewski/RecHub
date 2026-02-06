import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.extensions import db


class TestRegisterEndpointStatusCodes:
    def test_should_return_201_when_user_is_registered(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "Johnt",
                "surrname": "Does",
                "email": "sample@gmail.com",
                "password": "Sample123!",
            },
        )
        assert response.status_code == 201

    def test_should_return_400_when_any_data_param_is_empty(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "",
                "surrname": "Doe",
                "email": "",
                "password": "Sample123!",
            },
        )
        assert response.status_code == 400

    def test_should_return_400_when_email_is_not_valid(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "",
                "surrname": "Doe",
                "email": "samplegmailcom",
                "password": "Sample123!",
            },
        )
        assert response.status_code == 400

    def test_should_return_400_when_password_is_not_valid(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "name": "John",
                "surrname": "Doe",
                "email": "sample@gmail.com",
                "password": "2!",
            },
        )
        assert response.status_code == 400

    def test_should_return_400_when_user_already_exists(self, client):
        client.post(
            "/api/auth/register",
            json={
                "name": "John",
                "surrname": "Doe",
                "email": "sample@gmail.com",
                "password": "Sample123!",
            },
        )
        response = client.post(
            "/api/auth/register",
            json={
                "name": "John",
                "surrname": "Doe",
                "email": "sample@gmail.com",
                "password": "Sample123!",
            },
        )
        assert response.status_code == 400

    def test_should_return_409_when_user_not_created(self, client, mocker):
        mocker.patch(
            "src.auth.register.Register.register_user",
            side_effect=SQLAlchemyError,
        )
        with pytest.raises(SQLAlchemyError):
            response = client.post(
                "/api/auth/register",
                json={
                    "name": "John",
                    "surrname": "Doe",
                    "email": "sample@gmail.com",
                    "password": "Sample123!",
                },
            )

            assert response.status_code == 409
