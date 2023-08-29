from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.api.models.model import Urls
from app.api.modules.logger_modify import ColoredLogger

logger = ColoredLogger().get_logger()

class UrlDataRepository:
    """
    Provides CRUD operations for URLs data.

    This class encapsulates the operations to manage URL data in the database and Redis.
    """

    def __init__(self, db: Session):
        """
        Initializes a new instance of UrlDataRepository.

        Args:
            db (DBContext): The database context to use for database operations.
            redis (RedisManager): The Redis manager to use for Redis operations.
            logger (ColoredLogger): The logger instance to use for logging.
        """
        self.logger = logger
        self.db = db

    def create_url(self, title: str, description: str, author: str, rating: int, user_id: int) -> Urls:
        """
        Creates a new URL in the database and stores the log in Redis.

        Args:
            title (str): The title of the URL.
            description (str): The description of the URL.
            author (str): The author of the URL.
            rating (int): The rating of the URL.
            user_id (int): The ID of the user to whom the URL belongs.

        Returns:
            Urls: The created Urls object.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            url = Urls(title=title, description=description, author=author, rating=rating, user_id=user_id)
            self.db.add(url)
            self.db.commit()
            self.db.refresh(url)
            self.logger.info("URL created: %s", url.title)

            log_message = f"URL created: {url.title}"
            self.logger.info("URL log stored in Redis: %s", log_message)

            return url
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error("Error creating URL: %s", str(e))
            raise e

    def read_url(self, url_id: int) -> Urls:
        """
        Retrieves a URL from the database by URL ID and stores the log in Redis.

        Args:
            url_id (int): The ID of the URL to retrieve.

        Returns:
            Urls: The retrieved Urls object.

        Raises:
            ValueError: If the URL with the specified ID is not found.
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            url = self.db.query(Urls).filter(Urls.id == url_id).first()
            if not url:
                self.logger.warning("URL not found with ID: %d", url_id)
                raise ValueError("URL not found")
            self.logger.info("URL retrieved: %s", url.title)

            log_message = f"URL retrieved: {url.title}"
            self.logger.info("URL log stored in Redis: %s", log_message)

            return url
        except SQLAlchemyError as e:
            self.logger.error("Error reading URL: %s", str(e))
            raise e

    def update_url(self, url_id: int, new_data: dict) -> bool:
        """
        Updates a URL in the database and stores the log in Redis.

        Args:
            url_id (int): The ID of the URL to update.
            new_data (dict): Dictionary containing the new data to update.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            url = self.read_url(url_id)
            if not url:
                return False

            for key, value in new_data.items():
                setattr(url, key, value)

            self.db.commit()
            self.logger.info("URL updated: %s", url.title)

            log_message = f"URL updated: {url.title}"
            self.logger.info("URL log stored in Redis: %s", log_message)

            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error("Error updating URL: %s", str(e))
            raise e

    def delete_url(self, url_id: int) -> bool:
        """
        Deletes a URL from the database and stores the log in Redis.

        Args:
            url_id (int): The ID of the URL to delete.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            SQLAlchemyError: If an error occurs during database operations.
        """
        try:
            url = self.read_url(url_id)
            if not url:
                return False

            self.db.delete(url)
            self.db.commit()
            self.logger.info("URL deleted: %s", url.title)

            log_message = f"URL deleted: {url.title}"
            self.logger.info("URL log stored in Redis: %s", log_message)

            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            self.logger.error("Error deleting URL: %s", str(e))
            raise e