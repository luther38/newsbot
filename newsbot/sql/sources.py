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
from newsbot.sql import ITables
from newsbot.sql.exceptions import *

class Sources(Base, ITables):
    __tablename__ = "sources"
    id = Column(String, primary_key=True)
    name = Column(String)
    url = Column(String)
    enabled = Column(Boolean)

    def __init__(self, name="", url="") -> None:
        self.id = str(uuid.uuid4())
        self.name = name
        self.url = url
        self.enabled = True

    def add(self) -> None:
        s = database.newSession()
        h = Sources()
        h.name = self.name
        h.url = self.url
        h.enabled = self.enabled
        try:
            s.add(self)
            s.commit()
            # print(f"'{self.name}' was added to the Discord queue")
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.name} to DiscordWebHook table! {e}")
        finally:
            s.close()

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

