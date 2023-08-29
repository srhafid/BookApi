from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.api.connections.db import Base
class User(Base):
    """
    Class representing a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): User's username.
        password (str): User's password.
        role (str): User's role.
        urls (Relationship): Relationship with associated URLs for the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    role = Column(String(20))

    urls = relationship("Urls", back_populates="user")


class Urls(Base):
    """
    Class representing a URL in the database.

    Attributes:
        id (int): Unique identifier for the URL.
        title (str): URL's title.
        description (str): URL's description.
        author (str): URL's author.
        rating (int): URL's rating.
        user_id (int): ID of the user to whom the URL belongs.
        user (Relationship): Relationship with the user who owns the URL.
    """

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(500))
    author = Column(String(50))
    rating = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="urls")
