import uuid
import httpx
import psycopg2

BASE_URL = "http://localhost:8000"
PASSWORD = "pytestpass123"

SYNC_DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/library_db1"


def unique_username(prefix: str = "pytest_user"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def create_user(username: str, password: str = PASSWORD):
    return httpx.post(
        f"{BASE_URL}/users/",
        json={
            "username": username,
            "password": password,
        },
    )


def login_user(username: str, password: str = PASSWORD):
    return httpx.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )


def get_token(username: str, password: str = PASSWORD):
    response = login_user(username, password)

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }


def make_user_admin(username: str):
    with psycopg2.connect(SYNC_DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET role = 'admin'
                WHERE username = %s
                """,
                (username,),
            )
