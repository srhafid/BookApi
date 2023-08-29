from fastapi import APIRouter, Depends, HTTPException
from app.api.connections.instace import get_db
from app.api.controllers.controller_url import UrlController
from app.api.connections.db import DBContext
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager
from sqlalchemy.orm import Session

router = APIRouter()
logger = ColoredLogger().get_logger()


def get_redis_manager(redis: RedisManager = Depends(RedisManager)):
    return CrudRedis(redis)


@router.post("/url/")
def create_url(
    url_data: dict,
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
):
    try:
        controller = UrlController(db, redis_manager)
        url = controller.create_url(url_data)
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/url/{url_id}")
def read_url(
    url_id: int,
    db: Session = Depends(get_db),
    redis_manager: CrudRedis = Depends(get_redis_manager),
):
    try:
        controller = UrlController(db, redis_manager)
        url = controller.read_url(url_id)
        return url
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/url/{url_id}")
def update_url(
    url_id: int,
    url_data: dict,
    db: Session = Depends(get_db),
):
    try:
        controller = UrlController(db, get_redis_manager())
        updated = controller.update_url(url_id, url_data)
        if updated:
            return {"message": "URL updated successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/url/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
):
    try:
        controller = UrlController(db, get_redis_manager())
        deleted = controller.delete_url(url_id)
        if deleted:
            return {"message": "URL deleted successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
