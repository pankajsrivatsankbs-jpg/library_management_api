# Library Backend API

A RESTful Library Management API built with FastAPI, PostgreSQL, Async SQLAlchemy, Alembic, JWT authentication, role-based authorization, and Docker Compose.

This project implements a library management backend where users can register, authenticate, borrow books, return books, and administrators manage the book catalog.

---

# Features

- User registration
- Password hashing with bcrypt
- JWT-based authentication
- OAuth2 password login flow
- Protected routes using dependency injection
- Role-based authorization
- Admin-only book management (Create, Update, Delete)
- Borrow and return books
- View current user profile
- View current user's active borrowed books
- Admin view of all borrow records
- Book pagination using `limit` and `offset`
- Book availability filtering
- PostgreSQL database
- Async SQLAlchemy ORM
- Alembic database migrations
- Dockerized FastAPI and PostgreSQL setup

---

# Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- AsyncPG
- Alembic
- Pydantic
- JWT
- Passlib
- bcrypt
- Docker
- Docker Compose
- Uvicorn
- Pytest

---

# Project Structure

```text
app/
├── core/
│   ├── config.py
│   └── security.py
│
├── db/
│   └── database.py
│
├── models/
│   ├── user.py
│   ├── book.py
│   └── borrow_record.py
│
├── routes/
│   ├── auth_routes.py
│   ├── user_routes.py
│   ├── book_routes.py
│   ├── borrow_routes.py
│   └── admin_routes.py
│
├── schemas/
│   └── schemas.py
│
└── dependencies.py

alembic/
├── env.py
└── versions/

tests/

main.py
Dockerfile
docker-compose.yml
requirements.txt
.env.example
README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/pankajsrivatsankbs-jpg/library_management_api.git
cd library_management_api
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@db:5432/library_db1
SECRET_KEY=replace_with_your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Never commit your real `.env` file.

---

# Running with Docker

Build and start the application

```bash
docker compose up --build
```

Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

Open Swagger UI

```
http://localhost:8000/docs
```

Stop containers

```bash
docker compose down
```

Remove containers and database volume

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` permanently deletes the PostgreSQL Docker volume and all stored data.

---

# Running Without Docker

Apply migrations

```bash
alembic upgrade head
```

Start the API

```bash
uvicorn main:app --reload
```

Open Swagger

```
http://127.0.0.1:8000/docs
```

---

# Running Tests

```bash
pytest
```

---

# Authentication Flow

```text
User registers
        │
        ▼
Password is hashed with bcrypt
        │
        ▼
User is stored in PostgreSQL
        │
        ▼
User logs in
        │
        ▼
Password is verified
        │
        ▼
JWT access token is generated
        │
        ▼
Client sends Authorization: Bearer <token>
        │
        ▼
Protected routes use get_current_user()
```

---

# Authorization

Authentication answers:

```
Who are you?
```

Authorization answers:

```
What are you allowed to do?
```

### User Permissions

- View books
- Borrow books
- Return books
- View their own profile
- View their own borrowed books

### Admin Permissions

- Create books
- Update books
- Delete books
- View all borrow records

---

# API Endpoints

## Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/auth/login` | Login and receive JWT token |

---

## Users

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/users/` | Register user |
| GET | `/users/me` | Current authenticated user |
| GET | `/users/{user_id}` | Get user by ID |

---

## Books

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/books/` | List books with pagination and filtering |
| POST | `/books/` | Create book (Admin) |
| PATCH | `/books/{book_id}` | Update book (Admin) |
| DELETE | `/books/{book_id}` | Delete book (Admin) |

---

## Borrow

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/borrow/` | Borrow a book |
| POST | `/borrow/return` | Return a book |
| GET | `/borrow/my-books` | Current user's active borrowed books |

---

## Admin

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/admin/borrows` | View all borrow records |

---

# Pagination and Filtering

List all books

```
GET /books/
```

Available books

```
GET /books/?available=true
```

Unavailable books

```
GET /books/?available=false
```

Pagination

```
GET /books/?limit=10&offset=0
```

| Parameter | Description |
|-----------|-------------|
| available | Optional availability filter |
| limit | Maximum books returned |
| offset | Number of books skipped |

---

# Alembic Commands

Create migration

```bash
docker compose exec api alembic revision --autogenerate -m "migration message"
```

Apply migrations

```bash
docker compose exec api alembic upgrade head
```

Current migration

```bash
docker compose exec api alembic current
```

---

# Making a User an Admin

Enter PostgreSQL

```bash
docker compose exec db psql -U postgres -d library_db1
```

Grant admin role

```sql
UPDATE users
SET role = 'admin'
WHERE username = 'pankaj';
```

Verify

```sql
SELECT id, username, role
FROM users;
```

Exit

```sql
\q
```

Log in again to receive a JWT containing the updated role.

---

# Common Docker Commands

Start

```bash
docker compose up --build
```

Stop

```bash
docker compose down
```

Rebuild

```bash
docker compose build --no-cache
```

View API logs

```bash
docker compose logs api --tail=100
```

Enter PostgreSQL

```bash
docker compose exec db psql -U postgres -d library_db1
```

Run migrations

```bash
docker compose exec api alembic upgrade head
```

---

# Development Notes

This project was built to strengthen practical backend development skills, including:

- FastAPI application architecture
- Dependency Injection
- Request validation with Pydantic
- Async SQLAlchemy
- PostgreSQL integration
- JWT authentication
- Role-based authorization
- Business logic implementation
- Alembic migrations
- Docker Compose workflows
- Backend testing with Pytest
- Debugging real-world integration issues
