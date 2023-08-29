from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager
from redis import RedisError
from json import dumps as json_dumps
from json import loads as json_loads

logger = ColoredLogger().get_logger()


class CrudRedis:
    """
    Provides methods for CRUD operations using Redis as a data store.

    This class encapsulates the operations to store, retrieve, update, and delete data in Redis.
    """

    def __init__(
        self,
        redis: RedisManager
    ) -> None:
        """
        Initializes a new instance of CrudRedis.

        Args:
            redis (RedisManager): The Redis manager to use for Redis operations.
        """
        self.logger = logger
        self.redis_manager = redis

    def store_url_in_redis(self, url_id: int, url_data: dict):
        """
        Store URL data in Redis.

        Args:
            url_id (int): The ID of the URL.
            url_data (dict): The data to store in Redis.

        Raises:
            RedisError: If an error occurs while storing URL data in Redis.
        """
        try:
            key = f"url_data:{url_id}"
            value = json_dumps(url_data)
            self.redis_manager.get_client().set(key, value)
        except RedisError as e:
            self.logger.error("Error storing URL data in Redis: %s", str(e))
            raise e

    def get_url_from_redis(self, url_id: int) -> dict:
        """
        Retrieve URL data from Redis.

        Args:
            url_id (int): The ID of the URL.

        Returns:
            dict: The retrieved URL data, or None if not found.
        """
        key = f"url_data:{url_id}"
        value = self.redis_manager.get_client().get(key)
        if value:
            return json_loads(value)
        return None

    def update_url_in_redis(self, url_id: int, new_data: dict):
        """
        Update URL data in Redis.

        Args:
            url_id (int): The ID of the URL.
            new_data (dict): The new data to update in Redis.

        Raises:
            RedisError: If an error occurs while updating URL data in Redis.
        """
        try:
            key = f"url_data:{url_id}"
            value = json_dumps(new_data)
            self.redis_manager.get_client().set(key, value)
        except RedisError as e:
            self.logger.error("Error updating URL data in Redis: %s", str(e))
            raise e

    def delete_url_from_redis(self, url_id: int):
        """
        Delete URL data from Redis.

        Args:
            url_id (int): The ID of the URL.

        Raises:
            RedisError: If an error occurs while deleting URL data from Redis.
        """
        try:
            key = f"url_data:{url_id}"
            self.redis_manager.get_client().delete(key)
        except RedisError as e:
            self.logger.error("Error deleting URL data from Redis: %s", str(e))
            raise e
