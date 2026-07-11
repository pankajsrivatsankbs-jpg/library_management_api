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

    response = create_user(username, PASSWORD)
    assert response.status_code == 200

    make_user_admin(username)

    token = get_token(username, PASSWORD)

    return username, token


def create_normal_user():
    username = unique_username()

    response = create_user(username, PASSWORD)
    assert response.status_code == 200

    token = get_token(username, PASSWORD)

    return username, token


def create_book(admin_token):
    response = httpx.post(
        f"{BASE_URL}/books/",
        json={
            "title": "Borrow Test Book",
            "author": "Pytest",
            "published_year": 2024,
        },
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200

    return response.json()["id"]


def test_user_can_borrow_book():
    _, admin_token = create_admin_user()

    book_id = create_book(admin_token)

    _, user_token = create_normal_user()

    response = httpx.post(
        f"{BASE_URL}/borrow/",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert response.status_code == 200
    assert response.json()["book_id"] == book_id


def test_book_becomes_unavailable_after_borrow():
    _, admin_token = create_admin_user()

    book_id = create_book(admin_token)

    _, user_token = create_normal_user()

    borrow = httpx.post(
        f"{BASE_URL}/borrow/",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert borrow.status_code == 200

    second_user, second_token = create_normal_user()

    second = httpx.post(
        f"{BASE_URL}/borrow/",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(second_token),
    )

    assert second.status_code == 409


def test_user_can_return_book():
    _, admin_token = create_admin_user()

    book_id = create_book(admin_token)

    _, user_token = create_normal_user()

    borrow = httpx.post(
        f"{BASE_URL}/borrow/",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert borrow.status_code == 200

    response = httpx.post(
        f"{BASE_URL}/borrow/return",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert response.status_code == 200
    assert response.json()["book_id"] == book_id
    assert response.json()["returned_at"] is not None


def test_return_without_borrowing_fails():
    _, admin_token = create_admin_user()

    book_id = create_book(admin_token)

    _, user_token = create_normal_user()

    response = httpx.post(
        f"{BASE_URL}/borrow/return",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert response.status_code == 404


def test_get_my_borrowed_books():
    _, admin_token = create_admin_user()

    book_id = create_book(admin_token)

    _, user_token = create_normal_user()

    borrow = httpx.post(
        f"{BASE_URL}/borrow/",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert borrow.status_code == 200

    response = httpx.get(
        f"{BASE_URL}/borrow/my-books",
        headers=auth_headers(user_token),
    )

    assert response.status_code == 200

    records = response.json()

    assert isinstance(records, list)
    assert any(record["book_id"] == book_id for record in records)


def test_returned_book_not_in_my_books():
    _, admin_token = create_admin_user()

    book_id = create_book(admin_token)

    _, user_token = create_normal_user()

    borrow = httpx.post(
        f"{BASE_URL}/borrow/",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert borrow.status_code == 200

    returned = httpx.post(
        f"{BASE_URL}/borrow/return",
        json={
            "book_id": book_id,
        },
        headers=auth_headers(user_token),
    )

    assert returned.status_code == 200

    response = httpx.get(
        f"{BASE_URL}/borrow/my-books",
        headers=auth_headers(user_token),
    )

    assert response.status_code == 200

    records = response.json()

    assert all(record["book_id"] != book_id for record in records)
