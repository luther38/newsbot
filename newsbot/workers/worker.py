
from newsbot import logger, env, database
from newsbot.tables import Articles, DiscordQueue
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSArticle
from newsbot.exceptions import FailedToAddToDatabase
from time import sleep

class Worker:
    """
    This is a generic worker that will contain the source it will monitor.
    """
    def __init__(self, source: RSSReader):
        self.source: RSSReader = source
        pass

    def check(self) -> bool:
        if len(self.source.hooks) >= 1:
            return True
        else:
            return False

    def init(self) -> None:
        """
        This is the entry point for the worker.  
        Once its turned on it will check the Source for new items.
        """
        enable: bool = self.check()
        if enable == True:
            logger.debug(f"{self.source.siteName} Worker has started.")

            while True:
                news = self.source.getArticles()

                # Check the DB if it has been posted
                for i in news.articles:
                    i: RSSArticle = i
                    exists = self.articleExits(i)
                    if exists == False:
                        self.addArticle(i)
                        self.addDiscordQueue(i)

                        if len(self.source.settings['hooks']) >= 1:
                            self.sendToDiscord(i)

                logger.debug(f"{self.source.siteName} Worker is going to sleep.")
                sleep(env.threadSleepTimer)
        #raise NotImplementedError

    def sendToDiscord(self, article: RSSArticle):
        env.discordQueue.append(article)
        logger.debug(f" '{article.title}' was added to the Discord queue")

    def articleExits(self, article: RSSArticle) -> bool:
        s = database.newSession()
        a = Articles()
        try:
            for res in s.query(Articles).filter(Articles.url == article.link):
                a = res
        except Exception as e:
            pass

        s.close()
        if article.link == a.url:
            return True
        else:
            return False

    def addArticle(self, article: RSSArticle) -> None:
        s: Session = database.newSession()
        a = Articles(article)
        a.siteName = article.siteName
        a.tags = article.tags.__str__()
        try:
            s.add(a)
            s.commit()
        except FailedToAddToDatabase as e:
            logger.critical(f"Failed to add {article.title} to the database! {e}")
        finally:
            s.close()

    def addDiscordQueue(self, article: RSSArticle) -> None:
        s: Session = database.newSession()
        dq = DiscordQueue()
        dq.siteName = article.siteName
        dq.title = article.title
        dq.link = article.link
        dq.tags = article.tags
        dq.thumbnail = article.thumbnail
        dq.description = article.description

        try:
            s.add(dq)
            s.commit()
        except FailedToAddToDatabase as e:
            logger.critical(f"Failed to add {article.title} to DiscorQueue table! {e}")
        finally:
            s.close()
