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
#from newsbot import Base, database
from newsbot.sql import Base, database
from newsbot.sql.exceptions import FailedToAddToDatabase
from newsbot.sql.tables import ITables

class Icons(Base):
    __tablename__ = "icons"
    id = Column(String, primary_key=True)
    filename = Column(String)
    site = Column(String)

    def __init__(self,
        fileName: str = "",
        site: str = ""
        ) -> None:
        self.id = str(uuid.uuid4())
        self.filename = fileName
        self.site = site

    def add(self) -> None:
        s = database.newSession()

        try:
            s.add(self)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.site} to Icons table! {e}")
        finally:
            s.close()

    def update(self) -> None:
        #s = database.newSession()
        
        res = self.findAllByName()
        if len(res) == 0:
            self.add()
        elif res[0].site != self.site or res[0].filename != self.filename:
            self.remove()
            self.add()
        else:
            pass

    def remove(self) -> None:
        s = database.newSession()
        try:
            for d in s.query(Icons).filter(Icons.site == self.site):
                s.delete(d)
            s.commit()
        except Exception as e:
            print(f"{e}")
        finally:
            s.close()

    def clearTable(self) -> None:
        s = database.newSession()
        try:
            for d in s.query(Icons):
                s.delete(d)
            s.commit()
        except Exception as e:
            print(f"{e}")
        finally:
            s.close()

    def findAllByName(self) -> List:
        s = database.newSession()
        l = list()
        try:
            for res in s.query(Icons).filter(Icons.site.contains(self.site)):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()
            return l

    def __len__(self) -> int:
        """
        Returns the number of rows based off the Site value provided.

        Returns: Int
        """
        s = database.newSession()
        l = list()
        try:
            for res in s.query(Icons).filter(Icons.site == self.site):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)