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
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import sqlalchemy
import uuid
from dotenv import load_dotenv
from pathlib import Path
import os

Base = declarative_base()


class Articles(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True)
    title = Column(String)
    url = Column(String)
    pubDate = Column(String)

    def __init__(self) -> None:
        self.id = str(uuid.uuid4())


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
