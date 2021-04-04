from typing import List
from newsbot import env
from newsbot.logger import Logger
from newsbot.sources.common import BChrome, BSources, ISources, UnableToFindContent, UnableToParseContent
from newsbot.sql import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup
from re import findall
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait


class InstagramReader(ISources, BSources, BChrome):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://www.instagram.com/"
        self.baseUri = self.uri
        self.siteName: str = "Instagram"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.currentLink: Sources = Sources()
        self.checkEnv(self.siteName)
        pass

    def getArticles(self) -> List[Articles]:
        self.driver = self.driverStart()
        allArticles: List[Articles] = list()

        for site in self.links:
            self.currentLink = site

            nameSplit = site.name.split(" ")
            igType = nameSplit[1]
            self.siteName = f"Instagram {nameSplit[2]}"
            self.logger.debug(f"Instagram - {nameSplit[2]} - Checking for updates.")
            
            #self.uri = f"{self.baseUri}directory/hashtags/"
            self.uri = f"https://www.instagram.com/directory/profiles/0-0/"
            self.driverGoTo(self.uri)

            # Figure out if we are looking for a user or tag
            if igType == "user":
                #self.uri = f"{self.baseUri}{nameSplit[2]}"
                WebDriverWait(driver=self.driver, timeout=5)
                self.driver.save_screenshot('ig_hashtag.png')
                res = self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div/div/span[2]')
                links = self.getUserArticleLinks()
            elif igType == "tag":
                self.uri = f"{self.baseUri}explore/tags/{nameSplit[2]}/"
                self.driverGoTo(self.uri)
                links = self.getTagArticleLinks()

            for l in links:
                # check if we have already seen the url
                a = Articles(url=l)
                if a.exists() == False:
                    # Get the content
                    allArticles.append(self.getPostInfo(l))

            self.logger.debug(f"{self.siteName} - Finished checking.")
            try:
                pass
            except Exception as e:
                self.logger.error(
                    f"Failed to parse articles from {self.siteName}.  Chances are we have a malformed responce. {e}"
                )

        self.driverClose()
        self.siteName = "Instagram"

        return allArticles

    def getUserArticleLinks(self) -> List[str]:
        """
        This reviews a users page to find all the links that relate to each post they have made.
        """
        links = list()
        try:
            #source = self.getContent()
            soup: BeautifulSoup = self.getParser(requestsContent=self.getContent())
            res = soup.find_all(name="article")
            for i in res[0].contents[0].contents[0].contents:
                for l in i.contents:
                    links.append(
                        f"https://www.instagram.com{l.contents[0].attrs['href']}"
                    )

        except Exception as e:
            self.logger.error(e)
            self.driverClose()

        return links

    def getTagArticleLinks(self) -> List[str]:
        """
        This checks the tag for the newst posts.
        """
        links = list()

        try:
            #source: str = self.getContent()
            soup: BeautifulSoup = self.getParser(requestsContent=self.getContent())
            res = soup.find_all(name="article")

            # Top Posts
            links = self.getArticleLinks(
                res[0].contents[0].contents[1].contents[0].contents, links
            )

            # Recent
            # TODO Need a way to define options on Instagram Tags.  One might not want EVERYTHING.
            # links = self.getArticleLinks(res[0].contents[2].contents[0].contents, links)

        except Exception as e:
            self.logger.error(f"Driver ran into a problem pulling links from a tag. {e}")

        return links

    def getArticleLinks(self, soupList: List, linkList: List) -> List[str]:

        for i in soupList:
            try:
                for l in i.contents:
                    linkList.append(
                        f"https://www.instagram.com{l.contents[0].attrs['href']}"
                    )
            except Exception as e:
                self.logger.error(f"Failed to extract post link. {e}")
        return linkList

    def getPostInfo(self, link: str) -> Articles:
        a = Articles(url=link, siteName=self.currentLink.name, tags="instagram, posts")

        self.driverGoTo(link)
        #source = self.getContent()
        soup = self.getParser(requestsContent=self.getContent())

        nameSplit = self.currentLink.name.split(" ")
        if nameSplit[1] == "tag":
            a.tags += f", tag, {nameSplit[2]}"
        elif nameSplit[1] == "user":
            a.tags += f", user, {nameSplit[2]}"

        # Get the title from the post
        title = soup.find_all(name="span", attrs={"class", ""})

        # Get the poster Avatar
        authorImages = soup.find_all(name="img")
        for i in authorImages:
            try:
                if "profile picture" in i.attrs["alt"]:
                    a.authorImage = i.attrs["src"]
                    break
            except:
                pass

        # get posters name
        authorName = soup.find_all(
            name="a", attrs={"class": "sqdOP yWX7d _8A5w5 ZIAjV"}
        )
        a.authorName = authorName[0].text

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
            try:
                if "photo by " in i.attrs["alt"].lower():
                    return i.attrs["src"]
                elif "photo shared by" in i.attrs["alt"].lower():
                    return i.attrs["src"]
            except:
                pass

        # Checking for images that have people/objects tagged
        for i in soup.find_all(name="img", attrs={"class": "FFVAD"}):
            # we are just going to take the first one that shows up in the list.
            return i.attrs["src"]

#    def __driverGet__(self, uri: str) -> None:
#        try:
#            self.driver.get(uri)
#            self.driver.implicitly_wait(5)
#        except Exception as e:
#            self.logger.error(f"Driver failed to get {uri}. Error: {e}")
#
#    def __close__(self) -> None:
#        try:
#            self.driver.close()
#        except Exception as e:
#            self.logger.error(f"Driver failed to close. Error: {e}")

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
