from abc import ABC, abstractclassmethod

from sqlalchemy.orm.session import Session
from newsbot.core.sql.tables import Settings, SettingsTable

class Cache:
    def __init__(self, session: Session) -> None:
        self.sql: iCache = SqlCache(session=session)

    def find(self, key: str) -> str:
        return self.sql.find(key)

    def add(self, key: str, value: str) -> str:
        self.sql.add(key, value)
        return value

    def remove(self, key: str) -> None:
        self.sql.remove(key)


class iCache(ABC):
    def __init__(self):
        pass
    
    @abstractclassmethod
    def find(self, key: str) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def add(self, key: str, value: str) -> str:
        raise NotImplementedError

    @abstractclassmethod
    def remove(self, key: str) -> None:
        raise NotImplementedError


class SqlCache(iCache):
    """
    This is an implementation of basic cashing with sql.
    Do not use this class directly.  
    Always use Cache class and it will find the data as needed.
    """

    def __init__(self, session: Session):
        self.session: Session = session
        pass

    def find(self, key: str) -> str:
        res = SettingsTable(session=self.session).findSingleByKey(key=key)
        return res.value

    def add(self, key: str, value: str) -> str:
        SettingsTable(session=self.session).add(Settings(key=key, value=value))
        return value

    def remove(self, key: str) -> None:
        SettingsTable(session=self.session).remove(key=key)
        
