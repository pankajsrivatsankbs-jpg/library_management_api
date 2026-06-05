from fastapi import FastAPI
from app.db.database import engine
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.book import Book
from app.models.user import User
from app.models.borrow_record import BorrowRecord
from app.routes.user_routes import router as user_router
from fastapi import FastAPI

from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.book_routes import router as book_router
from app.routes.borrow_routes import router as borrow_router
from app.routes.admin_routes import router as admin_router

app = FastAPI()


print(Base.metadata.tables.keys())

@asynccontextmanager
async def lifespan(app:FastAPI):
        yield

app=FastAPI(lifespan= lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(borrow_router)
app.include_router(admin_router)

for route in app.routes:
    print(route.path)