from newsbot import logger, env, database
from newsbot.workers.nbworker import NBWorker
from newsbot.sources.pso2 import PSO2Reader
from newsbot.tables import Articles
from newsbot.collections import RSSArticle
from newsbot.outputs.discord import Discord
from newsbot.exceptions import FailedToAddToDatabase
from sqlalchemy.orm.session import Session
from time import sleep


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

            while True:
                reader = PSO2Reader()
                news = reader.getArticles()

                # Check the DB if it has been posted
                for i in news.articles:
                    i: RSSArticle = i
                    exists = self.articleExits(i)
                    if exists == False:
                        self.addArticle(i)

                        if len(env.pso2_hooks) >= 1:
                            self.sendToDiscord(i)

                logger.debug("Thread is going to sleep")
                sleep(env.threadSleepTimer)

    def sendToDiscord(self, i: Articles) -> None:
        env.discordQueue.append(i)
        self.logger.debug(f"PSO2 - '{i.title}' was added to the Discord queue.")
        # d = Discord(i, env.pso2_hooks, "PSO2")
        # d.sendMessage()
        # sleep(env.discord_delay_seconds)

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
        a.siteName = article.title
        a.tags = article.tags
        try:
            s.add(article)
            s.commit()
        except FailedToAddToDatabase as e:
            logger.critical(f"Failed to add {article.title} to the database! {e}")
        finally:
            s.close()
