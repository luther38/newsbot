
from loguru import logger
from newsbot.tables import Logs
from datetime import datetime


class Logger:
    def __init__(self) -> None:
        self.logger = self.init()
        pass

    def init(self) -> logger:
        logger.add("./mounts/logs/newsbot.log", rotation="5 MB")
        return logger

    def debug(self, message: str) -> None:
        self.logger.debug(message)
        self.__writeDb__(message, 'debug')

    def info(self, message: str) -> None:
        self.logger.info(message)
        self.__writeDb__(message, 'info')

    def warning(self, message: str) -> None:
        self.logger.warning(message)
        self.__writeDb__(message, 'warning')

    def error(self, message: str) -> None:
        self.logger.error(message)
        self.__writeDb__(message, 'error')

    def critical(self, message: str) -> None:
        self.logger.critical(message)
        self.__writeDb__(message, 'critical')

    def __writeDb__(self, message, type) -> None:
        dt = datetime.now()
        Logs(date=f"{dt.year}-{dt.month}-{dt.day}", 
            time=f"{dt.hour}:{dt.minute}:{dt.second}:{dt.microsecond}",
            type=type,
            caller='',
            message=message).add()
        pass
