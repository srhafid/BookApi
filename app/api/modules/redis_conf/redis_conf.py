from redis import StrictRedis


class RedisManager:
    """
    Class for managing the global Redis client instance.

    This class provides a centralized way to configure and obtain the Redis client
    instance for use in different parts of the project.

    Args:
        host (str): The host where the Redis server is running. Default is 'localhost'.
        port (int): The port on which the Redis server is listening. Default is 6379.
        db (int): The Redis database number to use. Default is 0.

    Attributes:
        redis_client (redis.StrictRedis): The Redis client instance.

    Example:
        # Create a global instance of the RedisManager class
        redis_manager = RedisManager()

        # Get the Redis client from the global instance
        redis_client = redis_manager.get_client()

        # Now you can use redis_client to perform operations on Redis
    """

    def __init__(self, host="localhost", port=6379, db=0):
        """
        Initialize a new instance of RedisManager.

        Args:
            host (str): The host where the Redis server is running. Default is 'localhost'.
            port (int): The port on which the Redis server is listening. Default is 6379.
            db (int): The Redis database number to use. Default is 0.
        """
        self.redis_client = StrictRedis(host=host, port=port, db=db)

    def get_client(self):
        """
        Get the Redis client instance.

        Returns:
            redis.StrictRedis: The Redis client instance.
        """
        return self.redis_client


# # Create a global instance of the RedisManager class
# redis_manager = RedisManager()
