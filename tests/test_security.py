import base64
from pathlib import Path
import pytest
from app.main import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def login(client, username="alice", password="alice-password"):
    res = client.post("/login", json={"username": username, "password": password})
    assert res.status_code == 200
    return res.get_json()["token"]


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_login_rejects_bad_password(client):
    res = client.post("/login", json={"username": "alice", "password": "wrong"})
    assert res.status_code == 401


def test_user_cannot_read_another_user(client):
    token = login(client)
    res = client.get("/users/2", headers=auth(token))
    assert res.status_code == 403


def test_sql_injection_username_does_not_authenticate(client):
    res = client.post("/login", json={"username": "' OR 1=1 --", "password": "anything"})
    assert res.status_code == 401


def test_preferences_accept_json_only(client):
    token = login(client)
    res = client.post("/preferences/import", headers=auth(token), json={"theme": "dark"})
    assert res.status_code == 200
