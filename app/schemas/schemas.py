from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=72)

class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    published_year: int = Field(ge=0, le=2100)

class UserResponse(BaseModel):
    id: int
    username: str
    role:str

    class Config:
        from_attributes=True

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    published_year: int
    available: bool

    model_config = ConfigDict(from_attributes=True)

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
    