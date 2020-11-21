from typing import List
from newsbot import env
from newsbot.logger import logger
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from newsbot.cache import Cache
from requests import get, Response
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep

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
            self.sourceEnabled = True
            for i in res:
                self.links.append(i)

    def isDiscordOutputEnabled(self) -> None:
        dwh = DiscordWebHooks(name=self.siteName).findAllByName()
        if len(dwh) >= 1:
            self.outputDiscord = True
            for i in dwh:
                self.hooks.append(i)

    def getArticles(self) -> List[Articles]:
        logger.debug(f"Checking YouTube for new content")
        self.driver = self.getWebDriver()

        allArticles: List[Articles] = list()

        for site in self.links:
            s = site.name.split(' ')
            self.authorName = ''
            self.authorImage = ''
            logger.debug(f"{site.name} - Checking for updates")

            # pull the source code from the main youtube page
            channelID = Cache(key=f'youtube {s[1]} channelID').find()
            if channelID == "":
                self.uri = f"{site.url}"
                self.__driverGet__(self.uri)
                siteContent: str = self.getDriverContent()
                page: BeautifulSoup = self.getParser(siteContent)
                channelID: str = self.getChannelId(page)
                Cache(key=f'youtube {s[1]} channelID', value=channelID).add()

                # Not finding the values I want with just request.  Time for Chrome.
                # We are collecting info that is not present in the RSS feed.  
                # We are going to store them in the class.
                try:
                    authorImage = page.find_all(name='img', attrs={"id":"img"})
                    self.authorImage = authorImage[0].attrs['src']
                    Cache(key=f"youtube {s[1]} authorImage", value=self.authorImage).add()
                except Exception as e:
                    logger.error(f"Failed to find the authorImage for {s[1]}.  CSS might have changed. {e}")
                authorImage.clear()

                try:
                    authorName = page.find_all(name='yt-formatted-string', attrs={"class": "style-scope ytd-channel-name", "id":"text"})
                    self.authorName = authorName[0].text
                    Cache(key=f"youtube {s[1]} authorName", value=self.authorName).add()
                except Exception as e:
                    logger.error(f"Failed to find the authorName for {s[1]}.  CSS might have changed. {e}")
                authorName.clear()
            else:
                self.authorName = Cache(key=f"youtube {s[1]} authorName").find()
                self.authorImage = Cache(key=f"youtube {s[1]} authorImage").find()

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

                    allArticles.append(a)

        self.driver.quit()
        return allArticles

    def getContent(self) -> str:
        try:
            headers = self.getHeaders()
            res = get(self.uri, headers=headers)
            return res.text 
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getDriverContent(self) -> str:
        try:
            return self.driver.page_source
        except Exception as e:
            logger.critical(f"Filed to collect source code from driver at {self.uri}. {e}")


    def getParser(self, siteContent: str) -> BeautifulSoup:
        try:
            return BeautifulSoup(siteContent, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")

    def getChannelId(self, page: BeautifulSoup) -> str:
        #siteContent: Response = self.getContent()
        #page: BeautifulSoup = self.getParser(siteContent)

        meta = page.find_all("meta")
        for i in meta:
            try:
                if i.attrs["itemprop"] == "channelId":
                    channelId = i.attrs["content"]
                    return channelId
            except:
                pass

        return ""

    # Selenium Code
    def getWebDriver(self) -> Chrome:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            driver = Chrome(options=options)
            return driver
        except Exception as e:
            logger.critical(f"Chrome Driver failed to start! Error: {e}")

    def __driverGet__(self, uri: str) -> None:
        try:
            self.driver.get(uri)
            #self.driver.implicitly_wait(30)
            sleep(5)
        except Exception as e:
            logger.error(f"Driver failed to get {uri}. Error: {e}")

