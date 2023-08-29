from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.alembic import crud, models, schemas, database

# register routers imports
from app.api.routers.book_routers import router as book_routes
from app.api.routers.user_routers import router as user_routes


# init object fastapi
app = FastAPI()

# init database
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# register routers
app.include_router(user_routes, prefix="/users", tags=["users"])
app.include_router(book_routes, prefix="/books", tags=["books"])
