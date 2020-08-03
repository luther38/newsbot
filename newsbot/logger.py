
import logging

class Logger():
    def __init__(self) -> None:
        self.logger = self.init()
        pass

    def init(self) -> logging.Logger:
        format_string = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        logger = logging.getLogger(__name__)
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
        stream.setFormatter(formatter)
        logger.addHandler(stream)
        return logger