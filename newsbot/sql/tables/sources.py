import typing
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
from newsbot.sql import Base, database
from newsbot.sql.tables import ITables
from newsbot.sql.exceptions import *

class Sources(Base, ITables):
    #database = DB(Base)
    __tablename__ = "sources"
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    source: str = Column(String)
    type: str = Column(String)
    value: str = Column(String)
    enabled: bool = Column(Boolean)
    url: str = Column(String)
    tags: str = Column(String)

    def __init__(self, 
        name: str = "", source: str = "",type: str = ""
        ,value: str = "", enabled: bool = True, url: str = ""
        ,tags: str = ""
        ) -> None:
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.source: str = source
        self.type: str = type
        self.value: str = value
        self.enabled: bool = True
        self.url: str = url
        self.tags: str = tags

    def add(self) -> None:
        s = database.newSession()
        #h = Sources()
        #h.name = self.name
        #h.url = self.url
        #h.enabled = self.enabled
        try:
            s.add(self)
            s.commit()
            # print(f"'{self.name}' was added to the Discord queue")
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.name} to DiscordWebHook table! {e}")
        finally:
            s.close()

    def update(self) -> None:
        s = database.newSession()
        key = ""
        try:
            exists = Sources(name=self.name).findByName()
            if exists != None:
                key = exists.id 
                exists.clearSingle()

            d = Sources(name=self.name, source=self.source, url=self.url )
            if key != "":
                d.id = key

            d.add()
        except Exception as e:
            print(e)
            pass

    def clearTable(self) -> None:
        s = database.newSession()
        try:
            for d in s.query(Sources):
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
            for i in s.query(Sources).filter(Sources.id == self.id):
                s.delete(i)
                s.commit()
                result = True
        except Exception as e:
            print(e)
        finally:
            s.close()
            return result

    def findByName(self) -> object:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources).filter(
                Sources.name.contains(self.name)
            ):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            if len(hooks) == 0:
                return None
            else:
                return hooks[0]

    def findAllByName(self) -> List:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources).filter(Sources.name.contains(self.name)):
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
            for res in s.query(Sources):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)

