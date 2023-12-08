def test_should_return_201_when_user_is_registered(client):
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
