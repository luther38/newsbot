from typing import List
from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup

class YoutubeReader(ISources):
    def __init__(self):
        self.uri: str = "https://youtube.com"
        self.siteName: str = "Youtube"
        self.feedBase: str = "https://www.youtube.com/feeds/videos.xml?channel_id="

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
            for i in res:
                self.links.append(i)
                self.sourceEnabled = True

    def isDiscordOutputEnabled(self) -> None:
        dwh = DiscordWebHooks(name=self.siteName).findAllByName()
        if len(dwh) >= 1:
            self.outputDiscord = True
            for i in dwh:
                self.hooks.append(i)

    def getArticles(self) -> List[Articles]:
        logger.debug(f"Checking YouTube for new content")

        allArticles: List[Articles] = list()

        for site in self.links:
            logger.debug(f"{site.name} - Checking for updates")
            self.uri = f"{site.url}"
            channelID: str = self.getChannelId()

            self.uri = f"{self.feedBase}{channelID}"
            siteContent = self.getContent()
            page = self.getParser(siteContent)

            root = page.contents[2].contents
            for item in root:
                if item.name == "entry":
                    a = Articles()
                    a.url = item.contents[9].attrs['href']
                    a.video = a.url
                    a.title = item.contents[7].text
                    a.pubDate = item.contents[13].text
                    a.siteName = site.name
                    a.thumbnail = item.contents[17].contents[5].attrs['url']

                    allArticles.append(a)
                    
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

    def getChannelId(self) -> str:
        siteContent: Response = self.getContent()
        page: BeautifulSoup = self.getParser(siteContent)
        
        meta = page.find_all("meta")
        for i in meta:
            try:
                if i.attrs['itemprop'] == "channelId":
                    channelId = i.attrs['content']
                    return channelId
            except:
                pass
        
        return ''