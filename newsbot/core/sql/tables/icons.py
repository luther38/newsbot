from typing import List
from sqlalchemy.orm.session import Session
from newsbot.core.sql import database
from newsbot.core.sql.tables import ITables, Icons
from newsbot.core.sql.exceptions import FailedToAddToDatabase

class IconsTable():
    def __init__(self, session: Session) -> None:
        self.setSession(session)

    def setSession(self, session: Session) -> None:
        self.s = session

    def __len__(self, site: str) -> int:
        """
        Returns the number of rows based off the Site value provided.
        Returns: Int
        """
        l = list()
        try:
            for res in self.s.query(Icons).filter(Icons.site == site):
                l.append(res)
        except Exception as e:
            pass
        return len(l)

    def add(self, item: Icons) -> None:
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.site} to Icons table! {e}")
        
    def update(self, item: Icons) -> None:
        res = self.findAllByName(site=item.site)
        if len(res) == 0:
            self.add(item)
        elif res[0].site != item.site or res[0].filename != item.filename:
            self.remove(item.site)
            self.add(item)
        else:
            pass

    def remove(self, site: str) -> None:
        try:
            for d in self.s.query(Icons).filter(Icons.site == site):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")

    def clearTable(self) -> None:
        try:
            for d in self.s.query(Icons):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")
        
    def findAllByName(self, site: str) -> List[Icons]:
        l = list()
        try:
            for res in self.s.query(Icons).filter(Icons.site.contains(site)):
                l.append(res)
        except Exception as e:
            pass
        return l