from newsbot import logger, env
from newsbot.workers.nbworker import NBWorker
from newsbot.sources.pso2 import PSO2Reader
from newsbot.db import Articles


class PSO2Worker(NBWorker):
    def __init__(self) -> None:
        self.logger = logger
        pass

    def check(self) -> bool:
        if len(env.pso2_hooks) >= 1:
            return True

    def init(self):
        enable: bool = self.check()
        if enable == True:
            self.logger.debug("PSO2 Worker has started.")
            reader = PSO2Reader()
            news = reader.getArticles()

            # Check the DB if it has been posted

        pass
