from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class User(UserCreate):
    id: int

class UrlCreate(BaseModel):
    title: str
    author: str
    file: bytes

class Url(UrlCreate):
    id: int
    rating: int
    user_id: int