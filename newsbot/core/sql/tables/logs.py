from newsbot.core.sql import database
from newsbot.core.sql.tables import ITables, Logs
from newsbot.core.sql.exceptions import FailedToAddToDatabase

class LogsTable():
    def __init__(self) -> None:
        self.s = database.newSession()
    #def __exit__(self) -> None:
    #    self.s.close()

    def add(self, item: Logs) -> None:
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add '{item.message}' to 'Logs'. {e}")
