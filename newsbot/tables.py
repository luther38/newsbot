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
from newsbot import Base, database
from newsbot.collections import RSSArticle


class Articles(Base):
    __tablename__ = "articles"
    id = Column(String, primary_key=True)
    siteName = Column(String)
    tags = Column(String)
    title = Column(String)
    url = Column(String)
    pubDate = Column(String)

    def __init__(self, article: RSSArticle = RSSArticle()) -> None:
        self.id = str(uuid.uuid4())
        self.convertRssArticle(article)

    def convertRssArticle(self, article: RSSArticle) -> None:
        self.title = article.title
        self.siteName = article.siteName
        self.pubDate = article.pubDate
        self.tags = article.tags
        self.url = article.link
