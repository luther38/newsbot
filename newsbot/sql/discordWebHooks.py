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
#from newsbot import Base, database
from newsbot.db import Base
from newsbot import database
from newsbot.sql.exceptions import FailedToAddToDatabase
from newsbot.sql import ITables


class DiscordWebHooks(Base, ITables):
    __tablename__ = "discordwebhooks"
    id = Column(String, primary_key=True)
    name = Column(String)
    key = Column(String)
    url = Column(String)
    server = Column(String)
    channel = Column(String)
    enabled = Column(Boolean)

    def __init__(self, name:str="", key:str="", server:str = "", channel:str = "", url: str = "") -> None:
        self.id = str(uuid.uuid4())
        self.name = name
        self.key = key
        self.url = url
        self.server = server
        self.channel = channel
        self.enabled = True

    def add(self) -> None:
        s = database.newSession()
        h = DiscordWebHooks()
        h.key = self.key
        h.url = self.url
        h.name = self.name
        h.server = self.server
        h.channel = self.channel
        h.enabled = self.enabled
        try:
            s.add(self)
            s.commit()
            # print(f"'{self.name}' was added to the Discord queue")
        except Exception as e:
            print(f"Failed to add {self.name} to DiscordWebHook table! {e}")
        finally:
            s.close()

    def update(self) -> bool:
        s = database.newSession()
        self.clearSingle()
        DiscordWebHooks(
            name=self.name
            ,key=self.key
            ,server=self.server
            ,channel=self.channel
            ,url=self.url
        ).add()

    def clearTable(self) -> None:
        s = database.newSession()
        try:
            for d in s.query(DiscordWebHooks):
                s.delete(d)
            s.commit()
        except Exception as e:
            print(f"{e}")
        finally:
            s.close()

    def clearSingle(self) -> bool:
        """
        This will remove a single entry from the table by its ID value.
        """
        s = database.newSession()
        result: bool = False
        try:
            for i in s.query(DiscordWebHooks).filter(DiscordWebHooks.id == self.id):
                s.delete(i)
                s.commit()
                result = True
        except Exception as e:
            print(e)
        finally:
            s.close()
            return result

    def findById(self) -> object:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks).filter(
                DiscordWebHooks.id.contains(self.id)
            ):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks[0]

    def findAllByName(self) -> List:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks).filter(
                DiscordWebHooks.name.contains(self.name)
            ):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks

    def findAll(self) -> List:
        s= database.newSession()
        #s = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks

    def __len__(self) -> int:
        s = database.newSession()
        l = list()
        try:
            for res in s.query(DiscordWebHooks):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)
