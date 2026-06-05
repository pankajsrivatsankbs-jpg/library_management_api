from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Book(Base):
    __tablename__ = "books"
    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    published_year:Mapped[int]
    available: Mapped[bool]=mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)