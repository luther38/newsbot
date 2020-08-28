from typing import List
import requests
from bs4 import BeautifulSoup
import re
from newsbot import logger, env
from newsbot.tables import Articles, Sources, DiscordWebHooks
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSRoot, RSSArticle


class FFXIVReader(RSSReader):
    def __init__(self) -> None:
        self.uri: str = "https://na.finalfantasyxiv.com/lodestone/news/"
        self.baseUri: str = "https://na.finalfantasyxiv.com"
        self.siteName: str = "Final Fantasy XIV"
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

            if "Topics" in site.name:
                try:
                    for news in page.find_all(
                        "li", {"class", "news__list--topics ic__topics--list"}
                    ):
                        a = RSSArticle()
                        a.siteName = self.siteName
                        header = news.contents[0].contents
                        body = news.contents[1].contents
                        a.title = header[0].text
                        a.link = f"{self.baseUri}{header[0].contents[0].attrs['href']}"
                        a.thumbnail = body[0].contents[0].attrs["src"]
                        a.description = body[0].contents[0].next_element.text
                        a.tags = "Topics"
                        rss.articles.append(a)
                except Exception as e:
                    logger.error(f"Failed to collect Topics from FFXIV. {e}")

            if "Notices" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__info--list"}
                    ):
                        a = RSSArticle()
                        a.siteName = self.siteName
                        a.title = news.text
                        a.link = f"{self.baseUri}{news.attrs['href']}"
                        a.tags = "Notices"
                        self.uri = a.link
                        details = self.getParser()
                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        rss.articles.append(a)
                except Exception as e:
                    logger.error(f"Failed to collect Notice from FFXIV. {e}")
                    pass

            if "Maintenance" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__maintenance--list"}
                    ):
                        a = RSSArticle()
                        a.siteName = self.siteName
                        a.title = news.text
                        a.link = f"{self.baseUri}{news.attrs['href']}"
                        a.tags = site["tag"]
                        self.uri = a.link
                        details = self.getParser()
                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        rss.articles.append(a)
                except Exception as e:
                    logger.error(
                        f"Failed to collect {site['tag']} records from FFXIV. {e}"
                    )
                    pass

            if "Updates" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__update--list"}
                    ):
                        a = RSSArticle()
                        a.siteName = self.siteName
                        a.title = news.text
                        a.link = f"{self.baseUri}{news.attrs['href']}"
                        a.tags = site["tag"]
                        self.uri = a.link
                        details = self.getParser()
                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        rss.articles.append(a)
                except Exception as e:
                    logger.error(
                        f"Failed to collect {site['tag']} records from FFXIV. {e}"
                    )
                    pass

            if "Status" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__obstacle--list"}
                    ):
                        a = RSSArticle()
                        a.siteName = self.siteName
                        a.title = news.text
                        a.link = f"{self.baseUri}{news.attrs['href']}"
                        a.tags = site["tag"]
                        self.uri = a.link
                        details = self.getParser()
                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        rss.articles.append(a)
                except Exception as e:
                    logger.error(
                        f"Failed to collect {site['tag']} records from FFXIV. {e}"
                    )
                    pass

        return rss

    def checkEnv(self):
        # Check what topics we will pull, if any.
        res = Sources(name="Final Fantasy XIV").findAllByName()
        # if we do not come back with a result, close down the thead
        if len(res) >= 1:
            for r in res:
                self.links.append(r)

            dwh = DiscordWebHooks(name="Final Fantasy XIV").findAllByName()
            for r in dwh:
                self.hooks.append(r)
