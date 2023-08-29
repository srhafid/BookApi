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


def get_redis_manager(redis: RedisManager = Depends(RedisManager)):
    return CrudRedis(redis)


@router.post("/user/", response_model=dict)
def create_user(
    user_data: dict,
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
):
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
    try:
        controller = UserController(db, get_redis_manager())
        return controller.delete_user(user_id)
    except Exception as e:
        logger.error("Error deleting user: %s", str(e))
        raise HTTPException(status_code=500, detail="Error deleting user")
