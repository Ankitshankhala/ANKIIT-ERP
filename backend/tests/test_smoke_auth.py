from tests.conftest import ADMIN_PASSWORD


def test_register_without_organization_creates_personal_one(make_user):
    user, _ = make_user()
    assert user["organization_id"] is not None


def test_register_with_same_organization_name_twice(make_user):
    first, _ = make_user(organization_name="Acme Corp")
    second, _ = make_user(organization_name="Acme Corp")
    # Each registration gets its own organization rather than joining someone else's
    assert first["organization_id"] != second["organization_id"]


def test_register_duplicate_email_rejected(client, make_user):
    user, _ = make_user()
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "someone_else",
            "email": user["email"],
            "first_name": "Dup",
            "last_name": "User",
            "password": "Passw0rd!",
        },
    )
    assert response.status_code == 400


def test_login_wrong_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email_or_username": "admin", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_returns_role(client, admin_headers):
    response = client.get("/api/v1/auth/me", headers=admin_headers)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["username"] == "admin"
    assert body["role_name"] == "superuser"


def test_me_requires_token(client):
    assert client.get("/api/v1/auth/me").status_code in (401, 403)


def test_refresh_token(client):
    login = client.post(
        "/api/v1/auth/login",
        json={"email_or_username": "admin", "password": ADMIN_PASSWORD},
    ).json()
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": login["refresh_token"]})
    assert response.status_code == 200, response.text
    assert response.json()["access_token"]


def test_regular_user_cannot_read_finance(client, make_user):
    _, headers = make_user()
    response = client.get("/api/v1/finance/accounts", headers=headers)
    assert response.status_code == 403
