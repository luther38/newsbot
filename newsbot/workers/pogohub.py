from newsbot import logger, env, database
from newsbot.sources.pokemongohub import RSSPogohub
from newsbot.outputs.discord import Discord
from newsbot.collections import RSSRoot, RSSArticle
from newsbot.tables import Articles
from time import sleep


class PoGoHubWorker:
    def __init__(self) -> None:
        self.settings = env
        pass

    def checkup(self) -> bool:
        # This checks to ensure that we want to use this source.
        if len(self.settings.pogo_hooks) >= 1:
            return True

    def init(self) -> None:
        runThread: bool = self.checkup()
        if runThread == True:
            logger.debug(f"Pokemon Go Hub - Thread Started")
            while True:
                logger.debug("Checking for new articles")
                pogo = RSSPogohub()
                pogoNews: RSSRoot = pogo.getArticles()

                for a in pogoNews.articles:
                    exists = self.exists(a)

                    if exists == False:
                        self.add(a)
                        a.thumbnail = pogo.getArticleThumbnail(a.link)

                        # Send to outputs
                        # Check if we have any webhooks to send to.
                        if len(self.settings.pogo_hooks) >= 1:
                            self.sendToDiscord(a)

                logger.debug("Thead is going to sleep")
                sleep(env.threadSleepTimer)

        else:
            logger.info(
                "Did not have enough to enable Pokemon Go Hub Source.  Thread will exit."
            )

    def sendToDiscord(self, article: RSSArticle):
        env.discordQueue.append(article)
        # d = Discord(article, self.settings.pogo_hooks, "Pokemon Go Hub")
        # d.sendMessage()
        # sleep(self.settings.discord_delay_seconds)

    def exists(self, item: RSSArticle) -> bool:
        session = database.newSession()
        result = Articles()
        try:
            for res in session.query(Articles).filter(Articles.url == item.link):
                result = res
        except Exception as e:
            print(e)
        finally:
            session.close()

        if result.url == item.link:
            return True
        else:
            return False

    def add(self, item: RSSArticle) -> None:
        session = database.newSession()
        a = Articles(item)
        a.siteName = "Pokemon Go Hub"
        a.tags = item.tags.__str__()
        try:
            session.add(a)
            session.commit()
        except Exception as e:
            print(f"Failed to add record to the DB. {e}")
        finally:
            session.close()
