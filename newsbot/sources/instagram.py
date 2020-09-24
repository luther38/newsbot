from typing import List
from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup
from re import findall
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
        self.currentLink: Sources = Sources()
        self.checkEnv()
        pass

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
        self.driver = self.getWebDriver()
        allArticles: List[Articles] = list()

        for site in self.links:
            self.currentLink = site

            nameSplit = site.name.split(" ")
            igType = nameSplit[1]
            self.siteName = f"Instagram {nameSplit[2]}"
            logger.debug(f"Instagram - {nameSplit[2]} - Checking for updates.")

            # Figure out if we are looking for a user or tag
            if igType == "user":
                self.uri = f"{self.baseUri}{nameSplit[2]}"
                self.__driverGet__(self.uri)
                links = self.getUserArticleLinks()
            elif igType == "tag":
                self.uri = f"{self.baseUri}explore/tags/{nameSplit[2]}/"
                self.__driverGet__(self.uri)
                links = self.getTagArticleLinks()

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

        self.driver.quit()
        self.siteName = "Instagram"

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

    def getUserArticleLinks(self) -> List[str]:
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

    def getTagArticleLinks(self) -> List[str]:
        """
        This checks the tag for the newst posts.
        """
        links = list()

        try:
            source: str = self.getContent()
            soup: BeautifulSoup = self.getParser(source)
            res = soup.find_all(name="article")

            # Top Posts
            links = self.getArticleLinks(
                res[0].contents[0].contents[1].contents[0].contents, links
            )

            # Recent
            # TODO Need a way to define options on Instagram Tags.  One might not want EVERYTHING.
            # links = self.getArticleLinks(res[0].contents[2].contents[0].contents, links)

        except Exception as e:
            logger.error("Driver ran into a problem pulling links from a tag.")

        return links

    def getArticleLinks(self, soupList: List, linkList: List) -> List[str]:

        for i in soupList:
            try:
                for l in i.contents:
                    linkList.append(
                        f"https://www.instagram.com{l.contents[0].attrs['href']}"
                    )
            except Exception as e:
                logger.error(f"Failed to extract post link. {e}")
        return linkList

    def getPostInfo(self, link: str) -> Articles:
        a = Articles(url=link, siteName=self.currentLink.name, tags="instagram, posts")
        nameSplit = self.currentLink.name.split(" ")
        if "tag" in self.currentLink.name:
            a.tags += f", tag, {nameSplit[2]}"
        elif "user" in self.currentLink.name:
            a.tags += f", user, {nameSplit[2]}"

        self.__driverGet__(link)
        source = self.getContent()
        soup = self.getParser(source)

        # Get the title from the post
        title = soup.find_all(name="span", attrs={"class", ""})

        # Check the title to make sure it was not just all tags... someone did that! - Done
        # TODO Need a better placeholder value
        cleanTitle = self.cleanTitle(title[1].text)
        if cleanTitle == "":
            a.title = "Instagram Post"
        else:
            a.title = cleanTitle

        # improve the regex to collect tags.  It nuked out a title... oops - Made an adjustment
        tags = self.getTags(title[1].text)
        if tags != "":
            a.tags = tags

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
            elif "photo shared by" in i.attrs["alt"].lower():
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

    def getTags(self, text: str) -> str:
        t = ""
        # res = findall('#[a-zA-Z0-9].*', text)
        res = findall("[#](.*?)[ ]", text)
        if len(res) >= 1:
            # tags = res[0].split('#')
            for i in res:
                try:
                    i: str = i.replace(" ", "")
                    if i != "":
                        t += f"{i}, "
                except:
                    pass
        return t

    def cleanTitle(self, text: str) -> str:
        """
        This will check the text given for Instagram tags. If they are found, remove them.
        If no tags are found from regex, it will return the given text.
        """
        t = ""
        res = findall("#[a-zA-Z0-9].*", text)
        if len(res) >= 1:
            t = text.replace(res[0], "")
            return t
        else:
            return text
