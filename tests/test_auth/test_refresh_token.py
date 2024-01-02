import json


def test_should_return_200_when_refresh_token_is_valid(
    client, logged_in_user, register_user
):
    register_user = register_user
    logged_in_user = logged_in_user

    response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {logged_in_user.json['refresh_token']}"},
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["access_token"] != logged_in_user.json["access_token"]
    assert data["refresh_token"] != logged_in_user.json["refresh_token"]
    assert data["message"] == "Token refreshed!"


def test_should_return_422_when_refresh_token_is_invalid(
    client, logged_in_user, register_user
):
    register_user = register_user
    logged_in_user = logged_in_user

    response = client.post(
        "/api/auth/refresh",
        headers={
            "Authorization": f"Bearer {logged_in_user.json['refresh_token'] + 'SomeRandomStringToMakeItInvalid'}"
        },
    )

    assert response.status_code == 422
    data = json.loads(response.data)
    assert "msg" in data
    assert data["msg"] == "Signature verification failed"


def test_should_return_422_when_refresh_token_is_missing(
    client, logged_in_user, register_user
):
    register_user = register_user
    logged_in_user = logged_in_user

    response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": "Bearer "},
    )

    assert response.status_code == 422
    data = json.loads(response.data)
    print(data["msg"])
    assert "msg" in data
    assert (
        data["msg"]
        == "Bad Authorization header. Expected 'Authorization: Bearer <JWT>'"
    )
