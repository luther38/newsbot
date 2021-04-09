from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    create_engine,
    Binary,
)
import uuid
from typing import List
from newsbot.sql import Base, database
from newsbot.sql.tables import ITables
from newsbot.sql.exceptions import FailedToAddToDatabase

class SourceLinks(Base, ITables):
    __tablename__ = 'sourcelinks'
    id = Column('id', String, primary_key=True)
    name: str = Column("name", String)
    sourceID: str = Column("sourceID", String)
    discordID: str = Column("discordID", String)
    
    def __init__(self, name: str = "", sourceID: str = "", discordID: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.sourceID = sourceID
        self.discordID = discordID

    def add(self) -> None:
        """
        Adds a single object to the table.
        Returns: None
        """
        s = database.newSession()
        try:
            s.add(self)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.name} to 'SourceLinks'. {e}")
        finally:
            s.close()

    def update(self) -> bool:
        s = database.newSession()
        key = ""
        try:
            exists = SourceLinks(name=self.name).findByName()
            if exists != None:
                key = exists.id 
                exists.clearSingle()

            d = SourceLinks(
                name=self.name, sourceID=self.sourceID, discordID=self.discordID 
            )
            if key != "":
                d.id = key

            d.add()
        except Exception as e:
            print(e)
            pass

    def remove(self) -> None:
        """
        Removes single object based on its ID value.
        Returns: None
        """
        s = database.newSession()
        try:
            for d in s.query(SourceLinks).filter(SourceLinks.id == self.id):
                s.delete(d)
            s.commit()
        except Exception as e:
            Logger().error(f"Failed to remove {self.name} from SourceLinks table. {e}")
        finally:
            s.close()
    
    def clearTable(self) -> None:
        """
        Removes all the objects found in the SourceLinks Table.

        Returns: None
        """
        s = database.newSession()
        try:
            for d in s.query(SourceLinks):
                s.delete(d)
            s.commit()
        except Exception as e:
            print(f"{e}")
        finally:
            s.close()

    def findByName(self) -> object:
        s = database.newSession()
        hooks = list()
        try:
            for res in s.query(SourceLinks).filter(
                SourceLinks.name.contains(self.name)
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

    def findAllByname(self) -> List:
        """
        Searches the database for objects that contain the name value.
        
        Returns: List[SourceLinks]
        """
        s = database.newSession()
        l = list()
        try:
            for res in s.query(SourceLinks).filter(SourceLinks.name.contains(self.name)):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return l

    def findSingleByname(self) -> None:
        """
        Searches the database for objects that contain the name value.
        
        Returns: SourceLinks
        """
        s = database.newSession()
        d = SourceLinks()
        try:
            for d in s.query(SourceLinks).filter(SourceLinks.name.contains(self.name)):
                pass
        except Exception as e:
            pass
        finally:
            s.close()
        
        return d
        
    def __len__(self) -> int:
        """
        Returns the number of rows based off the name value provided.

        Returns: Int
        """
        s = database.newSession()
        l = list()
        try:
            for res in s.query(SourceLinks).filter(SourceLinks.name == self.name):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)
        