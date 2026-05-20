from fastapi import status


def test_register_success(client):
    res = client.post("/register", json={
        "email": "new@example.com",
        "username": "newuser",
        "password": "password123",
    })
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_register_duplicate_email(client, registered_user):
    res = client.post("/register", json={
        "email": "test@example.com",
        "username": "other",
        "password": "pass",
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_register_duplicate_username(client, registered_user):
    res = client.post("/register", json={
        "email": "other@example.com",
        "username": "testuser",
        "password": "pass",
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, registered_user):
    res = client.post("/login", json=registered_user)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    res = client.post("/login", json={"username": "testuser", "password": "wrong"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_unknown_user(client):
    res = client.post("/login", json={"username": "nobody", "password": "pass"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
