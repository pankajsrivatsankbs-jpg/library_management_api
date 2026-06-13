import uuid
import httpx

BASE_URL = "http://localhost:8000"
PASSWORD = "pytestpass123"


def unique_username():
    return f"pytest_user_{uuid.uuid4().hex[:8]}"


def create_user(username: str, password: str):
    return httpx.post(
        f"{BASE_URL}/users/",
        json={
            "username": username,
            "password": password,
        },
    )


def login_user(username: str, password: str):
    return httpx.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_user():
    username = unique_username()

    response = create_user(username, PASSWORD)

    assert response.status_code == 200
    assert response.json()["username"] == username
    assert "hashed_password" not in response.json()
    assert "password" not in response.json()


def test_login_user():
    username = unique_username()

    create_response = create_user(username, PASSWORD)
    assert create_response.status_code == 200

    login_response = login_user(username, PASSWORD)

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"


def test_me_without_token_fails():
    response = httpx.get(f"{BASE_URL}/users/me")

    assert response.status_code == 401


def test_me_with_token():
    username = unique_username()

    create_response = create_user(username, PASSWORD)
    assert create_response.status_code == 200

    login_response = login_user(username, PASSWORD)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = httpx.get(
        f"{BASE_URL}/users/me",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert response.json()["username"] == username