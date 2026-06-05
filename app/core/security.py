from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)-> str:
    return pwd_context.hash(password)

def verify_password(entered_password:str,stored_hash:str)->bool:
    return pwd_context.verify(entered_password,stored_hash)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"]=expire
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")#it returns the value of the "sub claim in string format"

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    stmt = select(User).where(
        User.id == int(user_id)
    )

    result = await db.execute(stmt)

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

    return user

def require_admin(current_user:User=Depends(get_current_user)):
    if current_user.role !="admin":
        raise HTTPException(status_code=403,detail="admin access required")
    return current_user
