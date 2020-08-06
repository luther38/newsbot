from newsbot import logger
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSArticle, RSSRoot, RssArticleImages, RssArticleLinks
from newsbot.exceptions import UnableToFindContent
from bs4 import BeautifulSoup
from typing import List
import re
import requests


class PSO2Reader(RSSReader):
    def __init__(self) -> None:
        self.logger = logger
        self.uri: str = "https://pso2.com/news"

        pass

    def getParser(self) -> BeautifulSoup:
        try:
            r = requests.get(self.uri)
        except Exception as e:
            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

        try:
            bs = BeautifulSoup(r.content, features="html.parser")
            return bs
        except Exception as e:
            self.logger.critical(f"failed to parse data returned from requests. {e}")

    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.uri

        rss.title = "Phantasy Star Online 2"

        page = self.getParser()
        # news = self.findNewsLinks(bs)
        try:
            for news in page.find_all("li", {"class", "news-item all sr"}):
                a = RSSArticle()
                a.siteName = "Phantasy Star Online 2"
                a.thumbnail = re.findall(
                    "url[(](.*?)[)]", news.contents[1].attrs["style"]
                )[0]

                nc = news.contents[3].contents
                a.title = nc[1].text
                a.description = nc[3].text

                bottom = nc[5].contents
                a.tags.append(bottom[1].text)
                a.pubDate = bottom[5].text

                link = re.findall(r"ShowDetails\('(.*?)'", bottom[7].attrs["onclick"],)[
                    0
                ]
                # tells us the news type and news link
                cat = bottom[1].text.lower()
                if " " in cat:
                    cat = cat.replace(" ", "-")

                a.link = f"{self.uri}/{cat}/{link}"

                rss.articles.append(a)
        except UnableToFindContent as e:
            self.logger.error(f"PSO2 - Unable to find articles. {e}")

        self.logger.debug("PSO2 - Finished collecting articles")
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
