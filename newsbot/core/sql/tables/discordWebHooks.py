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
from typing import ClassVar, List
from sqlalchemy.orm.session import Session
from newsbot.core.sql import database, Base
from newsbot.core.sql.tables import Articles, ITables
from newsbot.core.sql.exceptions import FailedToAddToDatabase



class DiscordWebHooks(Base, ITables):
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
        self.id = str(uuid.uuid4())
        self.server = server
        self.channel = channel
        if name == "":  self.name = self.__generateName__()
        else:           self.name = name
        self.key = key
        self.url = url
        self.enabled = True
        self.fromEnv: bool = fromEnv

    def add(self) -> None:
        s: Session = database.newSession()
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
        # s: Session = database.newSession()
        key = ""
        try:
            nameExists = DiscordWebHooks(name=self.name).findByName()
            urlExists = DiscordWebHooks(url=self.url).findByUrl()
            if nameExists != None:
                key = nameExists.id
                urlExists.clearSingle()
            elif urlExists != None:
                key = urlExists.id
                urlExists.clearSingle()

            d = DiscordWebHooks(
                name=self.name,
                key=self.key,
                server=self.server,
                channel=self.channel,
                url=self.url,
                fromEnv=self.fromEnv
            )
            if key != "":
                d.id = key

            d.add()
        except Exception as e:
            print(e)
            pass

    def clearTable(self) -> None:
        s: Session = database.newSession()
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
        s: Session = database.newSession()
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
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks).filter(DiscordWebHooks.id == self.id):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            if len(hooks) == 0:
                return None
            else:
                return hooks[0]

    def findByName(self) -> object:
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks).filter(
                DiscordWebHooks.name == self.name
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

    def findByServer(self) -> object:
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks).filter(
                DiscordWebHooks.server == self.server
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

    def findByUrl(self) -> object:
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(DiscordWebHooks).filter(DiscordWebHooks.url == self.url):
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
        s: Session = database.newSession()
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
        s: Session = database.newSession()
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
        s: Session = database.newSession()
        l = list()
        try:
            for res in s.query(DiscordWebHooks):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)

    def __generateName__(self) -> str:
        return f"{self.server} - {self.channel}"
