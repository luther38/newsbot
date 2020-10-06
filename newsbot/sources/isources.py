from typing import List
from requests import get, Response
from bs4 import BeautifulSoup
from newsbot import logger
from newsbot.tables import Articles


class UnableToFindContent(Exception):
    """
    Used when failure to return results from a scrape request.
    """

    pass


class UnableToParseContent(Exception):
    """
    This is used when a failure happens on parsing the content that came back from requests.
    Could be malformed site, or just not what was expected.
    """


class ISources:
    def __init__(self, rootUrl: str = "") -> None:
        # This defines the URI that will be requested by requests.
        # This can be static, or filled in by each loop of links.
        self.uri: str = ""

        # This contains all the links that will be looped though.
        self.links = list()

        # This contains all the DiscordWebHooks that relate to this Source.
        self.hooks = list()

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        pass

    def getContent(self) -> str:
        raise NotImplementedError

    def getDriverContent(self) -> str:
        raise NotImplementedError

    def getParser(self, souce: str) -> BeautifulSoup:
        raise NotImplementedError

    def getArticles(self) -> List[Articles]:
        """
        This is the primary loop that checks the source to extract all the articles.
        """
        raise NotImplementedError

    def checkEnv(self) -> None:
        """
        This runs at __init__ to check to see what is enabled.
        """
        raise NotImplementedError

    def isSourceEnabled(self) -> None:
        """
        Checks to see if the desired Source is enabled.
        This will write all the valid URL's to self.links to loop though.
        This also updates self.sourceEnabled
        Returns -> Bool
        """
        raise NotImplementedError

    def isDiscordOutputEnabled(self) -> None:
        """
        This checks to see if it was defined to add to the DiscordQueue.
        """
        raise NotImplementedError

    def getHeaders(self) -> dict:
        return {"User-Agent": "NewsBot - Automated News Delivery"}
