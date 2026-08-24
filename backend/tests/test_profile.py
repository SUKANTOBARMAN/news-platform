def _register_and_login(client, email="profile@example.com", password="testpass123"):
    client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Karim",
            "last_name": "Ahmed",
            "email": email,
            "password": password,
        },
    )
    login_resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_my_profile(client):
    headers = _register_and_login(client)
    response = client.get("/api/v1/user/profile/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "profile@example.com"


def test_profile_requires_auth(client):
    response = client.get("/api/v1/user/profile/me")
    assert response.status_code == 401


def test_register_and_list_device(client):
    headers = _register_and_login(client, email="device@example.com")

    create_resp = client.post(
        "/api/v1/user/profile/devices",
        headers=headers,
        json={"device_fingerprint": "abc123", "platform": "web"},
    )
    assert create_resp.status_code == 201
    assert create_resp.json()["platform"] == "web"

    list_resp = client.get("/api/v1/user/profile/devices", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1