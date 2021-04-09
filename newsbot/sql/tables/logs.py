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
from newsbot.sql import Base, database
from newsbot.sql.tables import iTables
from newsbot.sql.exceptions import FailedToAddToDatabase

class Logs(Base):
    __tablename__ = 'logs'
    id = Column('id', String, primary_key=True)
    date = Column('date', String)
    time = Column('time', String)
    type = Column('type', String)
    caller = Column('caller', String)
    message = Column('message', String)

    def __init__(self, date: str, time: str, type: str, caller: str, message: str):
        self.id = str(uuid.uuid4())
        self.date = date
        self.time = time
        self.type = type
        self.caller = caller
        self.message = message

    def add(self) -> None:
        s = database.newSession()
        try:
            s.add(self)
            s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add '{self.message}' to 'Logs'. {e}")
        finally:
            s.close()