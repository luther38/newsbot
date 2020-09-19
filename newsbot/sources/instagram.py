from typing import List
from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions


class InstagramReader(ISources):
    def __init__(self) -> None:
        self.uri = "https://www.instagram.com/"
        self.baseUri = self.uri
        self.siteName: str = "Instagram"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.driver = self.getWebDriver()
        self.checkEnv()
        pass

    def getWebDriver(self) -> Chrome:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            return Chrome(chrome_options=options)
        except Exception as e:
            logger.critical(f"Chrome Driver failed to start! Error: {e}")

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
        allArticles: List[Articles] = list()
        
        for site in self.links:
            nameSplit = site.name.split(" ")
            self.uri = f"{self.baseUri}{nameSplit[1]}"
            self.siteName = f"Instagram {nameSplit[1]}"
            logger.debug(f"Instagram - {nameSplit[1]} - Checking for updates.")
            self.__driverGet__(self.uri)

            links = self.getArticleLinks()
            for l in links:
                # check if we have already seen the url
                a = Articles(url=l)
                if a.exists() == False:
                    # Get the content
                    allArticles.append(self.getPostInfo(l))

            logger.debug(f"{self.siteName} - Finished checking.")
            try:
                pass
            except Exception as e:
                logger.error(
                    f"Failed to parse articles from {self.siteName}.  Chances are we have a malformed responce. {e}"
                )

        return allArticles

    def getContent(self) -> str:
        try:
            # headers = self.getHeaders()
            # res: Response = get(self.uri, headers=headers)
            # return res.content
            return self.driver.page_source
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, source: str) -> BeautifulSoup:
        try:
            return BeautifulSoup(source, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")

    def getArticleLinks(self) -> List[str]:
        """
        This reviews a users page to find all the links that relate to each post they have made.
        """
        links = list()
        try:
            source = self.getContent()
            soup: BeautifulSoup = self.getParser(source)
            res = soup.find_all(name="article")
            for i in res[0].contents[0].contents[0].contents:
                for l in i.contents:
                    links.append(
                        f"https://www.instagram.com{l.contents[0].attrs['href']}"
                    )

        except Exception as e:
            logger.error(e)
            self.__close__()

        return links

    def getPostInfo(self, link: str) -> Articles:
        a = Articles(url=link, siteName=self.siteName, tags="instagram, posts")
        self.__driverGet__(link)
        source = self.getContent()
        soup = self.getParser(source)

        # Get the title from the post
        title = soup.find_all(name="span", attrs={"class", ""})
        a.title = title[1].text

        # Get when the post went up
        dt = soup.find_all(name="time", attrs={"class": "FH9sR Nzb55"})
        a.pubDate = dt[0].attrs["datetime"]

        # Video link
        hasVideo = soup.find_all(
            name="span", attrs={"class": "qBUYS _7CSz9 FGFB7 videoSpritePlayButton"}
        )
        hasCollection = soup.find_all(name="button", attrs={"class": "_6CZji"})
        if len(hasVideo) >= 1:
            video = soup.find(name="video", attrs={"class": "tWeCl"})
            a.description = "This post contains a video, view it online!"
            a.video = video.attrs["src"]

        # check if it contains multiple pictures
        elif len(hasCollection) >= 1:
            a.description = "This post contains multiple pictures, view them online!"
            a.thumbnail = self.getPicture(soup)
            # TODO Figure out if the collection can be stored.
            # Its not like Discord can present them all with a single post.
            # self.getCollection(soup)

        # Get a single picture
        else:
            a.thumbnail = self.getPicture(soup)
        return a

    def getPicture(self, soup: BeautifulSoup) -> str:
        images = soup.find_all(name="img")
        for i in images:
            if "photo by " in i.attrs["alt"].lower():
                return i.attrs["src"]

    def __driverGet__(self, uri: str) -> None:
        try:
            self.driver.get(uri)
            self.driver.implicitly_wait(5)
        except Exception as e:
            logger.error(f"Driver failed to get {uri}. Error: {e}")

    def __close__(self) -> None:
        try:
            self.driver.close()
        except Exception as e:
            logger.error(f"Driver failed to close. Error: {e}")
