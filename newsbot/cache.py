
from newsbot.tables import Settings

class Cache():
    def __init__(self, key: str, value: str = '') -> None:
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

class iCache():
    def __init__(self):
        pass
    
    def find(self, key: str) -> str:
        raise NotImplementedError

    def add(self, key: str, value: str) -> str:
        raise NotImplementedError

    def remove(self, key: str) -> None:
        raise NotImplementedError

class SqlCache(iCache):
    """
    This is an implementation of basic cashing with sql.
    Do not use this class directly.  
    Always use Cache class and it will find the data as needed.
    """
    def __init__(self):
        pass

    def find(self, key: str) -> str:
        res: Settings = Settings(key=key).findSingleByKey()
        return res.value

    def add(self, key: str, value: str) -> str:
        Settings(key=key, value=value).add()
        return value

    def remove(self, key: str) -> None:
        Settings(key=key).remove()
