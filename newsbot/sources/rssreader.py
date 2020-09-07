
from typing import List
from requests import get, Request
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

class RSSReader:
    def __init__(self, rootUrl: str = "") -> None:
        # 
        self.rootUrl = rootUrl
        self.uri: str = ""  

        self.headers = {"User-Agent": "NewsBot - Automated News Delivery"}

        self.links = list()
        self.hooks = list() 

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False     
        pass

    def getContent(self) -> Request:
        raise NotImplementedError

    def getParser(self) -> BeautifulSoup:
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

    def isSourceEnabled(self) -> bool:
        """
        Checks to see if the desired Source is enabled.
        This will write all the valid URL's to self.links to loop though.
        This also updates self.sourceEnabled
        Returns -> Bool
        """
        raise NotImplementedError

    def isDiscordOutput(self) -> None:
        """
        This checks to see if it was defined to add to the DiscordQueue.
        """
        raise NotImplementedError