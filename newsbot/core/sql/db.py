from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import sqlalchemy
import os

Base = declarative_base()

class DB:
    def __init__(self, Base):
        name = self.__getDbName__()
        uri: str = ""
        if name == "unittest":
            uri = "sqlite://"
        else:
            uri = f"sqlite:///mounts/database/{name}"
        self.engine = create_engine(uri)
        self.session: sessionmaker = sessionmaker()
        self.session.configure(bind=self.engine)
        self.Base = Base
        self.Base.metadata.create_all(self.engine)

    def newSession(self) -> Session:
        return self.session()

    def __getDbName__(self) -> str:
        name = os.getenv("NEWSBOT_DATABASE_NAME")
        mode = os.getenv("NEWSBOT_MODE")
        if name == None:
            return "newsbot.db"
        elif mode == "unittest":
            return ":memory:"
        else:
            return name


database = DB(Base)
