from fastapi import APIRouter, Depends
from app.api.crud import create_user
from app.api.schemas.schemas import UserCreate, User
from app.api.crud import database

router = APIRouter()


@router.post("/books/", response_model=User)
def create_user_register(
    user: UserCreate,
    db: database.Session = Depends(database.get_db),
):
    return create_user(db, user)
