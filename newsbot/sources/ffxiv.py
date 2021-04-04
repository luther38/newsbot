from typing import List
from newsbot.logger import Logger
from newsbot.sql import Articles
from newsbot.sources.common import ISources, BSources, UnableToParseContent, UnableToFindContent

class FFXIVReader(ISources, BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = "https://na.finalfantasyxiv.com/lodestone/news/"
        self.baseUri: str = "https://na.finalfantasyxiv.com"
        self.siteName: str = "Final Fantasy XIV"
        self.authorName: str = "Final Fantasy XIV Offical Site"
        self.links = list()
        self.hooks = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        pass

    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for site in self.links:
            self.logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url

            #siteContent: Response = self.getContent()
            page = self.getParser(requestsContent=self.getContent())

            if "Topics" in site.name:
                try:
                    for news in page.find_all(
                        "li", {"class", "news__list--topics ic__topics--list"}
                    ):
                        a = Articles(
                            siteName=self.siteName,
                            tags="ffxiv, topics, news",
                            authorName=self.authorName,
                        )
                        # a.siteName = self.siteName
                        header = news.contents[0].contents
                        body = news.contents[1].contents
                        a.title = header[0].text
                        a.url = f"{self.baseUri}{header[0].contents[0].attrs['href']}"
                        a.thumbnail = body[0].contents[0].attrs["src"]
                        a.description = body[0].contents[0].next_element.text
                        # a.tags = "Topics"
                        allArticles.append(a)
                except Exception as e:
                    self.logger.error(f"Failed to collect Topics from FFXIV. {e}")

            if "Notices" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__info--list"}
                    ):
                        a = Articles(
                            siteName=self.siteName,
                            tags="ffxiv, notices, news",
                            authorName=self.authorName,
                        )
                        # a.siteName = self.siteName
                        a.title = news.text
                        a.url = f"{self.baseUri}{news.attrs['href']}"
                        # a.tags = "Notices"
                        self.uri = a.link
                        #subPage = self.getContent()
                        details = self.getParser(requestsContent=self.getContent())
                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        allArticles.append(a)
                except Exception as e:
                    self.logger.error(f"Failed to collect Notice from FFXIV. {e}")
                    pass

            if "Maintenance" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__maintenance--list"}
                    ):
                        a = Articles(
                            siteName=self.siteName,
                            tags="ffxiv, maintenance, news",
                            authorName=self.authorName,
                        )
                        # a.siteName = self.siteName
                        a.title = news.text
                        a.url = f"{self.baseUri}{news.attrs['href']}"
                        # a.tags = site["tag"]
                        self.uri = a.link
                        #subPage = self.getContent()
                        details = self.getParser(requestsContent=self.getContent())
                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text

                        allArticles.append(a)
                except Exception as e:
                    self.logger.error(
                        f"Failed to collect {site['tag']} records from FFXIV. {e}"
                    )
                    pass

            if "Updates" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__update--list"}
                    ):
                        a = Articles(
                            siteName=self.siteName,
                            tags="ffxiv, updates, news",
                            authorName=self.authorName,
                        )
                        a.title = news.text
                        a.url = f"{self.baseUri}{news.attrs['href']}"
                        self.uri = a.link

                        #subPage = self.getContent()
                        details = self.getParser(requestsContent=self.getContent())

                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        allArticles.append(a)
                except Exception as e:
                    self.logger.error(
                        f"Failed to collect {site['tag']} records from FFXIV. {e}"
                    )
                    pass

            if "Status" in site.name:
                try:
                    for news in page.find_all(
                        "a", {"class", "news__list--link ic__obstacle--list"}
                    ):
                        a = Articles(
                            siteName=self.siteName,
                            tags="ffxiv, news, status",
                            authorName=self.authorName,
                        )
                        a.siteName = self.siteName
                        a.title = news.text
                        a.link = f"{self.baseUri}{news.attrs['href']}"
                        a.tags = site["tag"]
                        self.uri = a.link

                        #subPage = self.getContent()
                        details = self.getParser(requestsContent=self.getContent())

                        for d in details.find_all(
                            "div", {"class", "news__detail__wrapper"}
                        ):
                            a.description = d.text
                        allArticles.append(a)
                except Exception as e:
                    self.logger.error(
                        f"Failed to collect {site['tag']} records from FFXIV. {e}"
                    )
                    pass

        return allArticles

#    def checkEnv(self) -> None:
#        # Check if site was requested.
#        self.outputDiscord = self.isDiscordEnabled(self.siteName)
#        if self.outputDiscord == True:
#            self.hooks = self.getDiscordList(self.siteName)
#
#        self.sourceEnabled = self.isSourceEnabled(self.siteName)
#        if self.sourceEnabled == True:
#            self.links = self.getSourceList(self.siteName)

#    def getContent(self) -> Response:
#        try:
#            headers = self.getHeaders()
#            return get(self.uri, headers=headers)
#        except Exception as e:
#            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")
#
#    def getParser(self, siteContent: Response) -> BeautifulSoup:
#        try:
#            return BeautifulSoup(siteContent.content, features="html.parser")
#        except Exception as e:
#            self.logger.critical(f"failed to parse data returned from requests. {e}")
