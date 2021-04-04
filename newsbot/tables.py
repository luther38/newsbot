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
from newsbot.db import DB as database

#from newsbot.logger import Logger

class FailedToAddToDatabase(Exception):
    pass

#class Articles(Base):
#    __tablename__ = "articles"
#    id = Column(String, primary_key=True)
#    siteName = Column(String)
#    tags = Column(String)
#    title = Column(String)
#    url = Column(String)
#    pubDate = Column(String)
#    video = Column(String)
#    videoHeight = Column(Integer)
#    videoWidth = Column(Integer)
#    thumbnail = Column(String)
#    description = Column(String)
#    authorName = Column(String)
#    authorImage = Column(String)
#
#    def __init__(
#        self,
#        siteName: str = "",
#        tags: str = "",
#        title: str = "",
#        url: str = "",
#        pubDate: str = "",
#        video: str = "",
#        videoHeight: int = -1,
#        videoWidth: int = -1,
#        thumbnail: str = "",
#        description: str = "",
#        authorName: str = "",
#        authorImage: str = ""
#    ) -> None:
#        self.id = str(uuid.uuid4())
#        self.siteName = siteName
#        self.tags = tags
#        self.title = title
#        self.url = url
#        self.pubDate = pubDate
#        self.video = video
#        self.videoHeight = videoHeight
#        self.videoWidth = videoWidth
#        self.thumbnail = thumbnail
#        self.description = description
#        self.authorName = authorName
#        self.authorImage = authorImage
#
#    def exists(self) -> bool:
#        """
#        Check to see if the current record exists.
#        """
#
#        s = database.newSession()
#        a = Articles()
#        try:
#            for res in s.query(Articles).filter(Articles.url == self.url):
#                a = res
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        if self.url == a.url:
#            return True
#        else:
#            return False
#
#    def add(self) -> None:
#        s = database.newSession()
#
#        a = Articles(
#            siteName=self.siteName,
#            tags=self.tags,
#            title=self.title,
#            url=self.url,
#            pubDate=self.pubDate,
#            video=self.video,
#            videoWidth=self.videoWidth,
#            videoHeight=self.videoHeight,
#            thumbnail=self.thumbnail,
#            description=self.description,
#            authorImage=self.authorImage,
#            authorName=self.authorName
#        )
#
#        try:
#            s.add(a)
#            s.commit()
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add {self.title} to the database! {e}")
#        finally:
#            s.close()
#
#    def __len__(self) -> int:
#        """
#        Returns the number of rows based off the SiteName value provieded.
#        """
#
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(Articles).filter(Articles.siteName == self.siteName):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return len(l)


#class Sources(Base):
#    __tablename__ = "sources"
#    id = Column(String, primary_key=True)
#    name = Column(String)
#    url = Column(String)
#    enabled = Column(Boolean)
#
#    def __init__(self, name="", url="") -> None:
#        self.id = str(uuid.uuid4())
#        self.name = name
#        self.url = url
#        self.enabled = True
#
#    def add(self) -> None:
#        s = database.newSession()
#        h = Sources()
#        h.name = self.name
#        h.url = self.url
#        h.enabled = self.enabled
#        try:
#            s.add(self)
#            s.commit()
#            # print(f"'{self.name}' was added to the Discord queue")
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add {self.name} to DiscordWebHook table! {e}")
#        finally:
#            s.close()
#``
#    def clearTable(self) -> None:``
#        s = database.newSession()
#        try:
#            for d in s.query(Sources):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            print(f"{e}")
#        finally:
#            s.close()
#
#    def clearSingle(self) -> bool:
#        """
#        This will remove a single entry from the table by its ID value.
#        """
#        s = database.newSession()
#        result: bool = False
#        try:
#            for i in s.query(Sources).filter(Sources.id == self.id):
#                s.delete(i)
#                s.commit()
#                result = True
#        except Exception as e:
#            print(e)
#        finally:
#            s.close()
#            return result
#
#    def findAllByName(self) -> List:
#        s = database.newSession()
#        hooks = list()
#        try:
#            for res in s.query(Sources).filter(Sources.name.contains(self.name)):
#                hooks.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#            return hooks
#
#    def __len__(self) -> int:
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(DiscordWebHooks):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return len(l)


