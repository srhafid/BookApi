from app.api.models.model import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres@localhost/urluser"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBContext:
    def __init__(self) -> None:
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self):
        self.db.close()
