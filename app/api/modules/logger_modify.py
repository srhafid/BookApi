from logging import DEBUG
from colorlog import StreamHandler, getLogger, ColoredFormatter


class ColoredLogger:
    """
    A utility class for creating and configuring colored loggers.

    This class provides a convenient way to create and configure a logger with
    colored output using the `colorlog` library.

    Attributes:
        logger (Logger): The configured logger instance.

    Methods:
        get_logger(): Get the configured logger instance.
    """

    def __init__(self):
        """
        Initialize the ColoredLogger instance.

        This constructor sets up the logger with a colored formatter and the
        desired log level.

        Args:
            None

        Returns:
            None
        """
        handler = StreamHandler()
        handler.setFormatter(
            ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
        )

        self.logger = getLogger(__name__)
        self.logger.setLevel(DEBUG)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        Get the configured logger instance.

        Returns:
            Logger: The configured logger instance.
        """
        return self.logger
