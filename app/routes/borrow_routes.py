from fastapi import APIRouter
router=APIRouter(prefix="/borrow",tags=["Borrow"])
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.schemas import BorrowCreate,BorrowResponse,ReturnCreate,ReturnResponse
from app.models.user import User
from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from sqlalchemy import select
from fastapi import HTTPException
from app.core.security import get_current_user
from datetime import datetime

@router.post("/",response_model=BorrowResponse)
async def borrow_book(borrow:BorrowCreate,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    book_stmt=select(Book).where(Book.id ==borrow.book_id)
    result_stmt= await db.execute(book_stmt)
    book=result_stmt.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404,detail="book does not exist")
    if not book.available:
        raise HTTPException(status_code=409,detail="book is not available")
    new_record=BorrowRecord(user_id=current_user.id, book_id=borrow.book_id)
    book.available=False
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record

@router.post("/return",response_model=ReturnResponse)
async def return_book(return_data:ReturnCreate,current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    record_stmt=select(BorrowRecord).where(
        BorrowRecord.user_id == current_user.id,
        BorrowRecord.book_id == return_data.book_id,
        BorrowRecord.returned_at.is_(None)
    )
    record_result=await db.execute(record_stmt)
    borrow_record=record_result.scalar_one_or_none()
    if borrow_record is None:
        raise HTTPException(status_code=404,detail="active borrow record not found")
    book_stmt=select(Book).where(Book.id ==return_data.book_id)
    book_result=await db.execute(book_stmt)
    book=book_result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    borrow_record.returned_at=datetime.utcnow()
    book.available = True
    await db.commit()
    await db.refresh(borrow_record)
    return borrow_record

@router.get("/my-books",response_model=list[BorrowResponse])
async def get_my_borrows(current_user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    stmt=select(BorrowRecord).where(BorrowRecord.user_id == current_user.id,BorrowRecord.returned_at.is_(None))
    result=await db.execute(stmt)
    record=result.scalars().all()
    return record
