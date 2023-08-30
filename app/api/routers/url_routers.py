from fastapi import APIRouter, Depends, HTTPException
from app.api.connections.instace import get_db
from app.api.controllers.controller_url import UrlController
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager
from app.api.modules.tokens.token_init import jwt_auth
from sqlalchemy.orm import Session

router = APIRouter()
logger = ColoredLogger().get_logger()

"""
Module for URL-related routes.
"""


@router.post("/url/", response_model=dict)
@jwt_auth.token_required
def create_url(
    url_data: dict,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    """
    Create a new URL.

    Args:
        url_data (dict): Data to create the URL.
        redis_manager (RedisManager, optional): Redis manager instance. Defaults to using dependency.
        db (Session, optional): Database session. Defaults to using dependency.

    Returns:
        dict: Created URL information.

    Raises:
        HTTPException: If an error occurs during creation.
    """
    try:
        controller = UrlController(db, redis_manager)
        url = controller.create_url(url_data)
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/url/{url_id}", response_model=dict)
@jwt_auth.token_required
def read_url(
    url_id: int,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    """
    Get information about a URL by its ID.

    Args:
        url_id (int): ID of the URL to retrieve.
        redis_manager (RedisManager, optional): Redis manager instance. Defaults to using dependency.
        db (Session, optional): Database session. Defaults to using dependency.

    Returns:
        dict: URL information.

    Raises:
        HTTPException: If URL is not found or an error occurs during retrieval.
    """
    try:
        controller = UrlController(db, redis_manager)
        url = controller.read_url(url_id)
        return url
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/url/{url_id}", response_model=dict)
@jwt_auth.token_required
def update_url(
    url_id: int,
    url_data: dict,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    """
    Update information about a URL.

    Args:
        url_id (int): ID of the URL to update.
        url_data (dict): New data for the URL.
        redis_manager (RedisManager, optional): Redis manager instance. Defaults to using dependency.
        db (Session, optional): Database session. Defaults to using dependency.

    Returns:
        dict: Status message or updated URL information.

    Raises:
        HTTPException: If URL is not found or an error occurs during update.
    """
    try:
        controller = UrlController(db, redis_manager)
        updated = controller.update_url(url_id, url_data)
        if updated:
            return {"message": "URL updated successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/url/{url_id}", response_model=dict)
@jwt_auth.token_required
def delete_url(
    url_id: int,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    """
    Delete a URL by its ID.

    Args:
        url_id (int): ID of the URL to delete.
        redis_manager (RedisManager, optional): Redis manager instance. Defaults to using dependency.
        db (Session, optional): Database session. Defaults to using dependency.

    Returns:
        dict: Status message indicating success or failure.

    Raises:
        HTTPException: If URL is not found or an error occurs during deletion.
    """
    try:
        controller = UrlController(db, redis_manager)
        deleted = controller.delete_url(url_id)
        if deleted:
            return {"message": "URL deleted successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
