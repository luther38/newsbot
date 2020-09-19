from typing import List
from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup


class TemplateReader(ISources):
    def __init__(self) -> None:
        self.uri = "https://example.net/"
        self.siteName: str = "Example"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv()
        pass

    def checkEnv(self) -> None:
        # Check if Pokemon Go was requested
        self.isSourceEnabled()
        self.isDiscordOutputEnabled()

    def isSourceEnabled(self) -> None:
        res = Sources(name=self.siteName).findAllByName()
        if len(res) >= 1:
            self.links.append(res[0])
            self.sourceEnabled = True

    def isDiscordOutputEnabled(self) -> None:
        dwh = DiscordWebHooks(name=self.siteName).findAllByName()
        if len(dwh) >= 1:
            self.outputDiscord = True
            for i in dwh:
                self.hooks.append(i)

    def getArticles(self) -> List[Articles]:
        for site in self.links:
            logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url

            siteContent: Response = self.getContent()
            if siteContent.status_code != 200:
                raise UnableToFindContent(
                    f"Did not get status code 200.  Got status code {siteContent.status_code}"
                )

            bs: BeautifulSoup = self.getParser(siteContent)

            allArticles: List[Articles] = list()
            try:
                logger.debug(f"{self.siteName} - Finished checking.")
            except Exception as e:
                logger.error(
                    f"Failed to parse articles from {self.siteName}.  Chances are we have a malformed responce. {e}"
                )

        return allArticles

    def getContent(self) -> Response:
        try:
            headers = self.getHeaders()
            return get(self.uri, headers=headers)
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, siteContent: Response) -> BeautifulSoup:
        try:
            return BeautifulSoup(siteContent.content, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")
