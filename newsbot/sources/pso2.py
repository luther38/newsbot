
from newsbot import logger
from newsbot.sources.rssreader import RSSReader
from newsbot.html import Html
from newsbot.collections import RSSArticle, RSSRoot, RssArticleImages, RssArticleLinks
from newsbot.exceptions import UnableToFindContent
from bs4 import BeautifulSoup
from typing import List
import re
import requests


class PSO2Reader(RSSReader):
    def __init__(self) -> None:
        self.logger = logger

        self.uriAnnouncements: str = "https://pso2.com/news/announcements"
        self.uriScratch: str = "https://pso2.com/news/scratch-tickets"

        pass

    def getParser(self) -> BeautifulSoup:
        try:
            r = requests.get(self.uriAnnouncements)
        except Exception as e:
            # TODO Logger
            print(f"Failed to collect data from {self.uriAnnouncements}. {e}")

        try:
            bs = BeautifulSoup(r.content, features="html.parser")
            return bs
        except Exception as e:
            # TODO Logger
            print(f"failed to parse data returned from requests. {e}")

    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.uriAnnouncements
        rss.title = "Phantasy Star Online 2 - Announcements"

        page = self.getParser()
        #news = self.findNewsLinks(bs)
        try:
            for news in page.find_all("li", {"class", "news-item all sr"}):
                a = RSSArticle()
                a.thumbnail = re.findall(
                    "url[(](.*?)[)]", news.contents[1].attrs["style"]
                )[0]
                a.title = news.contents[3].contents[1].text
                a.description = news.contents[3].contents[3].text
                a.pubDate = news.contents[3].contents[5].contents[5].text

                link = re.findall(
                    r"ShowDetails\('(.*?)'",
                    news.contents[3].contents[5].contents[7].attrs["onclick"],
                )
                a.link = f"{self.uriAnnouncements}/{link[0]}"
                rss.articles.append(a)
        except UnableToFindContent as e:
            self.logger.error(f"PSO2 - Unable to find articles. {e}")
        
        return rss


    def findNewsLinks(self, page: BeautifulSoup) -> BeautifulSoup:
        try:
            news = page.find_all(
                "ul", {"class", "news-section all-news announcement-section active"}
            )
            if len(news) != 1:
                self.logger.error(
                    f"Collected results from news-section but got more results then expected."
                )

            return news
        except Exception as e:
            self.logger.error(
                f"Failed to find news-section.  Did the site layout change? {e}"
            )

    def findListItems(self, news: BeautifulSoup) -> BeautifulSoup:
        try:
            for article in news.find_all("li", {"class", "news-item all sr"}):
                print(article)
            pass
        except UnableToFindContent as e:
            self.logger.error(f"{e}")


