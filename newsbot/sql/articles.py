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
from newsbot.db import Base
from newsbot import database
from newsbot.sql.exceptions import FailedToAddToDatabase
from newsbot.sql.iTables import ITables

class Articles(Base, ITables):
    __tablename__ = "articles"
    id = Column(String, primary_key=True)
    siteName = Column(String)
    tags = Column(String)
    title = Column(String)
    url = Column(String)
    pubDate = Column(String)
    video = Column(String)
    videoHeight = Column(Integer)
    videoWidth = Column(Integer)
    thumbnail = Column(String)
    description = Column(String)
    authorName = Column(String)
    authorImage = Column(String)

    def __init__(
        self,
        siteName: str = "",
        tags: str = "",
        title: str = "",
        url: str = "",
        pubDate: str = "",
        video: str = "",
        videoHeight: int = -1,
        videoWidth: int = -1,
        thumbnail: str = "",
        description: str = "",
        authorName: str = "",
        authorImage: str = ""
    ) -> None:
        self.id = str(uuid.uuid4())
        self.siteName = siteName
        self.tags = tags
        self.title = title
        self.url = url
        self.pubDate = pubDate
        self.video = video
        self.videoHeight = videoHeight
        self.videoWidth = videoWidth
        self.thumbnail = thumbnail
        self.description = description
        self.authorName = authorName
        self.authorImage = authorImage

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

        a = Articles(
            siteName=self.siteName,
            tags=self.tags,
            title=self.title,
            url=self.url,
            pubDate=self.pubDate,
            video=self.video,
            videoWidth=self.videoWidth,
            videoHeight=self.videoHeight,
            thumbnail=self.thumbnail,
            description=self.description,
            authorImage=self.authorImage,
            authorName=self.authorName
        )

        try:
            s.add(a)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.title} to the database! {e}")
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
