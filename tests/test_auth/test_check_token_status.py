import json

import pytest


def test_should_return_200_when_token_is_valid(client, logged_in_user, register_user):
    register_user = register_user
    logged_in_user = logged_in_user

    response = client.post(
        "/api/auth/check-token-status",
        headers={"Authorization": f"Bearer {logged_in_user.json['access_token']}"},
    )
    print(response.json)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "Token is valid!"


def test_should_return_401_when_token_is_invalid(client, logged_in_user, register_user):
    register_user = register_user
    logged_in_user = logged_in_user

    response = client.post(
        "/api/auth/check-token-status",
        headers={
            "Authorization": f"Bearer {logged_in_user.json['access_token']+ 'SomeRandomStringToMakeItInvalid'}"
        },
    )

    assert response.status_code == 422
    data = json.loads(response.data)
    assert "msg" in data
    assert data["msg"] == "Signature verification failed"
