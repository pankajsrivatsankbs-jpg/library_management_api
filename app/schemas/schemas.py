from pydantic import BaseModel
from datetime import datetime
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role:str

    class Config:
        from_attributes=True

class BookCreate(BaseModel):
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

class BookUpdate(BaseModel):
    title: str | None = None
    author : str | None = None
    published_year : int | None = None 

class BorrowCreate(BaseModel):
    book_id:int

class BorrowResponse(BaseModel):
    id:int
    user_id:int
    book_id:int
    borrowed_at:datetime
    model_config={
        "from_attributes":True
    }

class ReturnCreate(BaseModel):
    book_id:int

class ReturnResponse(BaseModel):
    id:int
    user_id:int
    book_id:int
    borrowed_at:datetime
    returned_at:datetime | None
    model_config={"from_attributes":True}
    