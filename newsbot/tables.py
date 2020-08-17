from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    create_engine,
    Binary,
)
import uuid
from typing import List
from newsbot import Base, database, logger
from newsbot.collections import RSSArticle
from newsbot.exceptions import FailedToAddToDatabase


class Articles(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True)
    siteName = Column(String)
    tags = Column(String)
    title = Column(String)
    url = Column(String)
    pubDate = Column(String)

    def __init__(self, article: RSSArticle = RSSArticle()) -> None:
        self.id = str(uuid.uuid4())
        self.convertRssArticle(article)

    def convertRssArticle(self, article: RSSArticle) -> None:
        self.title = article.title
        self.siteName = article.siteName
        self.pubDate = article.pubDate
        self.tags = article.tags
        self.url = article.link

    def exists(self) -> bool:
        """
        Check to see if the current record exists.
        """

        s = database.newSession()
        a = Articles()
        try:
            for res in s.query(Articles).filter(Articles.url == self.url):
                a = res
        except Exception as e:
            pass
        finally:
            s.close()

        if self.url == a.url:
            return True
        else:
            return False

    def add(self) -> None:
        s = database.newSession()

        a = Articles()
        a.siteName = self.siteName
        a.tags = self.tags
        a.title = self.title
        a.url = self.url
        a.pubDate = self.pubDate

        try:
            s.add(a)
            s.commit()
        except FailedToAddToDatabase as e:
            logger.critical(f"Failed to add {self.title} to the database! {e}")
        finally:
            s.close()

    def rowCount(self) -> int:
        """
        Returns the number of rows based off the SiteName value provieded.
        """

        s = database.newSession()
        l = list()
        try:
            for res in s.query(Articles).filter(Articles.siteName == self.siteName):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)


class Sources(Base):
    __tablename__ = "sources"
    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)
    enabled = Column(Boolean)

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())


class DiscordWebHooks(Base):
    __tablename__ = "discordwebhooks"
    id = Column(String, primary_key=True)
    name = Column(String)
    key = Column(String)
    enabled = Column(Boolean)

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())


class DiscordQueue(Base):
    __tablename__ = "discordQueue"
    id = Column(String, primary_key=True)
    siteName = Column(String)
    title = Column(String)
    link = Column(String)
    tags = Column(String)
    thumbnail = Column(String)
    description = Column(String)

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())

    def convert(self, rssArticle: RSSArticle) -> None:
        self.siteName = rssArticle.siteName
        self.title = rssArticle.title
        self.link = rssArticle.link
        self.tags = rssArticle.tags
        self.thumbnail = rssArticle.thumbnail
        self.description = rssArticle.description
        pass

    def getQueue(self) -> List:
        s = database.newSession()
        queue = list()
        dq = DiscordQueue()
        try:
            for res in s.query(DiscordQueue):
                queue.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return queue

    def add(self) -> None:
        s = database.newSession()

        dq = DiscordQueue()
        dq.siteName = self.siteName
        dq.title = self.title
        dq.link = self.link
        dq.tags = self.tags
        dq.thumbnail = self.thumbnail
        dq.description = self.description

        try:
            s.add(dq)
            s.commit()
            logger.debug(f" '{self.title}' was added to the Discord queue")
        except FailedToAddToDatabase as e:
            logger.critical(f"Failed to add {self.title} to DiscorQueue table! {e}")
        finally:
            s.close()

    def remove(self) -> None:
        s = database.newSession()
        try:
            for d in s.query(DiscordQueue).filter(DiscordQueue.link == self.link):
                s.delete(d)
            s.commit()
        except Exception as e:
            logger.critical(f"{e}")
        finally:
            s.close()
