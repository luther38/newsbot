from typing import List
from newsbot import env
from newsbot.logger import Logger
from newsbot.sources.common import (
    BChrome,
    ISources,
    BSources,
    UnableToFindContent,
    UnableToParseContent,
)
from newsbot.sql.tables import Articles, Sources, DiscordWebHooks
from newsbot.cache import Cache
from bs4 import BeautifulSoup
from time import sleep


class YoutubeReader(ISources, BSources, BChrome):
    def __init__(self):
        self.logger = Logger(__class__)
        self.uri: str = "https://youtube.com"
        self.siteName: str = "Youtube"
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
                # self.driver.save_screenshot("youtube_step1.png")
                siteContent: str = self.driverGetContent()
                page: BeautifulSoup = self.getParser(seleniumContent=siteContent)
                channelID: str = self.getChannelId(page)
                Cache(key=f"youtube {site.name} channelID", value=channelID).add()

                # Not finding the values I want with just request.  Time for Chrome.
                # We are collecting info that is not present in the RSS feed.
                # We are going to store them in the class.
                try:
                    authorImage = page.find_all(name="img", attrs={"id": "img"})
                    self.authorImage = authorImage[0].attrs["src"]
                    Cache(
                        key=f"{site.source} {site.name} authorImage",
                        value=self.authorImage,
                    ).add()
                except Exception as e:
                    self.logger.error(
                        f"Failed to find the authorImage for {site.name}.  CSS might have changed. {e}"
                    )
                authorImage.clear()

                try:
                    authorName = page.find_all(
                        name="yt-formatted-string",
                        attrs={"class": "style-scope ytd-channel-name", "id": "text"},
                    )
                    self.authorName = authorName[0].text
                    Cache(
                        key=f"youtube {site.name} authorName", value=self.authorName
                    ).add()
                except Exception as e:
                    self.logger.error(
                        f"Failed to find the authorName for {site.name}.  CSS might have changed. {e}"
                    )
                authorName.clear()
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
