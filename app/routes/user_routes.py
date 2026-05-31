from fastapi import APIRouter
router=APIRouter(prefix="/users",tags=["Users"])
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.schemas import UserCreate, UserResponse,BookCreate,BookResponse,BorrowCreate,BorrowResponse
from app.models.user import User
from app.models.book import Book
from app.models.borrow_record import BorrowRecord
from sqlalchemy import select
from fastapi import HTTPException
@router.post("/", response_model=UserResponse)
async def create_user(user:UserCreate,db:AsyncSession=Depends(get_db)):
    db_user=User(username=user.username,hashed_password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}",response_model=UserResponse)
async def get_user(user_id:int, db:AsyncSession=Depends(get_db)):
    stmt=select(User).where(User.id ==user_id)
    result=await db.execute(stmt)
    user=result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@router.post("/books",response_model=BookResponse)
async def create_book(book:BookCreate,db:AsyncSession=Depends(get_db)):
    new_book=Book(title=book.title, author=book.author,published_year=book.published_year)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@router.get("/books",response_model=list[BookResponse])
async def get_book(db:AsyncSession=Depends(get_db)):
    stmt=select(Book)
    result=await db.execute(stmt)
    books=result.scalars().all()
    return books

@router.post("/borrow",response_model=BorrowResponse)
async def borrow_book(borrow:BorrowCreate,db:AsyncSession=Depends(get_db)):
    user_stmt=select(User).where(User.id ==borrow.user_id)
    user_result=await db.execute(user_stmt)
    user=user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    book_stmt=select(Book).where(Book.id == borrow.book_id)
    book_result=await db.execute(book_stmt)
    book=book_result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    if not book.available:
        raise HTTPException(status_code=409, detail="book already borrowed")
    new_record=BorrowRecord(user_id=borrow.user_id, book_id=borrow.book_id)
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record