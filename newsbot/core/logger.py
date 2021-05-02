# from loguru import logger
from loguru import logger as _logger
from newsbot.core.sql.tables import Logs
from datetime import datetime

class Logger:
    def __init__(self, callerClass: str = "") -> None:
        """
        This class generates the logger used in NewsBot.
        When you call it, call it like this Logger(__class__).
        Doing this will let the logger know the source class

        Examples:
        logger = Logger(__class__)
        Logger(__class__).debug("hello world")
        """
        self.callerClass: str = str(callerClass)
        _logger.add("./mounts/logs/newsbot.log", rotation="5 MB")
        pass

    def debug(self, message: str) -> None:
        _logger.debug(message)
        self.__writeDb(message, "debug")

    def info(self, message: str) -> None:
        _logger.info(message)
        self.__writeDb(message, "info")

    def warning(self, message: str) -> None:
        _logger.warning(message)
        self.__writeDb(message, "warning")

    def error(self, message: str) -> None:
        _logger.error(message)
        self.__writeDb(message, "error")

    def critical(self, message: str) -> None:
        _logger.critical(message)
        self.__writeDb(message, "critical")

    def __writeDb(self, message, type) -> None:
        dt = datetime.now()
        Logs(
            date=f"{dt.year}-{dt.month}-{dt.day}",
            time=f"{dt.hour}:{dt.minute}:{dt.second}:{dt.microsecond}",
            type=type,
            caller=self.callerClass,
            message=message,
        ).add()
        pass
