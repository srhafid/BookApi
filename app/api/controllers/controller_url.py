from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.api.modules.crud_postgresql.query_url import UrlDataRepository
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.connections.db import DBContext
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager

# Initialize the logger
logger = ColoredLogger().get_logger()

class UrlController:
    """
    Controller class for URL-related operations.
    """

    def __init__(self, db: DBContext, redis_manager: RedisManager):
        """
        Initializes an instance of UrlController.

        Args:
            db (DBContext): The database context.
            redis_manager (RedisManager): The Redis manager.
        """
        self.logger = logger
        self.db = db
        self.url_repo = UrlDataRepository(db)
        self.redis_repo = CrudRedis(redis=redis_manager)

    def create_url(self, url_data: dict):
        """
        Create a new URL.

        Args:
            url_data (dict): The URL data.

        Returns:
            dict: The created URL data.
        """
        try:
            url = self.url_repo.create_url(**url_data)
            self.redis_repo.store_url_in_redis(url.id, url_data)
            url_to_json = jsonable_encoder(url)
            return {"status": url_to_json}
        except Exception as e:
            self.logger.error("Error creating URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error creating URL")

    def read_url(self, url_id: int):
        """
        Read URL data by ID.

        Args:
            url_id (int): The ID of the URL.

        Returns:
            dict: The retrieved URL data.
        """
        try:
            url = self.url_repo.read_url(url_id)
            if url:
                result = self.redis_repo.get_url_from_redis(url.id)
                result_to_json = jsonable_encoder(result)
                return {"result": result_to_json}
            url_to_json = jsonable_encoder(url)
            return {"status": url_to_json}
        except Exception as e:
            self.logger.error("Error reading URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error reading URL")

    def update_url(self, url_id: int, new_data: dict):
        """
        Update URL data by ID.

        Args:
            url_id (int): The ID of the URL.
            new_data (dict): The updated URL data.

        Returns:
            bool: True if update was successful, False otherwise.
        """
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
        """
        Delete URL data by ID.

        Args:
            url_id (int): The ID of the URL.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            url_deleted = self.url_repo.delete_url(url_id)
            if url_deleted:
                self.redis_repo.delete_url_from_redis(url_id)
                return True
            return False
        except Exception as e:
            self.logger.error("Error deleting URL: %s", str(e))
            raise HTTPException(status_code=500, detail="Error deleting URL")
