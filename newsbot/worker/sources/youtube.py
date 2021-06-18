from newsbot.core.sql.tables.schema import SourceLinks
from newsbot.worker.sources.driver import BFirefox
from typing import List
from newsbot.core.logger import Logger
from newsbot.core.constant import SourceName
from newsbot.worker.sources.common import BSources
from newsbot.core.sql.tables import Articles, Sources, DiscordWebHooks
from newsbot.worker.sources.driver import BFirefox
from newsbot.core.cache import Cache
from bs4 import BeautifulSoup
from time import sleep

class YoutubeReader(BSources, BFirefox):
    def __init__(self):
        self.logger = Logger(__class__)
        self.uri: str = "https://youtube.com"
        self.siteName: str = SourceName.YOUTUBE.value
        self.feedBase: str = "https://www.youtube.com/feeds/videos.xml?channel_id="

        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False

        self.checkEnv(self.siteName)
        pass

    def getArticles(self) -> List[Articles]:
        self.logger.debug(f"Checking YouTube for new content")
        self.driver = self.driverStart()

        allArticles: List[Articles] = list()

        for site in self.links:

            self.authorName = ""
            self.authorImage = ""
            self.logger.debug(f"{site.source} - {site.name} - Checking for updates")

            # pull the source code from the main youtube page
            channelID = Cache(key=f"{site.source} {site.name} channelID").find()
            if channelID == "":
                self.uri = f"{site.url}"
                self.driverGoTo(self.uri)
                self.driverSaveScreenshot("youtube_step1.png")
                siteContent: str = self.driverGetContent()
                page: BeautifulSoup = self.getParser(seleniumContent=siteContent)
                channelID: str = self.getChannelId(page)
                Cache(key=f"youtube {site.name} channelID", value=channelID).add()

                # Not finding the values I want with just request.  Time for Chrome.
                # We are collecting info that is not present in the RSS feed.
                # We are going to store them in the class.
                self.setAuthorImage(page, site)
                self.setAuthorName(page, site)
            else:
                self.authorName = Cache(key=f"youtube {site.name} authorName").find()
                self.authorImage = Cache(key=f"youtube {site.name} authorImage").find()

            # Generatet he hidden RSS feed uri
            self.uri = f"{self.feedBase}{channelID}"
            siteContent = self.getContent()
            page = self.getParser(siteContent)

            root = page.contents[2].contents
            for item in root:
                if item.name == "entry":
                    a = Articles()
                    a.url = item.contents[9].attrs["href"]
                    a.video = a.url
                    a.title = item.contents[7].text
                    a.pubDate = item.contents[13].text
                    #TODO to be phased out
                    a.siteName = site.name
                    a.thumbnail = item.contents[17].contents[5].attrs["url"]
                    a.authorImage = self.authorImage
                    a.authorName = self.authorName
                    a.sourceType = site.source
                    a.sourceName = site.name

                    allArticles.append(a)

        self.driverClose()
        return allArticles

    def getChannelId(self, page: BeautifulSoup) -> str:
        # siteContent: Response = self.getContent()
        # page: BeautifulSoup = self.getParser(siteContent)

        meta = page.find_all("meta")
        for i in meta:
            try:
                if i.attrs["itemprop"] == "channelId":
                    channelId = i.attrs["content"]
                    return channelId
            except:
                pass

        return ""

    def setAuthorName(self, page: BeautifulSoup, site: Sources):
        try:
            authorName = page.find_all(
                name="yt-formatted-string",
                attrs={"class": "style-scope ytd-channel-name", "id": "text"},
            )
            self.authorName = authorName[0].text
            if self.authorName == None or self.authorName == '':
                self.logger.error(f"Failed to find the authorName for {site.name}.  CSS might have changed.")    
            Cache(
                key=f"youtube {site.name} authorName", value=self.authorName
            ).add()
        except Exception as e:
            self.logger.error(
                f"Failed to find the authorName for {site.name}.  CSS might have changed. {e}"
            )

    def setAuthorImage(self, page: BeautifulSoup, site: Sources) -> str:
        try:
            authorImage = page.find_all(name="yt-img-shadow", attrs={"id": "avatar"})
            img = authorImage[0].contents[1].attrs["src"]
            if img != '':
                Cache(
                    key=f"{site.source} {site.name} authorImage",
                    value=img,
                ).add()
                self.authorImage = img
            else:
                self.logger.error(f"Failed to find the AuthorImage on the youtube page.")
        except Exception as e:
            self.logger.error(
                f"Failed to find the authorImage for {site.name}.  CSS might have changed. {e}"
            )