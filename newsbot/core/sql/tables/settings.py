from typing import List

from sqlalchemy.orm.session import Session
from newsbot.core.sql import database
from newsbot.core.sql.tables import ITables, Settings
from newsbot.core.sql.exceptions import FailedToAddToDatabase

class SettingsTable():
    def __init__(self, session: Session) -> None:
        self.setSession(session)

    def setSession(self, session: Session) -> None:
        self.s = session
    
    def __len__(self, key: str) -> int:
        """
        Returns the number of rows based off the Key value provided.
        Returns: Int
        """
        l = list()
        try:
            for res in self.s.query(Settings).filter(Settings.key == key):
                l.append(res)
        except Exception as e:
            pass
        return len(l)

    def add(self, item: Settings) -> None:
        """
        Adds a single object to the table.
        Returns: None
        """
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.key} to 'settings'. {e}")

    def remove(self, id: str) -> None:
        """
        Removes single object based on its ID value.

        Returns: None
        """
        try:
            for d in self.s.query(Settings).filter(Settings.id == id):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            Logger().error(f"Failed to remove {self.key} from Settings table. {e}")

    def clearTable(self) -> None:
        """
        Removes all the objects found in the Settings Table.
        Returns: None
        """
        try:
            for d in self.s.query(Settings):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")

    def findAllByKey(self, key: str ) -> List[Settings]:
        """
        Searches the database for objects that contain the Key value.
        
        Returns: List[Settings]
        """
        l = list()
        try:
            for res in self.s.query(Settings).filter(Settings.key.contains(key)):
                l.append(res)
        except Exception as e:
            pass
        return l

    def findSingleByKey(self, key: str ) -> Settings:
        """
        Searches the database for objects that contain the Key value.        
        Returns: Settings
        """
        try:
            for d in self.s.query(Settings).filter(Settings.key.contains(key)):
                return d
        except Exception as e:
            pass
        return Settings()
