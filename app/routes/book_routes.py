from fastapi import APIRouter
router=APIRouter(prefix="/books",tags=["Books"])
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.schemas import BookCreate,BookResponse,BookUpdate
from app.models.user import User
from app.models.book import Book
from sqlalchemy import select
from fastapi import HTTPException
from app.core.security import require_admin

@router.post("/",response_model=BookResponse)
async def create_book(book:BookCreate,current_admin:User=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    new_book=Book(title=book.title, author=book.author,published_year=book.published_year)
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@router.get("/",response_model=list[BookResponse])
async def get_book(db:AsyncSession=Depends(get_db)):
    stmt=select(Book)
    result=await db.execute(stmt)
    books=result.scalars().all()
    return books

@router.delete("/{book_id}")
async def delete_book(book_id:int, current_admin:User=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    stmt=select(Book).where(Book.id ==book_id)
    result=await db.execute(stmt)
    book=result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    await db.delete(book)
    await db.commit()
    return {"message":"book deleted successfully"}

@router.patch("/{book_id}",response_model=BookResponse)
async def update_book(book_id:int,book_update:BookUpdate,current_admin:User=Depends(require_admin) ,db:AsyncSession=Depends(get_db)):
    stmt=select(Book).where(Book.id ==book_id)
    result = await db.execute(stmt)
    book=result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    if book_update.title is not None:
        book.title = book_update.title
        
    if book_update.author is not None:
        book.author = book_update.author

    if book_update.published_year is not None:
        book.published_year= book_update.published_year

    await db.commit()
    await db.refresh(book)
    return book 