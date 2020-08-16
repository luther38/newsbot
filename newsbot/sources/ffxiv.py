
from typing import List
import requests
from bs4 import BeautifulSoup
import re
from newsbot import logger, env
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSRoot, RSSArticle

class FFXIV(RSSReader):
    def __init__(self) -> None:
        self.uri: str = "https://na.finalfantasyxiv.com/lodestone/news/"
        self.baseUri: str = "https://na.finalfantasyxiv.com"
        self.siteName: str = "Final Fantasy XIV"
        self.settings = env.getFfxivValues()
        pass
    
    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.uri
        rss.title = self.siteName

        page = self.getParser()

        try:
            for news in page.find_all("li", {"class", "news__list--topics ic__topics--list"}):
                a = RSSArticle()
                a.siteName = self.siteName
                header = news.contents[0].contents
                body = news.contents[1].contents
                a.title = header[0].text
                a.link = f"{self.baseUri}{header[0].contents[0].attrs['href']}"
                #a.pubDate = header.contents[1].
                a.thumbnail = body[0].contents[0].attrs['src']
                a.description = body[0].contents[0].next_element.text

                rss.articles.append(a)

        except Exception as e:
            logger.error(e)

        return rss






