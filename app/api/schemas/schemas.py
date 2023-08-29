from pydantic import BaseModel

class UrlCreate(BaseModel):
    title: str
    description: str
    author: str
    rating: int

class UserLogin(BaseModel):
    username: str
    password: str
