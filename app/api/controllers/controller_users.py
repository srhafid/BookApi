from fastapi import HTTPException
from app.api.connections.db import DBContext
from app.api.modules.crud_postgresql.querys_user import UserRepository
from app.api.modules.crud_reddis.crud_redis_basic import CrudRedis
from app.api.modules.logger_modify import ColoredLogger
from app.api.modules.redis_conf.redis_conf import RedisManager

logger = ColoredLogger().get_logger()

class UserController:
    def __init__(
        self, db: DBContext, redis_manager: RedisManager
    ):
        self.logger = logger
        self.db = db
        self.user_repo = UserRepository(db)
        self.redis_manager = CrudRedis(redis_manager)

    def create_user(self, user_data: dict):
        try:
            user = self.user_repo.create_user(**user_data)
            user_dict = {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
            return user_dict
        except Exception as e:
            self.logger.error("Error creating user: %s", str(e))
            raise HTTPException(status_code=500, detail="Error creating user")

    def read_user(self, user_id: int):
        try:
            user = self.user_repo.read_user(user_id)
            user_dict = {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
            return user_dict
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
