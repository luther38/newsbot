from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import sqlalchemy

Base = declarative_base()


class DB:
    def __init__(self, Base):
        uri: str = f"sqlite:///newsbot.db"
        self.engine = create_engine(uri)
        self.session: sessionmaker = sessionmaker()
        self.session.configure(bind=self.engine)
        self.Base = Base
        self.Base.metadata.create_all(self.engine)

    def newSession(self) -> Session:
        return self.session()