import httpx

from tests.helpers import (
    BASE_URL,
    PASSWORD,
    unique_username,
    create_user,
    get_token,
    auth_headers,
    make_user_admin,
)


def create_admin_user():
    username = unique_username("pytest_admin")

    create_response = create_user(username, PASSWORD)
    assert create_response.status_code == 200

    make_user_admin(username)

    token = get_token(username, PASSWORD)

    return username, token


def test_normal_user_cannot_create_book():
    username = unique_username()

    create_response = create_user(username, PASSWORD)
    assert create_response.status_code == 200

    token = get_token(username, PASSWORD)

    response = httpx.post(
        f"{BASE_URL}/books/",
        json={
            "title": "Normal User Book",
            "author": "Test Author",
            "published_year": 2024,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 403


def test_admin_can_create_book():
    username, token = create_admin_user()

    response = httpx.post(
        f"{BASE_URL}/books/",
        json={
            "title": "Admin Created Book",
            "author": "Admin Author",
            "published_year": 2024,
        },
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Admin Created Book"
    assert response.json()["available"] is True


def test_get_books_works():
    response = httpx.get(f"{BASE_URL}/books/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_books_pagination_limit_one():
    response = httpx.get(
        f"{BASE_URL}/books/?limit=1&offset=0"
    )

    assert response.status_code == 200

    books = response.json()

    assert isinstance(books, list)
    assert len(books) <= 1


def test_available_true_filter():
    response = httpx.get(
        f"{BASE_URL}/books/?available=true"
    )

    assert response.status_code == 200

    books = response.json()

    assert isinstance(books, list)

    for book in books:
        assert book["available"] is True