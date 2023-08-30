import pytest
from app.api.models.model import User, Urls


@pytest.fixture
def db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.api.connections.db import Base

    engine = create_engine("postgresql://postgres@localhost/urluser")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_create_user(db):
    user_data = {"username": "testuser", "password": "testpassword", "role": "user"}
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == user_data["username"]
    assert user.password == user_data["password"]
    assert user.role == user_data["role"]


def test_create_url(db):
    user_data = {"username": "testuser", "password": "testpassword", "role": "user"}
    user = User(**user_data)
    db.add(user)
    db.commit()

    url_data = {
        "title": "Test URL",
        "description": "This is a test URL",
        "author": "Test Author",
        "rating": 5,
        "user_id": user.id,
    }
    url = Urls(**url_data)
    db.add(url)
    db.commit()
    db.refresh(url)

    assert url.id is not None
    assert url.title == url_data["title"]
    assert url.description == url_data["description"]
    assert url.author == url_data["author"]
    assert url.rating == url_data["rating"]
    assert url.user_id == user.id
