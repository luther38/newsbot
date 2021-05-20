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

from sqlalchemy.orm.session import Session
from newsbot.core.sql import database, Base
from newsbot.core.sql.tables import Articles, ITables
from newsbot.core.sql.exceptions import FailedToAddToDatabase
from json import dumps

class Sources(Base, ITables):
    # database = DB(Base)
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

    def toJson(self, item: object) -> str:
        d = {
            'id': item.id,
            'name': item.name,
            'source': item.source,
            'type': item.type,
            'value': item.value,
            'enabled': item.enabled,
            'url': item.url,
            'tags': item.tags,
            "fromEnv": item.fromEnv
        }
        print(d)

    def add(self) -> None:
        s = database.newSession()
        # h = Sources()
        # h.name = self.name
        # h.url = self.url
        # h.enabled = self.enabled
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
            exists = Sources(name=self.name, source=self.source).findBySourceAndName()
            if exists.source != None:
                key = exists.id
                exists.clearSingle()

            d = Sources(
                name=self.name,
                source=self.source,
                url=self.url,
                type=self.type,
                value=self.value,
                tags=self.tags,
                enabled=self.enabled,
                fromEnv=self.fromEnv
            )
            if key != "":
                d.id = key

            d.add()
        except Exception as e:
            print(f"Failed to update")
            print(e)
            pass

    def updateId(self, id: str) -> None:
        s = database.newSession()
        try:
            Sources(id=id).clearSingle()
            d = Sources(
                name=self.name,
                source=self.source,
                url=self.url,
                type=self.type,
                value=self.value,
                tags=self.tags,
                enabled=self.enabled,
                fromEnv=self.fromEnv
            )
            d.id = id
            d.add()
        except Exception as e:
            print(f"Failed to update")
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
            for res in s.query(Sources).filter(Sources.name.contains(self.name)):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            if len(hooks) == 0:
                return None
            else:
                return hooks[0]

    def findById(self) -> object:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources).filter(
                    Sources.id.contains(self.id)):
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

    def findAllBySource(self) -> List:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources).filter(Sources.source.contains(self.source)):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks
    
    def findBySourceAndName(self) -> object:
        s = database.newSession()
        hooks: List[Sources] = list()
        try:
            for res in s.query(Sources).filter(
                Sources.source.contains(self.source),
                Sources.name.contains(self.name)
                ):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            if len(hooks) >= 1:
                return hooks[0]
            else:
                return Sources()

    def findBySourceNameType(self) -> object:
        s = database.newSession()
        hooks: List[Sources] = list()
        try:
            for res in s.query(Sources).filter(
                Sources.source.contains(self.source),
                Sources.name.contains(self.name),
                Sources.type.contains(self.type)
                ):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks[0]

    def findAll(self) -> List:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources):
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

class SourceTableFind():
    def findAllBySource(self, source: str) -> List[Sources]:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources).filter(Sources.source.contains(source)):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks    

    def findAll(self) -> List[Sources]:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return hooks

    def findById(self) -> Sources:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(Sources).filter(
                    Sources.id.contains(self.id)):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            if len(hooks) == 0:
                return None
            else:
                return hooks[0]

class SourceTableConvert():
    def toListDict(self, items: List[Sources]) -> List[dict]:
        l = list()
        for i in items:
            l.append(self.toDict(i))
        return l

    def toDict(self, item: Sources) -> dict:
        d = {
            'id': item.id,
            'name': item.name,
            'source': item.source,
            'type': item.type,
            'value': item.value,
            'enabled': item.enabled,
            'url': item.url,
            'tags': item.tags,
            "fromEnv": item.fromEnv
        }
        return d

class SourcesTable(ITables, SourceTableFind, SourceTableConvert):
    def add(self, item: Sources) -> None:
        s = database.newSession()
        try:
            s.add(item)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {item.name} to Source table! {e}")
        finally:
            s.close()