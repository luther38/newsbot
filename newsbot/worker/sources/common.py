from newsbot.core.sql.tables.sources import SourcesTable
from typing import List
from requests import get, Response
from bs4 import BeautifulSoup
from newsbot.core.sql.tables import Articles, Sources, DiscordWebHooks, SourceLinks
from abc import ABC, abstractclassmethod
from newsbot.core.logger import Logger

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
    pass

class ISources(ABC):
    def __init__(self, rootUrl: str = "") -> None:
        # This defines the URI that will be requested by requests.
        # This can be static, or filled in by each loop of links.
        #self.uri: str = ""

        # This contains all the links that will be looped though.
        #self.links = list()

        # This contains all the DiscordWebHooks that relate to this Source.
        #self.hooks = list()

        #self.sourceEnabled: bool = False
        #self.outputDiscord: bool = False
        pass

    #@abstractclassmethod
    #def checkConfig(self) -> str:
    #    raise NotImplementedError

    @abstractclassmethod
    def getArticles(self) -> List[Articles]:
        """
        This is the primary loop that checks the source to extract all the articles.
        """
        raise NotImplementedError

class BSources(ISources):
    """
    This class contains some common code found in the sources.  Do not use this on its own!
    """

    def __init__(self) -> None:
        self.uri: str = ""
        self.logger = Logger(__class__)

        self.outputDiscord: bool = False
        self.hooks: List[DiscordWebHooks] = list()

        self.sourceEnabled: bool = False
        self.links: List[Sources] = list()
        pass

    def checkEnv(self, siteName: str) -> None:
        # Check if site was requested.
        outputDiscord = self.isDiscordEnabled(siteName)
        if len(outputDiscord) >= 1:
            self.outputDiscord = True
            self.hooks = outputDiscord

        sources = self.getSourceList(siteName)
        if len(sources) >= 1:
            self.sourceEnabled = True
            self.links = sources

    def getSourceList(self, siteName: str) -> List[Sources]:
        l = list()
        res = Sources(source=siteName).findAllBySource()
        for i in res:
            l.append(i)
        return l

    def isDiscordEnabled(self, siteName: str) -> List[DiscordWebHooks]:
        h: List[DiscordWebHooks] = list()
        tSources = SourcesTable()
        s = tSources.findAllBySource(source=siteName)
        for i in s:
            sl: SourceLinks = SourceLinks(sourceID=i.id).findBySourceID()
            if sl == None:
                continue
            elif sl.discordID != "" or sl.discordID != None:
                d = DiscordWebHooks()
                d.id = sl.discordID
                discordRef: DiscordWebHooks = d.findById()
                if discordRef.enabled == True:
                    h.append(discordRef)
            else:
                continue
        return h

    def getContent(self) -> Response:
        try:
            headers = self.getHeaders()
            return get(self.uri, headers=headers)
        except Exception as e:
            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(
        self, requestsContent: Response = "", seleniumContent: str = ""
    ) -> BeautifulSoup:
        try:
            if seleniumContent != "":
                return BeautifulSoup(seleniumContent, features="html.parser")
            else:
                return BeautifulSoup(requestsContent.content, features="html.parser")
        except Exception as e:
            self.logger.critical(f"failed to parse data returned from requests. {e}")

    def getHeaders(self) -> dict:
        return {"User-Agent": "NewsBot - Automated News Delivery"}



