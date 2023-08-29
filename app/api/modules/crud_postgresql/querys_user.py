from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.models.model import User
from app.api.connections.db import DBContext
from app.api.modules.logger_modify import ColoredLogger


class UserRepository:
    """
    Provides CRUD operations for User data.

    This class encapsulates the operations to manage User data in the database.
    """

    def __init__(self, db: DBContext, logger: ColoredLogger):
        """
        Initializes a new instance of UserRepository.

        Args:
            db (DBContext): The database context to use for database operations.
            logger (ColoredLogger): The logger instance to use for logging.
        """
        self.logger = logger.get_logger()
        self.db = db

    def create_user(self, username: str, password: str, role: str) -> User:
        """
        Creates a new User in the database.

        Args:
            username (str): The username of the User.
            password (str): The password of the User.
            role (str): The role of the User.

        Returns:
            User: The created User object.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            user = User(username=username, password=password, role=role)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            self.logger.info("User created: %s", user.username)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error("Error creating user: %s", str(e))
            raise e

    def read_user(self, user_id: int) -> User:
        """
        Retrieves a User from the database by User ID.

        Args:
            user_id (int): The ID of the User to retrieve.

        Returns:
            User: The retrieved User object.

        Raises:
            ValueError: If the User with the specified ID is not found.
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                self.logger.warning("User not found with ID: %d", user_id)
                raise ValueError("User not found")
            self.logger.info("User retrieved: %s", user.username)
            return user
        except SQLAlchemyError as e:
            self.logger.error("Error reading user: %s", str(e))
            raise e

    def update_user(self, user_id: int, new_data: dict) -> bool:
        """
        Updates a User in the database.

        Args:
            user_id (int): The ID of the User to update.
            new_data (dict): Dictionary containing the new data to update.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            user = self.read_user(user_id)
            if not user:
                return False

            for key, value in new_data.items():
                setattr(user, key, value)

            self.db.commit()
            self.logger.info("User updated: %s", user.username)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error("Error updating user: %s", str(e))
            raise e

    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a User from the database.

        Args:
            user_id (int): The ID of the User to delete.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            user = self.read_user(user_id)
            if not user:
                return False

            self.db.delete(user)
            self.db.commit()
            self.logger.info("User deleted: %s", user.username)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error("Error deleting user: %s", str(e))
            raise e
