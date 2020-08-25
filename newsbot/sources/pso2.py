from newsbot import logger, env
from newsbot.sources.rssreader import RSSReader
from newsbot.tables import Sources, DiscordWebHooks
from newsbot.collections import RSSArticle, RSSRoot, RssArticleImages, RssArticleLinks
from newsbot.exceptions import UnableToFindContent
from bs4 import BeautifulSoup
from typing import List
import re
import requests


class PSO2Reader(RSSReader):
    def __init__(self) -> None:
        self.uri: str = "https://pso2.com/news"
        self.siteName: str = "Phantasy Star Online 2"
        self.links = list()
        self.hooks = list()

        self.checkEnv()
        pass

    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.uri
        rss.title = self.siteName

        for site in self.links:
            logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url
            page = self.getParser()

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
                    a.tags = bottom[1].text
                    a.pubDate = bottom[5].text

                    link = re.findall(
                        r"ShowDetails\('(.*?)'", bottom[7].attrs["onclick"],
                    )[0]
                    # tells us the news type and news link
                    cat = bottom[1].text.lower()
                    if " " in cat:
                        cat = cat.replace(" ", "-")

                    a.link = f"{self.uri}/{cat}/{link}"

                    rss.articles.append(a)
            except UnableToFindContent as e:
                logger.error(f"PSO2 - Unable to find articles. {e}")

        logger.debug(f"{site.name} - Finished collecting articles")
        return rss

    def findNewsLinks(self, page: BeautifulSoup) -> BeautifulSoup:
        try:
            news = page.find_all(
                "ul", {"class", "news-section all-news announcement-section active"}
            )
            if len(news) != 1:
                logger.error(
                    f"Collected results from news-section but got more results then expected."
                )

            return news
        except Exception as e:
            logger.error(
                f"Failed to find news-section.  Did the site layout change? {e}"
            )

    def findListItems(self, news: BeautifulSoup) -> BeautifulSoup:
        try:
            for article in news.find_all("li", {"class", "news-item all sr"}):
                print(article)
            pass
        except UnableToFindContent as e:
            logger.error(f"{e}")

    def checkEnv(self):
        res = Sources(name=self.siteName).findAllByName()
        if len(res) >= 1:
            for r in res:
                self.links.append(r)
            
            dwh = DiscordWebHooks(name=self.siteName).findAllByName()
            for r in dwh:
                self.hooks.append(r)
