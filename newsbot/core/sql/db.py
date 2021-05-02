from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import sqlalchemy
import os

Base = declarative_base()


class DB:
    def __init__(self, Base):
        name = self.__getDbName__()
        uri: str = f"sqlite:///mounts/database/{name}"
        self.engine = create_engine(uri)
        # context.configure(connection=self.engine)
        # try:
        #    context.run_migrations
        self.session: sessionmaker = sessionmaker()
        self.session.configure(bind=self.engine)
        self.Base = Base
        self.Base.metadata.create_all(self.engine)

    def newSession(self) -> Session:
        return self.session()

    def __getDbName__(self) -> str:
        name = os.getenv("NEWSBOT_DATABASE_NAME")
        if name == None:
            return "newsbot.db"
        else:
            return name


database = DB(Base)
