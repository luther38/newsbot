from abc import ABC, abstractclassmethod
from newsbot.core.sql.tables import Settings, SettingsTable

class Cache:
    def __init__(self, key: str, value: str = "") -> None:
        self.sql: iCache = SqlCache()
        self.key = key
        self.value = value

    def find(self) -> str:
        return self.sql.find(self.key)

    def add(self) -> str:
        self.sql.add(self.key, self.value)
        return self.value

    def remove(self) -> None:
        self.sql.remove(self.key)


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

    def __init__(self):
        #self.table = SettingsTable()
        pass

    def find(self, key: str) -> str:
        res = SettingsTable().findSingleByKey(key=key)
        return res.value

    def add(self, key: str, value: str) -> str:
        SettingsTable().add(Settings(key=key, value=value))
        return value

    def remove(self, key: str) -> None:
        SettingsTable().remove(key=key)
        
