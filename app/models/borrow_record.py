from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class BorrowRecord(Base):
    __tablename__ = "borrow_records"
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id : Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrowed_at: Mapped[datetime]= mapped_column(default=datetime.utcnow)
    returned_at: Mapped[datetime | None]=mapped_column(nullable = True)

