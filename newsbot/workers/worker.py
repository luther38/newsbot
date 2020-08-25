from newsbot import logger, env, database
from newsbot.tables import Articles, DiscordQueue
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSArticle
from time import sleep

class Worker():
    """
    This is a generic worker that will contain the source it will monitor.
    """

    def __init__(self, source: RSSReader):
        self.source: RSSReader = source
        self.enabled: bool = False
        pass

    def check(self) -> bool:
        if len(self.source.links) >= 1:
            self.enabled = True
        else:
            self.enabled = False
            logger.info(f"{self.source.siteName} was not enabled.  Thread will exit.")

    def init(self) -> None:
        """
        This is the entry point for the worker.  
        Once its turned on it will check the Source for new items.
        """
        self.check()

        if self.enabled == True:
            logger.debug(f"{self.source.siteName} Worker has started.")

            while True:
                news = self.source.getArticles()

                # Check the DB if it has been posted
                for i in news.articles:
                    i: RSSArticle = i
                    a = Articles(article=i)
                    exists = a.exists()

                    if exists == False:
                        a.add()

                        if len(self.source.hooks) >= 1:
                            dq = DiscordQueue()
                            dq.convert(i)
                            dq.add()

                logger.debug(f"{self.source.siteName} Worker is going to sleep.")
                sleep(env.threadSleepTimer)