#class DiscordWebHooks(Base):
#    __tablename__ = "discordwebhooks"
#    id = Column(String, primary_key=True)
#    name = Column(String)
#    key = Column(String)
#    url = Column(String)
#    server = Column(String)
#    channel = Column(String)
#    enabled = Column(Boolean)
#
#    def __init__(self, name:str="", key:str="", server:str = "", channel:str = "", url: str = "") -> None:
#        self.id = str(uuid.uuid4())
#        self.name = name
#        self.key = key
#        self.url = url
#        self.server = server
#        self.channel = channel
#        self.enabled = True
#
#    def add(self) -> None:
#        s = database().newSession()
#        h = DiscordWebHooks()
#        h.key = self.key
#        h.url = self.url
#        h.name = self.name
#        h.server = self.server
#        h.channel = self.channel
#        h.enabled = self.enabled
#        try:
#            s.add(self)
#            s.commit()
#            # print(f"'{self.name}' was added to the Discord queue")
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add {self.name} to DiscordWebHook table! {e}")
#        finally:
#            s.close()
#
#    def clearTable(self) -> None:
#        s = database.newSession()
#        try:
#            for d in s.query(DiscordWebHooks):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            print(f"{e}")
#        finally:
#            s.close()
#
#    def clearSingle(self) -> bool:
#        """
#        This will remove a single entry from the table by its ID value.
#        """
#        s = database.newSession()
#        result: bool = False
#        try:
#            for i in s.query(DiscordWebHooks).filter(DiscordWebHooks.id == self.id):
#                s.delete(i)
#                s.commit()
#                result = True
#        except Exception as e:
#            print(e)
#        finally:
#            s.close()
#            return result
#
#    def findAllById(self) -> List:
#        s = database.newSession()
#        hooks = list()
#        try:
#            for res in s.query(DiscordWebHooks).filter(
#                DiscordWebHooks.id.contains(self.id)
#            ):
#                hooks.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#            return hooks
#
#    def findAllByName(self) -> List:
#        s = database.newSession()
#        hooks = list()
#        try:
#            for res in s.query(DiscordWebHooks).filter(
#                DiscordWebHooks.name.contains(self.name)
#            ):
#                hooks.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#            return hooks
#
#    def findAll(self) -> List:
#        s = database.newSession()
#        hooks = list()
#        try:
#            for res in s.query(DiscordWebHooks):
#                hooks.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#            return hooks
#
#    def __len__(self) -> int:
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(DiscordWebHooks):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return len(l)
#

#class DiscordQueue(Base):
#    __tablename__ = "discordQueue"
#    id = Column(String, primary_key=True)
#    siteName = Column(String)
#    title = Column(String)
#    link = Column(String)
#    tags = Column(String)
#    thumbnail = Column(String)
#    description = Column(String)
#    video = Column(String)
#    videoHeight = Column(Integer)
#    videoWidth = Column(Integer)
#    authorName = Column(String)
#    authorImage = Column(String)
#
#    def __init__(self) -> None:
#        self.id = str(uuid.uuid4())
#
#    def convert(self, Article: Articles) -> None:
#        self.siteName = Article.siteName
#        self.title = Article.title
#        self.link = Article.url
#        self.tags = Article.tags
#        self.thumbnail = Article.thumbnail
#        self.description = Article.description
#        self.video = Article.video
#        self.videoHeight = Article.videoHeight
#        self.videoWidth = Article.videoWidth
#        self.authorName = Article.authorName
#        self.authorImage = Article.authorImage
#
#    def getQueue(self) -> List:
#        s = database.newSession()
#        queue = list()
#        dq = DiscordQueue()
#        try:
#            for res in s.query(DiscordQueue):
#                queue.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return queue
#
#    def add(self) -> bool:
#        s = database.newSession()
#        res: bool = True
#        try:
#            s.add(self)
#            s.commit()
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add {self.title} to DiscorQueue table! {e}")
#            res = False
#        finally:
#            s.close()
#            return res
#
#    def remove(self) -> None:
#        s = database.newSession()
#        try:
#            for d in s.query(DiscordQueue).filter(DiscordQueue.link == self.link):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            print(f"{e}")
#        finally:
#            s.close()
#
#    def __len__(self) -> int:
#        """
#        Returns the number of rows based off the SiteName value provieded.
#        """
#
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(Articles).filter(Articles.siteName == self.siteName):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return len(l)


