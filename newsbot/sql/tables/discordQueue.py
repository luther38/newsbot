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
from newsbot.sql import database, Base
from newsbot.sql.tables import Articles, ITables
from newsbot.sql.exceptions import FailedToAddToDatabase

class DiscordQueue(Base, ITables):
    __tablename__ = "discordQueue"
    id = Column(String, primary_key=True)
    siteName = Column(String)
    title = Column(String)
    link = Column(String)
    tags = Column(String)
    thumbnail = Column(String)
    description = Column(String)
    video = Column(String)
    videoHeight = Column(Integer)
    videoWidth = Column(Integer)
    authorName = Column(String)
    authorImage = Column(String)

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())

    def convert(self, Article: Articles) -> None:
        self.siteName = Article.siteName
        self.title = Article.title
        self.link = Article.url
        self.tags = Article.tags
        self.thumbnail = Article.thumbnail
        self.description = Article.description
        self.video = Article.video
        self.videoHeight = Article.videoHeight
        self.videoWidth = Article.videoWidth
        self.authorName = Article.authorName
        self.authorImage = Article.authorImage

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

    def add(self) -> bool:
        s = database.newSession()
        res: bool = True
        try:
            s.add(self)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.title} to DiscorQueue table! {e}")
            res = False
        finally:
            s.close()
            return res

    def remove(self) -> None:
        s = database.newSession()
        try:
            for d in s.query(DiscordQueue).filter(DiscordQueue.link == self.link):
                s.delete(d)
            s.commit()
        except Exception as e:
            print(f"{e}")
        finally:
            s.close()

    def __len__(self) -> int:
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