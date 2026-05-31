from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)
class Base(DeclarativeBase):
    pass

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)



async def get_db():

    async with AsyncSessionLocal() as session:
        yield session