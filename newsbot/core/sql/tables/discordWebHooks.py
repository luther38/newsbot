from typing import List
from sqlalchemy.orm.session import Session
from werkzeug.datastructures import UpdateDictMixin
from newsbot.core.sql import database
from newsbot.core.sql.tables import ITables, DiscordWebHooks
from newsbot.core.sql.exceptions import FailedToAddToDatabase

class DiscordWebHooksTable(ITables):
    def __init__(self) -> None:
        self.s = database.newSession()

    def add(self, item:DiscordWebHooks) -> bool:
        try:
            self.s.add(item)
            self.s.commit()
            return True
        except Exception as e:
            print(f"Failed to add {item.name} to DiscordWebHook table! {e}")
            return False

    def findAll(self) -> List[DiscordWebHooks]:
        hooks = list()
        try:
            for res in self.s.query(DiscordWebHooks):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            return hooks

    def findAllByName(self, name: str) -> List[DiscordWebHooks]:
        hooks = list()
        try:
            for res in self.s.query(DiscordWebHooks).filter(DiscordWebHooks.name == name):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            return hooks

    def findById(self, id: str) -> DiscordWebHooks:
        try:
            for res in self.s.query(DiscordWebHooks).filter(DiscordWebHooks.id == id):
                return res
        except Exception as e:
            pass
        return None

    def findByName(self, name: str ) -> DiscordWebHooks:
        try:
            for res in self.s.query(DiscordWebHooks).filter(DiscordWebHooks.name == name):
                return res
        except Exception as e:
            pass
        
        return DiscordWebHooks()

    def findByUrl(self,url: str ) -> DiscordWebHooks:
        try:
            for res in self.s.query(DiscordWebHooks).filter(DiscordWebHooks.url == url):
                return res
        except Exception as e:
            pass
        return None

    def findByServer(self, server: str) -> DiscordWebHooks:
        try:
            for res in self.s.query(DiscordWebHooks).filter(DiscordWebHooks.server == server):
                return res
        except Exception as e:
            pass
        return None

    def delete(self, id: str = '') -> bool:
        if id != "":
            return self.deleteById(id=id)

    def deleteById(self, id: str) -> None:
        try:
            for d in self.s.query(DiscordWebHooks).filter(DiscordWebHooks.id == id):
                self.s.delete(d)
            self.s.commit()
            status = True
        except Exception as e:
            print(f"{e}")
            status = False
        finally:
            return status

    def update(self, updateWith: DiscordWebHooks, id: str = '') -> bool:
        if id != '':
            return self.updateById(updateWith=updateWith, id = id)
        else:
            raise Exception("Failed to update a record because no value was given to query.")

    def updateById(self, updateWith: DiscordWebHooks, id: str) -> bool:
        self.deleteById(id)
        self.add(updateWith)
            
    def toListDict(self, items: List[DiscordWebHooks]) -> List[dict]:
        l = list()
        for i in items:
            l.append(self.toDict(i))
        return l

    def __generateName__(self, server: str, channel: str) -> str:
        return f"{server} - {channel}"

    #def __exit__(self) -> None:
    #    self.s.close()

    def __len__(self) -> int:
        l = list()
        try:
            for res in self.s.query(DiscordWebHooks):
                l.append(res)
        except Exception as e:
            pass
        return len(l)

    def toDict(self, item: DiscordWebHooks) -> dict:
        d = {
            'id': item.id,
            'name': item.name,
            'server': item.server,
            'channel': item.channel,
            'url': item.url,
            "fromEnv": item.fromEnv
        }
        return d