#class Icons(Base):
#    __tablename__ = "icons"
#    id = Column(String, primary_key=True)
#    filename = Column(String)
#    site = Column(String)
#
#    def __init__(self,
#        fileName: str = "",
#        site: str = ""
#        ) -> None:
#        self.id = str(uuid.uuid4())
#        self.filename = fileName
#        self.site = site
#
#    def add(self) -> None:
#        s = database.newSession()
#
#        try:
#            s.add(self)
#            s.commit()
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add {self.site} to Icons table! {e}")
#        finally:
#            s.close()
#
#    def update(self) -> None:
#        #s = database.newSession()
#        
#        res = self.findAllByName()
#        if len(res) == 0:
#            self.add()
#        elif res[0].site != self.site or res[0].filename != self.filename:
#            self.remove()
#            self.add()
#        else:
#            pass
#
#    def remove(self) -> None:
#        s = database.newSession()
#        try:
#            for d in s.query(Icons).filter(Icons.site == self.site):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            print(f"{e}")
#        finally:
#            s.close()
#
#    def clearTable(self) -> None:
#        s = database.newSession()
#        try:
#            for d in s.query(Icons):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            print(f"{e}")
#        finally:
#            s.close()
#
#    def findAllByName(self) -> List:
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(Icons).filter(Icons.site.contains(self.site)):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#            return l
#
#    def __len__(self) -> int:
#        """
#        Returns the number of rows based off the Site value provided.
#
#        Returns: Int
#        """
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(Icons).filter(Icons.site == self.site):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return len(l)


#class Settings(Base):
#    __tablename__ = 'settings'
#    id = Column('id', String, primary_key=True)
#    key = Column("key", String)
#    value = Column("value", String)
#    options = Column("options", String)
#    notes = Column("notes", String)
#
#    def __init__(self, key: str = "", value: str = "", options: str = "", notes: str = ''):
#        self.id = str(uuid.uuid4())
#        self.key = key
#        self.value = value
#        self.options = options
#        self.notes = notes
#
#    def add(self) -> None:
#        """
#        Adds a single object to the table.
#
#        Returns: None
#        """
#        s = database.newSession()
#        try:
#            s.add(self)
#            s.commit()
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add {self.key} to 'settings'. {e}")
#        finally:
#            s.close()
#
#    def remove(self) -> None:
#        """
#        Removes single object based on its ID value.
#
#        Returns: None
#        """
#        s = database.newSession()
#        try:
#            for d in s.query(Settings).filter(Settings.id == self.id):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            Logger().error(f"Failed to remove {self.key} from Settings table. {e}")
#        finally:
#            s.close()
#    
#    def clearTable(self) -> None:
#        """
#        Removes all the objects found in the Settings Table.
#
#        Returns: None
#        """
#        s = database.newSession()
#        try:
#            for d in s.query(Settings):
#                s.delete(d)
#            s.commit()
#        except Exception as e:
#            print(f"{e}")
#        finally:
#            s.close()
#
#    def findAllByKey(self) -> List:
#        """
#        Searches the database for objects that contain the Key value.
#        
#        Returns: List[Settings]
#        """
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(Settings).filter(Settings.key.contains(self.key)):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#            return l
#
#    def findSingleByKey(self) -> None:
#        """
#        Searches the database for objects that contain the Key value.
#        
#        Returns: Settings
#        """
#        s = database.newSession()
#        d = Settings()
#        try:
#            for d in s.query(Settings).filter(Settings.key.contains(self.key)):
#                pass
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#        
#        return d
#        
#    def __len__(self) -> int:
#        """
#        Returns the number of rows based off the Key value provided.
#
#        Returns: Int
#        """
#        s = database.newSession()
#        l = list()
#        try:
#            for res in s.query(Settings).filter(Settings.key == self.key):
#                l.append(res)
#        except Exception as e:
#            pass
#        finally:
#            s.close()
#
#        return len(l)
#
#class Logs(Base):
#    __tablename__ = 'logs'
#    id = Column('id', String, primary_key=True)
#    date = Column('date', String)
#    time = Column('time', String)
#    type = Column('type', String)
#    caller = Column('caller', String)
#    message = Column('message', String)
#
#    def __init__(self, date: str, time: str, type: str, caller: str, message: str):
#        self.id = str(uuid.uuid4())
#        self.date = date
#        self.time = time
#        self.type = type
#        self.caller = caller
#        self.message = message
#
#    def add(self) -> None:
#        s = database.newSession()
#        try:
#            s.add(self)
#            s.commit()
#        except FailedToAddToDatabase as e:
#            print(f"Failed to add '{self.message}' to 'Logs'. {e}")
#        finally:
#            s.close()