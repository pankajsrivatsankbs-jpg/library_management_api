from fastapi import APIRouter
router=APIRouter(prefix="/auth",tags=["Auth"])
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models.user import User
from sqlalchemy import select
from fastapi import HTTPException
from app.core.security import verify_password,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    stmt=select(User).where(User.username ==form_data.username)
    result=await db.execute(stmt)
    user=result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401,detail="invalid credentials")
    if not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="invalid credentials")
    access_token=create_access_token(
        {"sub":str(user.id)}
    )
    return {"access_token":access_token,"token_type":"bearer"}
