from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False
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