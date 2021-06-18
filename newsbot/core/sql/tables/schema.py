from dataclasses import dataclass
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    create_engine,
    Binary,
)
from sqlalchemy.types import Enum
import uuid
from newsbot.core.constant import SourceName, SourceType
from newsbot.core.sql import Base

class Articles(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True)
    siteName = Column(String)
    sourceName = Column(String)
    sourceType = Column(String)
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
        siteName: SourceName = "",
        sourceType: SourceType = "",
        sourceName: SourceName = "",
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
        authorImage: str = "",
    ) -> None:
        self.id = str(uuid.uuid4())
        self.siteName = siteName
        self.sourceName = sourceName
        self.sourceType = sourceType
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

class DiscordQueue(Base):
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
    sourceName = Column(String)
    sourceType = Column(String)

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())

class DiscordWebHooks(Base):
    __tablename__ = "discordwebhooks"
    id = Column(String, primary_key=True)
    name = Column(String)
    key = Column(String)
    url = Column(String)
    server = Column(String)
    channel = Column(String)
    enabled = Column(Boolean)
    fromEnv = Column(Boolean)

    def __init__(
        self,
        name: str = "",
        key: str = "",
        server: str = "",
        channel: str = "",
        url: str = "",
        fromEnv: bool = False
    ) -> None:
        self.name = name
        self.id = str(uuid.uuid4())
        self.server = server
        self.channel = channel
        if name == "":  
            self.name = self.__generateName__()
        else: 
            self.name = name
        self.key = key
        self.url = url
        self.enabled = True
        self.fromEnv: bool = fromEnv

    def __generateName__(self) -> str:
        return f"{self.server} - {self.channel}"

class Icons(Base):
    __tablename__ = "icons"
    id = Column(String, primary_key=True)
    filename = Column(String)
    site = Column(String)

    def __init__(self, fileName: str = "", site: str = "") -> None:
        self.id = str(uuid.uuid4())
        self.filename = fileName
        self.site = site

class Logs(Base):
    __tablename__ = "logs"
    id = Column("id", String, primary_key=True)
    date = Column("date", String)
    time = Column("time", String)
    type = Column("type", String)
    caller = Column("caller", String)
    message = Column("message", String)

    def __init__(self, date: str, time: str, type: str, caller: str, message: str):
        self.id = str(uuid.uuid4())
        self.date = date
        self.time = time
        self.type = type
        self.caller = caller
        self.message = message

class Settings(Base):
    __tablename__ = "settings"
    id = Column("id", String, primary_key=True)
    key = Column("key", String)
    value = Column("value", String)
    options = Column("options", String)
    notes = Column("notes", String)

    def __init__(
        self, key: str = "", value: str = "", options: str = "", notes: str = ""
    ):
        self.id = str(uuid.uuid4())
        self.key = key
        self.value = value
        self.options = options
        self.notes = notes

class Sources(Base):
    __tablename__ = "sources"
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    source: str = Column(String)
    type: str = Column(String)
    value: str = Column(String)
    enabled: bool = Column(Boolean)
    url: str = Column(String)
    tags: str = Column(String)
    fromEnv: bool = Column(Boolean)

    def __init__(
        self,
        id: str = "",
        name: str = "",
        source: str = "",
        type: str = "",
        value: str = "",
        enabled: bool = True,
        url: str = "",
        tags: str = "",
        fromEnv: bool = False
    ) -> None:
        if id == "": self.id: str = str(uuid.uuid4())
        else: self.id = id
        self.name: str = name
        self.source: str = source
        self.type: str = type
        self.value: str = value
        self.enabled: bool = enabled
        self.url: str = url
        self.tags: str = tags
        self.fromEnv: bool = fromEnv

class SourceLinks(Base):
    __tablename__ = "sourcelinks"
    id = Column("id", String, primary_key=True)
    sourceID: str = Column("sourceID", String)
    sourceType: str = Column('sourceType', String)
    sourceName: str = Column("sourceName", String)
    discordName: str = Column("discordName", String)
    discordID: str = Column("discordID", String)

    def __init__(self, sourceName: SourceName = "", sourceID: str = "", sourceType: str = '',
        discordName: str = '', discordID: str = ""):
        self.id = str(uuid.uuid4())
        self.sourceID = sourceID
        self.sourceType = sourceType
        self.sourceName = sourceName
        self.discordID = discordID
        self.discordName = discordName


