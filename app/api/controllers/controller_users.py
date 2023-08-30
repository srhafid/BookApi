from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.api.connections.db import DBContext
from app.api.modules.crud_postgresql.querys_user import UserRepository
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager

# Initialize the logger
logger = ColoredLogger().get_logger()

class UserController:
    """
    Controller class for user-related operations.
    """

    def __init__(self, db: DBContext, redis_manager: RedisManager):
        """
        Initializes an instance of UserController.

        Args:
            db (DBContext): The database context.
            redis_manager (RedisManager): The Redis manager.
        """
        self.logger = logger
        self.db = db
        self.user_repo = UserRepository(db)
        self.redis_manager = CrudRedis(redis_manager)

    def create_user(self, user_data: dict):
        """
        Create a new user.

        Args:
            user_data (dict): The user data.

        Returns:
            dict: The created user data.
        """
        try:
            user = self.user_repo.create_user(**user_data)
            user_to_json = jsonable_encoder(user)
            return user_to_json
        except Exception as e:
            self.logger.error("Error creating user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error creating user")

    def read_user(self, user_id: int):
        """
        Read user data by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: The retrieved user data.
        """
        try:
            user = self.user_repo.read_user(user_id)
            user_to_json = jsonable_encoder(user)
            return user_to_json
        except Exception as e:
            self.logger.error("Error reading user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error reading user")

    def update_user(self, user_id: int, new_data: dict):
        """
        Update user data by ID.

        Args:
            user_id (int): The ID of the user.
            new_data (dict): The updated user data.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        try:
            user_updated = self.user_repo.update_user(user_id, new_data)
            if user_updated:
                return True
            return False
        except Exception as e:
            self.logger.error("Error updating user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error updating user")

    def delete_user(self, user_id: int):
        """
        Delete user data by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            user_deleted = self.user_repo.delete_user(user_id)
            if user_deleted:
                return True
            return False
        except Exception as e:
            self.logger.error("Error deleting user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error deleting user")

# Create a global instance of the RedisManager class
redis_manager = RedisManager()
