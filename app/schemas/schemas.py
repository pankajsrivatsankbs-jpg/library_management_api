from pydantic import BaseModel
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes=True

class BookCreate(BaseModel):
    id:int
    title:str
    author:str
    available:bool
    published_year:int

class BookResponse(BaseModel):
    title:str
    author:str
    published_year:int

    class Config:
        from_attributes=True

class BorrowCreate(BaseModel):
    user_id:int
    book_id:int

class BorrowResponse(BaseModel):
    id:int
    user_id:int
    book_id:int
    borrowed_at:datetime
    model_config={
        "from_attributes":True
    }