from sqlalchemy.orm import Session
from app.api.connections.db import DBContext


def get_db() -> Session:
    with DBContext() as db:
        yield db
