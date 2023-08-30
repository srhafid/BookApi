from fastapi import APIRouter, Depends, Form, HTTPException, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.connections.instace import get_db
from app.api.models.model import User
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager
from app.api.controllers.controller_users import UserController
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.modules.tokens.access_token import get_current_user, auth_required, auth

router = APIRouter()
logger = ColoredLogger().get_logger()

"""
Module for user-related routes.
"""


def get_redis_manager(redis: RedisManager = Depends(RedisManager)):
    """
    Get a Redis manager instance using dependency injection.

    Args:
        redis (RedisManager, optional): Redis manager instance. Defaults to using dependency.

    Returns:
        CrudRedis: Redis manager instance.
    """
    return CrudRedis(redis)


@router.post("/user/", response_model=dict)
@auth_required
def create_user(
    user_data: dict = Form(...),
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new user.

    Args:
        user_data (dict): Data to create the user.
        db (Session, optional): Database session. Defaults to using dependency.
        redis_manager (CrudRedis, optional): Redis manager instance. Defaults to using dependency.

    Returns:
        dict: Created user information.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        controller = UserController(db, redis_manager)
        return controller.create_user(user_data)
    except Exception as e:
        logger.error("Error creating user: %s", str(e))
        raise HTTPException(status_code=500, detail="Error creating user")


@router.get("/user/{user_id}", response_model=dict)
@auth_required
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
    current_user: dict = Depends(get_current_user),
):
    """
    Get information about a user by its ID.

    Args:
        user_id (int): ID of the user to retrieve.
        db (Session, optional): Database session. Defaults to using dependency.
        redis_manager (CrudRedis, optional): Redis manager instance. Defaults to using dependency.

    Returns:
        dict: User information.

    Raises:
        HTTPException: If user is not found or an error occurs during retrieval.
    """
    try:
        controller = UserController(db, redis_manager)
        return controller.read_user(user_id)
    except Exception as e:
        logger.error("Error reading user: %s", str(e))
        raise HTTPException(status_code=500, detail="Error reading user")


@router.put("/user/{user_id}", response_model=bool)
@auth_required
def update_user(
    user_id: int,
    new_data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update information about a user.

    Args:
        user_id (int): ID of the user to update.
        new_data (dict): New data for the user.
        db (Session, optional): Database session. Defaults to using dependency.

    Returns:
        bool: True if user is updated successfully, False otherwise.

    Raises:
        HTTPException: If user is not found or an error occurs during update.
    """
    try:
        controller = UserController(db, get_redis_manager())
        return controller.update_user(user_id, new_data)
    except Exception as e:
        logger.error("Error updating user: %s", str(e))
        raise HTTPException(status_code=500, detail="Error updating user")


@router.delete("/user/{user_id}", response_model=bool)
@auth_required
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a user by its ID.

    Args:
        user_id (int): ID of the user to delete.
        current_user (dict): Decoded JWT payload of the current user.
        db (Session, optional): Database session. Defaults to using dependency.

    Returns:
        bool: True if user is deleted successfully, False otherwise.

    Raises:
        HTTPException: If user is not found or an error occurs during deletion.
    """
    try:
        controller = UserController(db, get_redis_manager())
        return controller.delete_user(user_id)
    except Exception as e:
        logger.error("Error deleting user: %s", str(e))
        raise HTTPException(status_code=500, detail="Error deleting user")


@router.post("/login")
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user is None or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}
