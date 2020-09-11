from loguru import logger


class Logger:
    def __init__(self) -> None:
        self.logger = self.init()
        pass

    def init(self) -> logger:
        logger.add("./mounts/logs/newsbot.log", rotation="500 MB")
        return logger
