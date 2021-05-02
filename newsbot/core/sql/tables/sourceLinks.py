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

from sqlalchemy.orm.session import Session
from newsbot.core.sql import database, Base
from newsbot.core.sql.tables import Articles, ITables
from newsbot.core.sql.exceptions import FailedToAddToDatabase



class SourceLinks(Base, ITables):
    __tablename__ = "sourcelinks"
    id = Column("id", String, primary_key=True)
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
        s: Session = database.newSession()
        try:
            s.add(self)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.name} to 'SourceLinks'. {e}")
        finally:
            s.close()

    def update(self) -> None:
        """
        This looks for at the name column to find an existing record.
        If it does not find a record, it will look up based off the SourceID given to see if something exists for that source.
        """
        # s: Session = database.newSession()
        key = ""
        try:
            exists = SourceLinks(name=self.name).findByName()
            sourceId = SourceLinks(sourceID=self.sourceID).findBySourceID()

            if exists != None:
                key = exists.id
                exists.clearSingle()
            elif sourceId != None:
                if sourceId.name == self.name:
                    key = sourceId.id
                    sourceId.clearSingle()

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

    def clearSingle(self) -> bool:
        """
        This will remove a single entry from the table by its ID value.
        """
        s: Session = database.newSession()
        result: bool = False
        try:
            for i in s.query(SourceLinks).filter(SourceLinks.id == self.id):
                s.delete(i)
                s.commit()

                result = True
        except Exception as e:
            print(e)
        finally:
            s.close()
            return result

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
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(SourceLinks).filter(SourceLinks.name == self.name):
                hooks.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            if len(hooks) == 0:
                return None
            else:
                return hooks[0]

    def findBySourceID(self) -> object:
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(SourceLinks).filter(
                SourceLinks.sourceID == self.sourceID
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

    def findByDiscordID(self) -> object:
        s: Session = database.newSession()
        hooks = list()
        try:
            for res in s.query(SourceLinks).filter(
                SourceLinks.discordID == self.discordID
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
        """
        Searches the database for objects that contain the name value.
        
        Returns: List[SourceLinks]
        """
        s = database.newSession()
        l = list()
        try:
            for res in s.query(SourceLinks).filter(
                SourceLinks.name.contains(self.name)
            ):
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
