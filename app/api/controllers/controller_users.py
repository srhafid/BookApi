from fastapi import HTTPException
from app.api.modules.crud_postgresql.query_url import UrlDataRepository
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.modules.logger_modify import ColoredLogger
from app.api.connections.db import DBContext
from app.api.modules.redis_conf.redis_conf import RedisManager


class UrlController:
    def __init__(
        self, logger: ColoredLogger, db: DBContext, redis_manager: RedisManager
    ):
        self.logger = logger.get_logger()
        self.db = db
        self.url_repo = UrlDataRepository(db, logger)
        self.redis_repo = CrudRedis(redis_manager)

    def create_url(self, url_data: dict):
        try:
            url = self.url_repo.create_url(**url_data)
            self.redis_repo.store_url_in_redis(url.id, url_data)
            return url
        except Exception as e:
            self.logger.error("Error creating URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error creating URL")

    def read_url(self, url_id: int):
        try:
            url = self.url_repo.read_url(url_id)
            return url
        except Exception as e:
            self.logger.error("Error reading URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error reading URL")

    def update_url(self, url_id: int, new_data: dict):
        try:
            url_updated = self.url_repo.update_url(url_id, new_data)
            if url_updated:
                self.redis_repo.update_url_in_redis(url_id, new_data)
                return True
            return False
        except Exception as e:
            self.logger.error("Error updating URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error updating URL")

    def delete_url(self, url_id: int):
        try:
            url_deleted = self.url_repo.delete_url(url_id)
            if url_deleted:
                self.redis_repo.delete_url_from_redis(url_id)
                return True
            return False
        except Exception as e:
            self.logger.error("Error deleting URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error deleting URL")



