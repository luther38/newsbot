import enum
from typing import List
from sqlalchemy.orm.session import Session
from newsbot.core.constant import SourceName, SourceType
from newsbot.core.sql import database
from newsbot.core.sql import tables
from newsbot.core.sql.tables import ITables, Sources
from newsbot.core.sql.exceptions import FailedToAddToDatabase
 
class SourcesTable(ITables):
    def __init__(self, session: Session) -> None:
        self.setSession(session)
    
    def setSession(self, session: Session) -> None:
        self.s = session

    def __convertFromEnum__(self, item:Sources) -> Sources:
        t = item.source.__class__
        if t == SourceName:
            item.source = item.source.value
        
        try:
            item.type = item.type.value
        except:
            item.type = ''
        return item

    def __convertToEnum__(self, item: Sources) -> Sources:
        item.source = SourceName.fromString(item.source)
        item.type = SourceType.fromString(item.type)
        return item

    def __len__(self) -> int:
        l = list()
        try:
            for res in self.s.query(Sources):
                l.append(res)
        except Exception as e:
            pass
        return len(l)
    
    def clone(self, item: Sources) -> Sources:
        """
        Takes the given object and makes a new object without the Session info.
        """
        return Sources(
            id = item.id,
            name = item.name,
            source= item.source,
            type= item.type,
            value= item.value,
            enabled= item.enabled,
            url= item.url,
            tags=item.tags,
            fromEnv=item.fromEnv
        ) 

    def add(self, item: Sources, session: Session = '') -> None:
        if session != '':
            self.s = session      
        try:
            self.s.add(item)
            self.s.commit()
            self.s.close()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {item.name} to Source table! {e}")
    
    def update(self, item: Sources) -> None:
        try:
            exists = self.findByNameandSource(name=item.name, source=item.source)
            
            if exists.source != "":
                exists.name = item.name
                exists.source = item.source
                exists.type = item.type
                exists.value = item.value
                exists.enabled = item.enabled
                exists.url = item.url
                exists.tags = item.tags

                self.add(exists)
            else:
                self.add(item)

        except Exception as e:
            print(e)

    def updateId(self, id: str) -> None:
        raise NotImplementedError
        try:
            
            self.clearSingle(id=id)

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

    def findAllBySource(self, source: str) -> List[Sources]:
        hooks = list()
        try:
            for res in self.s.query(Sources).filter(Sources.source.contains(source)):
                hooks.append(self.__convertToEnum__(res))
                #hooks.append(res)
        except Exception as e:
            pass
        
        return hooks

    def findAll(self) -> List[Sources]:
        hooks = list()
        try:
            for res in self.s.query(Sources):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            return hooks

    def findAllBySource(self, source: str) -> List[Sources]:
        hooks = list()
        try:
            for res in self.s.query(Sources).filter(Sources.source.contains(source)):
                hooks.append(res)
        except Exception as e:
            pass
        return hooks

    def findAllByName(self, name: str ) -> List[Sources]:
        hooks = list()
        try:
            for res in self.s.query(Sources).filter(Sources.name.contains(name)):
                hooks.append(res)
        except Exception as e:
            pass
        return hooks

    def findById(self, id: str) -> Sources:
        try:
            for res in self.s.query(Sources).filter(Sources.id.contains(id)):
                return res
        except Exception as e:
            pass
        return None

    def findByName(self, name: str) -> Sources:
        try:
            for res in self.s.query(Sources).filter(Sources.name.contains(name)):
                return res
        except Exception as e:
            pass
        return Sources()

    def findByNameandSource(self, name: str, source: str) -> Sources:       
        try:
            for d in self.s.query(Sources).filter(
                Sources.name.contains(name),
                Sources.source.contains(source)
                ):
                return d
        except Exception as e:
            print(f'SQL Warning - Sources {e}')
            pass
        return Sources()

    def findBySourceNameType(self, source: str, name: str, type: str) -> Sources:
        hooks: List[Sources] = list()
        try:
            for res in self.s.query(Sources).filter(
                Sources.source.contains(source),
                Sources.name.contains(name),
                Sources.type.contains(type)
                ):
                return res
        except Exception as e:
            pass

        return Sources()

    def findBySourceAndName(self, source: str, name: str ) -> Sources:
        try:
            for res in self.s.query(Sources).filter(
                Sources.source.contains(source),
                Sources.name.contains(name)
                ):
                return res
        except Exception as e:
            pass

        return Sources()

    def findByNameSourceType(self, name: str, source: str, type:str ) -> Sources:
        try:
            for d in self.s.query(Sources).filter(
                Sources.name.contains(name),
                Sources.source.contains(source),
                Sources.type.contains(type)
                ):
                return d
        except Exception as e:
            pass
        return Sources()


    def clearTable(self) -> None:
        try:
            for d in self.s.query(Sources):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")

    def clearSingle(self, id: str) -> bool:
        """
        This will remove a single entry from the table by its ID value.
        """
        result: bool = False
        try:
            for i in self.s.query(Sources).filter(Sources.id == id):
                self.s.delete(i)
                self.s.commit()
                result = True
        except Exception as e:
            print(e)
        return result

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
        