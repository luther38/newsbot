from loguru import logger


class Logger:
    def __init__(self) -> None:
        self.logger = self.init()
        pass

    def init(self) -> logger:
        logger.add("./mounts/logs/newsbot.log", rotation="500 MB")
        return logger

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)
        
    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)

    def __writeDb__(self,message, type) -> None:
        pass
