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

from typing import List
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.selectable import FromClause
from requests import Response
from bs4 import BeautifulSoup
from newsbot.sql.tables import Sources, DiscordWebHooks
from newsbot.logger import Logger

class BSources():
    """
    This class contains some common code found in the sources.  Do not use this on its own!
    """
    def __init__(self) -> None:
        self.uri:str = ""
        self.logger = Logger(__class__)
        
        self.outputDiscord: bool = False
        self.hooks = List[DiscordWebHooks] = list()
        
        self.sourceEnabled: bool = False
        self.links: List[Sources] = list()
        pass

    def checkEnv(self, siteName: str) -> None:
        # Check if site was requested.
        self.outputDiscord = self.isDiscordEnabled(siteName)
        if self.outputDiscord == True:
            self.hooks = self.getDiscordList(siteName)

        self.sourceEnabled = self.isSourceEnabled(siteName)
        if self.sourceEnabled == True:
            self.links = self.getSourceList(siteName)

    def getSourceList(self, siteName: str) -> List[Sources]:
        l = list()
        res = Sources(name=siteName).findAllByName()
        for i in res:
            l.append(i)
        return l

    def isSourceEnabled(self, siteName: str) -> bool:
        res = Sources(name=siteName).findAllByName()
        if len(res) >= 1:
            return True
        else:
            return False

    def getDiscordList(self, siteName: str) -> List[DiscordWebHooks]:
        h = list()
        dwh = DiscordWebHooks(name=siteName).findAllByName()
        if len(dwh) >= 1:
            for i in dwh:
                h.append(i)
        return h

    def isDiscordEnabled(self, siteName: str) -> bool:
        dwh = DiscordWebHooks(name=siteName).findAllByName()
        if len(dwh) >= 1:
            return True 
        else:
            return False

    def getContent(self) -> Response:
        try:
            headers = self.getHeaders()
            return get(self.uri, headers=headers)
        except Exception as e:
            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, requestsContent: Response = "", seleniumContent: str = "") -> BeautifulSoup:
        try:
            if seleniumContent != "":
                return BeautifulSoup(seleniumContent, features="html.parser")
            else:
                return BeautifulSoup(requestsContent.content, features="html.parser")
        except Exception as e:
            self.logger.critical(f"failed to parse data returned from requests. {e}")

    def getHeaders(self) -> dict:
        return {"User-Agent": "NewsBot - Automated News Delivery"}


from selenium.webdriver import Chrome, ChromeOptions

class BChrome():
    """
    This class helps to interact with Chrome/Selenium.
    It was made to be used as a Base class for the sources who need Chrome.
    """
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = ""
        self.driver = self.driverStart()
        pass

    def driverStart(self) -> Chrome:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            driver = Chrome(options=options)
            return driver
        except Exception as e:
            self.logger.critical(f"Chrome Driver failed to start! Error: {e}")

    def driverGetContent(self) -> str:
        try:
            return self.driver.page_source
        except Exception as e:
            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

    #def __driverGet__(self, uri: str ) -> None:
    #    self.driverGoTo(uri=uri)

    def driverGoTo(self, uri: str) -> None:
        try:
            self.driver.get(uri)
            self.driver.implicitly_wait(10)
        except Exception as e:
            self.logger.error(f"Driver failed to get {uri}. Error: {e}")

    def driverClose(self) -> None:
        try:
            self.driver.close()
        except Exception as e:
            self.logger.error(f"Driver failed to close. Error: {e}")


from typing import List
from requests import get, Response
from bs4 import BeautifulSoup
from newsbot.sql.tables import Articles

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

    def checkConfig(self) -> str:
        raise NotImplementedError

    def getDriverContent(self) -> str:
        raise NotImplementedError

    #def getParser(self, souce: str) -> BeautifulSoup:
    #    raise NotImplementedError

    def getArticles(self) -> List[Articles]:
        """
        This is the primary loop that checks the source to extract all the articles.
        """
        raise NotImplementedError

