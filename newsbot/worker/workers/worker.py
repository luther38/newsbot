# from newsbot import database
from newsbot.core.env import Env
from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Articles, DiscordQueue
from newsbot.worker.sources.common import ISources
from time import sleep


class Worker:
    """
    This is a generic worker that will contain the source it will monitor.
    """

    def __init__(self, source: ISources):
        self.logger = Logger(__class__)
        self.source: ISources = source
        self.enabled: bool = False
        self.env = Env()
        pass

    def check(self) -> bool:
        if len(self.source.links) >= 1:
            self.enabled = True
        else:
            self.enabled = False
            self.logger.info(
                f"{self.source.siteName} was not enabled.  Thread will exit."
            )

    def init(self) -> None:
        """
        This is the entry point for the worker.  
        Once its turned on it will check the Source for new items.
        """
        if self.source.sourceEnabled == True:
            self.logger.debug(f"{self.source.siteName} Worker has started.")

            while True:
                news = self.source.getArticles()

                # Check the DB if it has been posted
                for i in news:
                    exists = i.exists()

                    if exists == False:
                        i.add()

                        if len(self.source.hooks) >= 1:
                            dq = DiscordQueue()
                            dq.convert(i)
                            res = dq.add()

                            self.discordQueueMessage(i, res)

                self.logger.debug(f"{self.source.siteName} Worker is going to sleep.")
                sleep(self.env.threadSleepTimer)

    def discordQueueMessage(self, i: Articles, added: bool) -> None:
        msg: str = ""
        if i.title != "":
            msg = i.title
        else:
            msg = i.description

        if added == True:
            self.logger.info(f'"{msg}" was added to the Discord queue.')
        else:
            self.logger.error(f'"{msg}" was not added to add to the Discord queue.')
