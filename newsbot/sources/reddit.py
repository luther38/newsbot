from typing import List
from json import loads
from newsbot import env
from newsbot.logger import Logger
from newsbot.tables import Sources, DiscordWebHooks, Articles
from newsbot.cache import Cache
from newsbot.sources.common import BChrome, ISources, BSources
from time import sleep
from requests import get, Response
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions


class RedditReader(ISources, BSources, BChrome):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://reddit.com/r/aww/top.json"
        self.siteName = "Reddit"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False

        self.checkEnv(self.siteName)

#    def checkEnv(self) -> None:
#        # Check if site was requested.
#        self.outputDiscord = self.isDiscordEnabled(self.siteName)
#        if self.outputDiscord == True:
#            self.hooks = self.getDiscordList(self.siteName)
#
#        self.sourceEnabled = self.isSourceEnabled(self.siteName)
#        if self.sourceEnabled == True:
#            self.links = self.getSourceList(self.siteName)

    def getArticles(self) -> List[Articles]:
        # TODO Flag NSFW
        #allowNSFW = True

        self.driver = self.driverStart()

        # rss = RSSRoot()
        allArticles: List[Articles] = list()
        for source in self.links:
            authorImage = ""
            authorName = ""
            subreddit = source.name.replace("Reddit ", "")

            self.logger.debug(f"Collecting posts for '/r/{subreddit}'...")

            # Add the info we get via Selenium to the Cache to avoid pulling it each time.
            authorImage = Cache(key=f"reddit {subreddit} authorImage").find()
            authorName = Cache(key=f"reddit {subreddit} authorName").find()
            if authorImage == "":
                # Collect values that we do not get from the RSS
                self.uri = f"https://reddit.com/r/{subreddit}"
                self.driverGoTo(self.uri)
                #source = self.driverGetContent()
                soup = self.getParser(seleniumContent=self.driverGetContent())

                subImages = soup.find_all(
                    name="img", attrs={"class": "Mh_Wl6YioFfBc9O1SQ4Jp"}
                )
                if len(subImages) != 0:
                    # Failed to find the custom icon.  The sub might not have a custom CSS.
                    authorImage = subImages[0].attrs["src"]

                if authorImage == "":
                    # I am not sure how to deal with svg images at this time.  Going to throw in the default reddit icon.
                    subImages = soup.find_all(
                        name="svg", attrs={"class": "ixfotyd9YXZz0LNAtJ25N"}
                    )
                    if len(subImages) == 1:
                        authorImage = "https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png"

                subName = soup.find_all(
                    name="h1", attrs={"class": "_2yYPPW47QxD4lFQTKpfpLQ"}
                )
                authorName = f"/r/{subreddit} - {subName[0].text}"
                Cache(key=f"reddit {subreddit} authorImage", value=authorImage).add()
                Cache(key=f"reddit {subreddit} authorName", value=authorName).add()

            # Now check the RSS
            posts = self.getPosts(subreddit)
            for p in posts:
                if (
                    Articles(url=f"https://reddit.com{p['data']['permalink']}").exists() == False
                ):
                    allArticles.append(
                        self.getPostDetails(
                            p["data"], subreddit, authorName, authorImage
                        )
                    )

            sleep(5.0)

        self.driverClose()
        return allArticles

#    def getContent(self) -> str:
#        try:
#            headers = self.getHeaders()
#            res = get(self.uri, headers=headers)
#            return res.text
#        except Exception as e:
#            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")
#
#    def getDriverContent(self) -> str:
#        return self.driver.page_source
#
#    def getParser(self, siteContent: str) -> BeautifulSoup:
#        try:
#            return BeautifulSoup(siteContent, features="html.parser")
#        except Exception as e:
#            self.logger.critical(f"failed to parse data returned from requests. {e}")

    def getVideoThumbnail(self, preview) -> str:
        try:
            return preview["images"][0]["source"]["url"]
        except:
            return ""

    def getPosts(self, subreddit: str) -> None:
        rootUri = f"https://reddit.com/r/{subreddit}"
        items = (f"{rootUri}/top.json", f"{rootUri}.json")
        for i in items:
            try:
                self.uri = i
                siteContent = self.getContent()
                page = self.getParser(requestsContent=siteContent)
                json = loads(page.text)
                items = json["data"]["children"]
                if len(items) >= 25:
                    return items
            except:
                pass

    def getPostDetails(
        self, obj: dict, subreddit: str, authorName: str, authorImage: str
        ) -> Articles:
        try:

            a = Articles()
            a.url = f"https://reddit.com{obj['permalink']}"
            a.siteName = f"Reddit {subreddit}"
            a.authorImage = authorImage
            a.authorName = authorName
            a.title = f"{obj['title']}"
            a.tags = obj["subreddit"]

            # figure out what url we are going to display
            if obj["is_video"] == True:
                a.video = obj["media"]["reddit_video"]["fallback_url"]
                a.videoHeight = obj["media"]["reddit_video"]["height"]
                a.videoWidth = obj["media"]["reddit_video"]["width"]
                a.thumbnail = self.getVideoThumbnail(obj["preview"])

            elif obj["media_only"] == True:
                print("review dis")
            elif "gallery" in obj["url"]:
                self.uri = obj["url"]
                source = self.getContent()
                soup = self.getParser(requestsContent=source)
                try:
                    images = soup.find_all(
                        name="img", attrs={"class": "_1dwExqTGJH2jnA-MYGkEL-"}
                    )
                    pictures: str = ""
                    for i in images:
                        pictures += f"{i.attrs['src']} "
                    a.thumbnail = pictures
                except Exception as e:
                    self.logger.error(
                        f"Failed to find the images on a reddit gallery.  CSS might have changed."
                    )
            else:
                a.thumbnail = obj["url"]

            return a
        except Exception as e:
            self.logger.error(f"Failed to extract Reddit post.  Too many connections? {e}")

    # Selenium Code
#    def getWebDriver(self) -> Chrome:
#        options = ChromeOptions()
#        options.add_argument("--disable-extensions")
#        options.add_argument("--headless")
#        options.add_argument("--no-sandbox")
#        options.add_argument("--disable-dev-shm-usage")
#        try:
#            driver = Chrome(options=options)
#            return driver
#        except Exception as e:
#            self.logger.critical(f"Chrome Driver failed to start! Error: {e}")
#
#    def __driverGet__(self, uri: str) -> None:
#        try:
#            self.driver.get(uri)
#            # self.driver.implicitly_wait(30)
#            sleep(5)
#        except Exception as e:
#            self.logger.error(f"Driver failed to get {uri}. Error: {e}")
#
#    def __driverQuit__(self):
#        self.driver.quit()
