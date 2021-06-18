from newsbot.core.sql import database
from newsbot.core.sql.exceptions import FailedToAddToDatabase
from newsbot.core.sql.tables import Articles

class ArticlesTable():
    def __init__(self) -> None:
        self.s =database.newSession()
        
    #def __exit__(self) -> None:
    #    self.s.close()

    def __len__(self) -> int:
        i: int = 0
        try:
            for res in self.s.query(Articles):
                i = i + 1
        except Exception as e:
            pass
        return len(i)

    def __len__(self, siteName: str ) -> int:
        """
        Returns the number of rows based off the SiteName value provieded.
        """

        s = database.newSession()
        l = list()
        try:
            for res in s.query(Articles).filter(Articles.siteName == self.siteName):
                l.append(res)
        except Exception as e:
            pass
        finally:
            s.close()

        return len(l)

    def add(self, item: Articles) -> None:
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {item.name} to Source table! {e}")

    def exists(self, url: str) -> bool:
        """
        Check to see if the current record exists.
        """
        try:
            for res in self.s.query(Articles).filter(Articles.url == url):
                return True
        except Exception as e:
            pass
        return False