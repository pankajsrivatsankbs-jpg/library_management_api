from fastapi import APIRouter
router=APIRouter(prefix="/admin",tags=["Admin"])
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.schemas import BorrowResponse
from app.models.user import User
from app.models.borrow_record import BorrowRecord
from sqlalchemy import select
from app.core.security import require_admin

@router.get("/borrows",response_model=list[BorrowResponse])
async def get_all_borrows(current_user:User=Depends(require_admin),db:AsyncSession=Depends(get_db)):
    stmt=select(BorrowRecord)
    result=await db.execute(stmt)
    records=result.scalars().all()
    return records