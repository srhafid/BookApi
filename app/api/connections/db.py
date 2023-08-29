from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://postgres@localhost/urluser"  # URL of the database
engine = create_engine(DATABASE_URL)  # Create database engine
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # Create local session
Base = declarative_base()  # Create declarative base

class DBContext:
    def __init__(self) -> None:
        self.db = SessionLocal()  # Initialize database session

    def __enter__(self):
        return self.db  # Return the session upon entering the context

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()  # Close the session upon exiting the context
