from sqlalchemy.exc import SQLAlchemyError
from app.api.models.model import Urls
from app.api.connections.db import DBContext
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager
from app.api.repositories.url_data_repository import UrlDataRepository
from app.api.repositories.redis_crud import CrudRedis


class UrlsController:
    def __init__(self, db: DBContext, logger: ColoredLogger):
        self.db = db
        self.logger = logger.get_logger()
        self.redis_manager = RedisManager()
        self.url_data_repo = UrlDataRepository(db, logger)
        self.redis_crud = CrudRedis(self.redis_manager)

    def create_url(self, url_data: dict):
        try:
            url = self.url_data_repo.create_url(**url_data)
            self.redis_crud.store_url_in_redis(url.id, url_data)
            return url
        except SQLAlchemyError as e:
            raise e

    def read_url(self, url_id: int):
        try:
            url = self.url_data_repo.read_url(url_id)
            return url
        except ValueError:
            raise ValueError("URL not found")
        except SQLAlchemyError as e:
            raise e

    def update_url(self, url_id: int, url_data: dict):
        try:
            url = self.url_data_repo.read_url(url_id)
            if not url:
                raise ValueError("URL not found")
            updated = self.url_data_repo.update_url(url_id, url_data)
            if updated:
                self.redis_crud.update_url_in_redis(url_id, url_data)
                return True
            return False
        except SQLAlchemyError as e:
            raise e

    def delete_url(self, url_id: int):
        try:
            url = self.url_data_repo.read_url(url_id)
            if not url:
                raise ValueError("URL not found")
            deleted = self.url_data_repo.delete_url(url_id)
            if deleted:
                self.redis_crud.delete_url_from_redis(url_id)
                return True
            return False
        except SQLAlchemyError as e:
            raise e
