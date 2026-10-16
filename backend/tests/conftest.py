import itertools
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Point the app at a throwaway SQLite database before any app module is imported.
# Real environment variables take priority over .env files, so a local .env is ignored here.
_TMP_DIR = tempfile.mkdtemp(prefix="ankiit_erp_tests_")
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_TMP_DIR, 'test.db').as_posix()}"
os.environ["DEBUG"] = "false"
os.environ["ADMIN_USERNAME"] = "admin"
os.environ["ADMIN_EMAIL"] = "admin@example.com"
os.environ["ADMIN_PASSWORD"] = "Test-Admin-Pass-1"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

_user_counter = itertools.count(1)


def _bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from scripts.init_db import init_database

    init_database()

    from main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def admin_headers(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email_or_username": "admin", "password": ADMIN_PASSWORD},
    )
    assert response.status_code == 200, response.text
    return _bearer(response.json()["access_token"])


@pytest.fixture
def make_user(client):
    """Register a regular user and return (user_json, auth_headers)."""

    def _make(**overrides):
        n = next(_user_counter)
        payload = {
            "username": f"user_{n}",
            "email": f"user_{n}@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "Passw0rd!",
        }
        payload.update(overrides)
        registered = client.post("/api/v1/auth/register", json=payload)
        assert registered.status_code == 200, registered.text
        login = client.post(
            "/api/v1/auth/login",
            json={"email_or_username": payload["username"], "password": payload["password"]},
        )
        assert login.status_code == 200, login.text
        return registered.json(), _bearer(login.json()["access_token"])

    return _make
