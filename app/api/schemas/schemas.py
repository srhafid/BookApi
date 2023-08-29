from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class User(UserCreate):
    id: int

class BookCreate(BaseModel):
    title: str
    author: str

class Book(BookCreate):
    id: int
    rating: int
    user_id: int