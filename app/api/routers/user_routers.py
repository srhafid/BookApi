from fastapi import APIRouter, Depends
from app.api.modules.logger_modify import ColoredLogger
from app.api.connections.db import DBContext
from app.api.modules.redis_conf.redis_conf import RedisManager
from app.api.controllers.user_controller import UserController
from app.api.dependencies import get_logger, get_db, get_redis_manager

router = APIRouter()


@router.post("/users/", response_model=dict)
async def create_user(
    user_data: dict,
    logger: ColoredLogger = Depends(get_logger),
    db: DBContext = Depends(get_db),
    redis_manager: RedisManager = Depends(get_redis_manager),
):
    controller = UserController(logger, db, redis_manager)
    return controller.create_user(user_data)


@router.get("/users/{user_id}", response_model=dict)
async def read_user(
    user_id: int,
    logger: ColoredLogger = Depends(get_logger),
    db: DBContext = Depends(get_db),
    redis_manager: RedisManager = Depends(get_redis_manager),
):
    controller = UserController(logger, db, redis_manager)
    return controller.read_user(user_id)


@router.put("/users/{user_id}", response_model=bool)
async def update_user(
    user_id: int, new_data: dict, logger: ColoredLogger = Depends(get_logger), db: DBContext = Depends(get_db)
):
    controller = UserController(logger, db, redis_manager)
    return controller.update_user(user_id, new_data)


@router.delete("/users/{user_id}", response_model=bool)
async def delete_user(
    user_id: int, logger: ColoredLogger = Depends(get_logger), db: DBContext = Depends(get_db)
):
    controller = UserController(logger, db, redis_manager)
    return controller.delete_user(user_id)
