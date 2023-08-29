from fastapi import HTTPException
from app.api.modules.crud_postgresql.querys_user import UserRepository
from app.api.modules.logger_modify import ColoredLogger
from app.api.connections.db import DBContext
from app.api.modules.redis_conf.redis_conf import RedisManager
from redis import StrictRedis


class UserController:
    def __init__(
        self, logger: ColoredLogger, db: DBContext, redis_manager: RedisManager
    ):
        self.logger = logger.get_logger()
        self.db = db
        self.user_repo = UserRepository(db, logger)
        self.redis_manager = redis_manager

    def create_user(self, user_data: dict):
        try:
            user = self.user_repo.create_user(**user_data)
            return user
        except Exception as e:
            self.logger.error("Error creating user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error creating user")

    def read_user(self, user_id: int):
        try:
            user = self.user_repo.read_user(user_id)
            return user
        except Exception as e:
            self.logger.error("Error reading user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error reading user")

    def update_user(self, user_id: int, new_data: dict):
        try:
            user_updated = self.user_repo.update_user(user_id, new_data)
            if user_updated:
                return True
            return False
        except Exception as e:
            self.logger.error("Error updating user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error updating user")

    def delete_user(self, user_id: int):
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
