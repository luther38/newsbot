from newsbot.core.sql import database
from sqlalchemy.sql.expression import desc
from newsbot.core.constant import SourceName
from newsbot.core.env import Env
from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Articles, ArticlesTable, DiscordQueue, DiscordQueueTable
from newsbot.worker.sources.common import ISources
from time import sleep


class Worker:
    """
    This is a generic worker that will contain the source it will monitor.
    """

    def __init__(self, source: ISources):
        #self.activateTables()
        self.logger = Logger(__class__)
        self.enabled: bool = False
        self.env = Env()
        self.source = source
        #self.activateSource(source)
        #self.check()
        pass
    
    def activateSource(self) -> None:
        #self.source: ISources = source
        self.source.session = self.session
        self.source.enableTables()
        self.source.checkEnv(self.source.siteName)

    def activateTables(self) -> None:
        self.session = database.newSession()
        self.articlesTable = ArticlesTable(session=self.session)
        self.queueTable = DiscordQueueTable(session=self.session)

    def threadInit(self) -> None:
        """This runs a startup process inside the thread"""
        self.activateTables()
        self.activateSource()
        self.check()

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
        self.threadInit()
        if self.source.sourceEnabled == True:
            self.logger.info(f"{self.source.siteName} Worker has started.")

            while True:
                news = self.source.getArticles()

                # Check the DB if it has been posted
                for i in news:
                    dq = self.queueTable.convert(i)
                    exists = self.articlesTable.exists(i.url)

                    if exists == False:
                        self.articlesTable.add(i)

                        if len(self.source.hooks) >= 1:
                            res = self.queueTable.add(dq)
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
