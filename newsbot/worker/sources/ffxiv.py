from typing import List
from bs4 import BeautifulSoup
from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Articles
from newsbot.worker.sources.common import (
    ISources,
    BSources,
)
from json import loads


class FFXIVReader(ISources, BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = "https://na.finalfantasyxiv.com/lodestone/news/"
        self.baseUri: str = "https://na.finalfantasyxiv.com"
        self.siteName: str = "finalfantasyxiv"
        self.authorName: str = "Final Fantasy XIV Offical Site"
        self.links = list()
        self.hooks = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        pass

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        self.logger.debug(f"{self.siteName} - Checking for updates.")
        rootPage = self.getParser(requestsContent=self.getContent())

        for site in self.links:
            if site.enabled == True:
                if site.name == "topics":
                    for i in self.getTopics(page=rootPage):
                        allArticles.append(i)

                elif site.name == "notices":
                    for i in self.getNotices(page=rootPage):
                        allArticles.append(i)

                elif site.name == "maintenance":
                    for i in self.getMaintenances(page=rootPage):
                        allArticles.append(i)
                                
                elif site.name == "updates":
                    for i in self.getUpdates(page=rootPage):
                        allArticles.append(i)

                elif site.name == "status":
                    for i in self.getStatus(page=rootPage):
                        allArticles.append(i)

        return allArticles
        
    def getTopics(self, page: BeautifulSoup) -> List[Articles]:
        #if "Topics" in site.name:
        l = list()
        try:
            for news in page.find_all(
                "li", {"class", "news__list--topics ic__topics--list"}
            ):
                a = Articles(
                    siteName=self.siteName,
                    tags="ffxiv, topics, news",
                    authorName=self.authorName,
                    sourceName="topics",
                    sourceType="finalfantasyxiv"
                )
                header = news.contents[0].contents
                body = news.contents[1].contents
                a.title = header[0].text
                a.url = f"{self.baseUri}{header[0].contents[0].attrs['href']}"
                a.thumbnail = body[0].contents[0].attrs["src"]
                a.description = body[0].contents[0].next_element.text
                l.append(a)
            return l
        except Exception as e:
            self.logger.error(f"Failed to collect 'Topics' from FFXIV. {e}")

    def getNotices(self, page: BeautifulSoup) -> List[Articles]:
        l = list()
            #if "Notices" in site.name:
        try:
            for news in page.find_all(
                "a", {"class", "news__list--link ic__info--list"}
            ):
                a = Articles(
                    siteName=self.siteName,
                    tags="ffxiv, notices, news",
                    authorName=self.authorName,
                    sourceName="notices",
                    sourceType="finalfantasyxiv"
                )
                a.title = news.text
                a.url = f"{self.baseUri}{news.attrs['href']}"
                self.uri = a.link
                details = self.getParser(requestsContent=self.getContent())
                for d in details.find_all(
                    "div", {"class", "news__detail__wrapper"}
                ):
                    a.description = d.text
                l.append(a)
            return l
        except Exception as e:
            self.logger.error(f"Failed to collect 'Notice' from FFXIV. {e}")
            pass

    def getMaintenances(self, page: BeautifulSoup) -> List[Articles]:
        l = list()
        try:
            for news in page.find_all(
                "a", {"class", "news__list--link ic__maintenance--list"}
            ):
                a = Articles(
                    siteName=self.siteName,
                    tags="ffxiv, maintenance, news",
                    authorName=self.authorName,
                    sourceName="maintenance",
                    sourceType="finalfantasyxiv"
                )
                a.title = news.text
                a.url = f"{self.baseUri}{news.attrs['href']}"
                self.uri = a.link
                details = self.getParser(requestsContent=self.getContent())
                for d in details.find_all(
                    "div", {"class", "news__detail__wrapper"}
                ):
                    a.description = d.text

                l.append(a)
            return l
        except Exception as e:
            self.logger.error(
                f"Failed to collect 'Maintenance' records from FFXIV. {e}"
            )
            pass

    def getUpdates(self, page: BeautifulSoup) -> List[Articles]:
        #if "Updates" in site.name:
        l = list()
        try:
            for news in page.find_all(
                "a", {"class", "news__list--link ic__update--list"}
            ):
                a = Articles(
                    siteName=self.siteName,
                    tags="ffxiv, updates, news",
                    authorName=self.authorName,
                    sourceName="updates",
                    sourceType="finalfantasyxiv"
                )
                a.title = news.text
                a.url = f"{self.baseUri}{news.attrs['href']}"
                self.uri = a.link
                details = self.getParser(requestsContent=self.getContent())

                for d in details.find_all(
                    "div", {"class", "news__detail__wrapper"}
                ):
                    a.description = d.text
                l.append(a)
            return l
        except Exception as e:
            self.logger.error(
                f"Failed to collect 'Updates' records from FFXIV. {e}"
            )
            pass

    def getStatus(self, page: BeautifulSoup) -> List[Articles]:
            #if "Status" in site.name:
        l = list()
        try:
            for news in page.find_all(
                "a", {"class", "news__list--link ic__obstacle--list"}
            ):
                a = Articles(
                    siteName=self.siteName,
                    tags="ffxiv, news, status",
                    authorName=self.authorName,
                    sourceName="status",
                    sourceType="finalfantasyxiv"
                )
                a.siteName = self.siteName
                a.title = news.text
                a.link = f"{self.baseUri}{news.attrs['href']}"
                self.uri = a.link

                # subPage = self.getContent()
                details = self.getParser(requestsContent=self.getContent())

                for d in details.find_all(
                    "div", {"class", "news__detail__wrapper"}
                ):
                    a.description = d.text
                l.append(a)
            return l
        except Exception as e:
            self.logger.error(
                f"Failed to collect 'Status' records from FFXIV. {e}"
            )
            pass