# Library Backend API

A Dockerized backend API built with FastAPI, PostgreSQL, Async SQLAlchemy, Alembic migrations, JWT authentication, role-based authorization, and Docker Compose.

This project simulates a library management backend where users can register, log in, borrow books, return books, and admins can manage the book catalog.

## Features

* User registration
* Password hashing with bcrypt
* JWT-based authentication
* OAuth2 password login flow
* Protected routes using current-user dependency
* Role-based authorization
* Admin-only book creation
* Admin-only book update
* Admin-only book deletion
* Borrow book flow
* Return book flow
* View current user profile
* View current user's active borrowed books
* Admin view of all borrow records
* Book pagination with `limit` and `offset`
* Book filtering by availability
* PostgreSQL database
* Async SQLAlchemy ORM
* Alembic database migrations
* Dockerized FastAPI and PostgreSQL setup

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy Async ORM
* AsyncPG
* Alembic
* Pydantic
* JWT
* Passlib
* bcrypt
* Docker
* Docker Compose
* Uvicorn
* pytest

## Project Structure

```txt
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

main.py
Dockerfile
docker-compose.yml
requirements.txt
.env.example
```

## Authentication Flow

```txt
User registers
↓
Password is hashed with bcrypt
↓
User is saved in PostgreSQL
↓
User logs in
↓
Password is verified
↓
JWT access token is created
↓
Client sends token in Authorization header
↓
Protected routes use get_current_user()
```

## Authorization Flow

Authentication answers:

```txt
Who are you?
```

Authorization answers:

```txt
What are you allowed to do?
```

Normal users can:

* View books
* Borrow books
* Return books
* View their own profile
* View their own active borrow records

Admin users can:

* Create books
* Update books
* Delete books
* View all borrow records

## API Endpoints

### Auth

| Method | Endpoint      | Description                        |
| ------ | ------------- | ---------------------------------- |
| POST   | `/auth/login` | Login and receive JWT access token |

### Users

| Method | Endpoint           | Description                |
| ------ | ------------------ | -------------------------- |
| POST   | `/users/`          | Register a new user        |
| GET    | `/users/me`        | Get current logged-in user |
| GET    | `/users/{user_id}` | Get user by ID             |

### Books

| Method | Endpoint           | Description                                        |
| ------ | ------------------ | -------------------------------------------------- |
| GET    | `/books/`          | List books with pagination and availability filter |
| POST   | `/books/`          | Create a book, admin only                          |
| PATCH  | `/books/{book_id}` | Update a book, admin only                          |
| DELETE | `/books/{book_id}` | Delete a book, admin only                          |

### Borrow

| Method | Endpoint           | Description                               |
| ------ | ------------------ | ----------------------------------------- |
| POST   | `/borrow/`         | Borrow a book                             |
| POST   | `/borrow/return`   | Return a borrowed book                    |
| GET    | `/borrow/my-books` | View current user's active borrowed books |

### Admin

| Method | Endpoint         | Description                         |
| ------ | ---------------- | ----------------------------------- |
| GET    | `/admin/borrows` | View all borrow records, admin only |

## Book Filtering and Pagination

List books:

```txt
GET /books/
```

Filter available books:

```txt
GET /books/?available=true
```

Filter unavailable books:

```txt
GET /books/?available=false
```

Use pagination:

```txt
GET /books/?limit=10&offset=0
```

Parameters:

| Parameter   | Description                                   |
| ----------- | --------------------------------------------- |
| `available` | Optional boolean filter for book availability |
| `limit`     | Number of books to return                     |
| `offset`    | Number of books to skip                       |

## Running With Docker

Build and start the containers:

```bash
docker compose up --build
```

Run Alembic migrations inside the API container:

```bash
docker compose exec api alembic upgrade head
```

Open Swagger UI:

```txt
http://localhost:8000/docs
```

Stop containers:

```bash
docker compose down
```

Stop containers and delete database volume:

```bash
docker compose down -v
```

Use `down -v` carefully because it deletes the PostgreSQL Docker volume.

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@db:5432/library_db1
SECRET_KEY=replace_with_your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Do not commit the real `.env` file.

## Alembic Migration Commands

Create a new migration:

```bash
docker compose exec api alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
docker compose exec api alembic upgrade head
```

Check current migration:

```bash
docker compose exec api alembic current
```

## Making a User Admin

Enter the PostgreSQL container:

```bash
docker compose exec db psql -U postgres -d library_db1
```

Update user role:

```sql
UPDATE users
SET role = 'admin'
WHERE username = 'pankaj';

SELECT id, username, role
FROM users;
```

Exit psql:

```sql
\q
```

After changing the role, log in again and authorize with a fresh token.

## Common Docker Commands

Start project:

```bash
docker compose up --build
```

Stop project:

```bash
docker compose down
```

Rebuild without cache:

```bash
docker compose build --no-cache
```

View API logs:

```bash
docker compose logs api --tail=100
```

Enter database:

```bash
docker compose exec db psql -U postgres -d library_db1
```

Run migrations:

```bash
docker compose exec api alembic upgrade head
```

## Development Notes

This project was built to practice:

* FastAPI route architecture
* Request validation with Pydantic
* Async SQLAlchemy sessions
* PostgreSQL relationships
* JWT authentication
* Role-based authorization
* Business logic for borrow/return flows
* Alembic migrations
* Docker Compose development
* Debugging real backend integration issues

## Future Improvements

* Add Pytest test suite
* Add refresh tokens
* Add duplicate username handling with `409 Conflict`
* Add soft delete for books
* Add admin user management
* Add CI/CD pipeline
* Deploy to Render, Railway, or a VPS
