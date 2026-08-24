def test_register_user(client):
    payload = {
        "first_name": "Karim",
        "last_name": "Ahmed",
        "email": "karim@example.com",
        "password": "supersecret123",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["email"] == "karim@example.com"


def test_duplicate_email_rejected(client):
    payload = {
        "first_name": "A",
        "last_name": "B",
        "email": "dup@example.com",
        "password": "password123",
    }
    client.post("/api/v1/auth/register", json=payload)
    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "login@example.com",
            "password": "correctpassword",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "correctpassword"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "login2@example.com",
            "password": "correctpassword",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login2@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "whatever123"},
    )
    assert response.status_code == 401