from fastapi import APIRouter
router=APIRouter(prefix="/users",tags=["Users"])
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.schemas.schemas import UserCreate, UserResponse
from app.models.user import User
from sqlalchemy import select
from fastapi import HTTPException
from app.core.security import hash_password,get_current_user


@router.post("/", response_model=UserResponse)
async def create_user(user:UserCreate,db:AsyncSession=Depends(get_db)):
    db_user=User(username=user.username,hashed_password=hash_password(user.password))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
@router.get("/me",response_model=UserResponse)
async def get_me(current_user:User=Depends(get_current_user)):
    return current_user

@router.get("/{user_id}",response_model=UserResponse)
async def get_user(user_id:int, db:AsyncSession=Depends(get_db)):
    stmt=select(User).where(User.id ==user_id)
    result=await db.execute(stmt)
    user=result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user



