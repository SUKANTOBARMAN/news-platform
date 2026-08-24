def _register(client, email="roleuser@example.com"):
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "first_name": "Role",
            "last_name": "User",
            "email": email,
            "password": "testpass123",
        },
    )
    return resp.json()["id"]


def test_create_role_and_assign(client):
    user_id = _register(client)

    create_role_resp = client.post("/api/v1/admin/users/roles/", json={"name": "editor_in_chief"})
    assert create_role_resp.status_code == 201
    role_id = create_role_resp.json()["id"]

    assign_resp = client.post(
        f"/api/v1/admin/users/{user_id}/roles", json={"role_id": role_id}
    )
    assert assign_resp.status_code == 200
    assert any(r["name"] == "editor_in_chief" for r in assign_resp.json()["roles"])


def test_list_roles(client):
    client.post("/api/v1/admin/users/roles/", json={"name": "reporter"})
    response = client.get("/api/v1/admin/users/roles/")
    assert response.status_code == 200
    assert any(r["name"] == "reporter" for r in response.json())


def test_duplicate_role_rejected(client):
    client.post("/api/v1/admin/users/roles/", json={"name": "subscriber"})
    second = client.post("/api/v1/admin/users/roles/", json={"name": "subscriber"})
    assert second.status_code == 400