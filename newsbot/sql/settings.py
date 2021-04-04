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
from newsbot.sql.exceptions import FailedToAddToDatabase

class Settings(Base, ITables):
    __tablename__ = 'settings'
    id = Column('id', String, primary_key=True)
    key = Column("key", String)
    value = Column("value", String)
    options = Column("options", String)
    notes = Column("notes", String)

    def __init__(self, key: str = "", value: str = "", options: str = "", notes: str = ''):
        self.id = str(uuid.uuid4())
        self.key = key
        self.value = value
        self.options = options
        self.notes = notes

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
            print(f"Failed to add {self.key} to 'settings'. {e}")
        finally:
            s.close()

    def remove(self) -> None:
        """
        Removes single object based on its ID value.

        Returns: None
        """
        s = database.newSession()
        try:
            for d in s.query(Settings).filter(Settings.id == self.id):
                s.delete(d)
            s.commit()
        except Exception as e:
            Logger().error(f"Failed to remove {self.key} from Settings table. {e}")
        finally:
            s.close()
    
    def clearTable(self) -> None:
        """
        Removes all the objects found in the Settings Table.

        Returns: None
        """
        s = database.newSession()
        try:
            for d in s.query(Settings):
                s.delete(d)
            s.commit()
        except Exception as e:
            print(f"{e}")
        finally:
            s.close()

    def findAllByKey(self) -> List:
        """
        Searches the database for objects that contain the Key value.
        
        Returns: List[Settings]
        """
        s = database.newSession()
        l = list()
        try:
            for res in s.query(Settings).filter(Settings.key.contains(self.key)):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return l

    def findSingleByKey(self) -> None:
        """
        Searches the database for objects that contain the Key value.
        
        Returns: Settings
        """
        s = database.newSession()
        d = Settings()
        try:
            for d in s.query(Settings).filter(Settings.key.contains(self.key)):
                pass
        except Exception as e:
            pass
        finally:
            s.close()
        
        return d
        
    def __len__(self) -> int:
        """
        Returns the number of rows based off the Key value provided.

        Returns: Int
        """
        s = database.newSession()
        l = list()
        try:
            for res in s.query(Settings).filter(Settings.key == self.key):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)