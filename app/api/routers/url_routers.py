from fastapi import APIRouter, Depends, HTTPException
from app.api.connections.instace import get_db
from app.api.controllers.controller_url import UrlController
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager
from sqlalchemy.orm import Session

router = APIRouter()
logger = ColoredLogger().get_logger()


@router.post("/url/", response_model=dict)
def create_url(
    url_data: dict,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    try:
        controller = UrlController(db, redis_manager)
        url = controller.create_url(url_data)
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/url/{url_id}", response_model=dict)
def read_url(
    url_id: int,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    try:
        controller = UrlController(db, redis_manager)
        url = controller.read_url(url_id)
        return url
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/url/{url_id}", response_model=dict)
def update_url(
    url_id: int,
    url_data: dict,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    try:
        controller = UrlController(db, redis_manager)
        updated = controller.update_url(url_id, url_data)
        if updated:
            return {"message": "URL updated successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/url/{url_id}", response_model=dict)
def delete_url(
    url_id: int,
    redis_manager: RedisManager = Depends(RedisManager),
    db: Session = Depends(get_db),
):
    try:
        controller = UrlController(db, redis_manager)
        deleted = controller.delete_url(url_id)
        if deleted:
            return {"message": "URL deleted successfully"}
        raise HTTPException(status_code=404, detail="URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
