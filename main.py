from fastapi import FastAPI
from app.db.database import engine
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.book import Book
from app.models.user import User
from app.models.borrow_record import BorrowRecord
from app.routes.user_routes import router as user_router


print(Base.metadata.tables.keys())

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app=FastAPI(lifespan= lifespan)
app.include_router(user_router)
