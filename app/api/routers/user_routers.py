from fastapi import APIRouter, Depends
from . import crud, schemas, database

router = APIRouter()

@router.post("/books/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: database.Session = Depends(database.get_db)):
    return crud.create_user(db, user)
