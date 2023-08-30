from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.api.connections.instace import get_db
from app.api.modules.logger_modify import ColoredLogger
from app.api.connections.db import DBContext
from app.api.modules.redis_conf.redis_conf import RedisManager
from app.api.controllers.controller_users import UserController
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis

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
def create_user(
    user_data: dict,
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
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
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
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
def update_user(
    user_id: int,
    new_data: dict,
    db: Session = Depends(get_db),
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
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a user by its ID.

    Args:
        user_id (int): ID of the user to delete.
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
