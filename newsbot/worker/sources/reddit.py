from typing import List
from json import loads

from bs4 import BeautifulSoup
from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Articles, Sources, DiscordWebHooks
from newsbot.core.cache import Cache
from newsbot.worker.sources.driver import BFirefox
from newsbot.worker.sources.common import BSources
from time import sleep

class RedditReader(BSources, BFirefox):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://reddit.com/r/aww/top.json"
        self.siteName = "Reddit"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False

        self.checkEnv(self.siteName)

    def getArticles(self) -> List[Articles]:
        # TODO Flag NSFW
        # allowNSFW = True

        self.driver = self.driverStart()

        # rss = RSSRoot()
        allArticles: List[Articles] = list()
        for source in self.links:
            authorImage = ""
            authorName = ""
            subreddit = source.name

            self.logger.debug(f"Collecting posts for '/r/{subreddit}'...")

            # Add the info we get via Selenium to the Cache to avoid pulling it each time.
            authorImage = Cache(key=f"reddit.{subreddit}.authorImage").find()
            authorName = Cache(key=f"reddit.{subreddit}.authorName").find()
            if authorImage == "":
                soup = self.getSubRedditSoup(subreddit)
                authorImage = self.findSubThumbnail(soup)
                subTagline = self.findTagline(soup)

                if subTagline != "":
                    authorName = f"/r/{subreddit} - {subTagline}"
                else:
                    authorName = f"/r/{subreddit}"

                Cache(key=f"reddit.{subreddit}.authorImage", value=authorImage).add()
                Cache(key=f"reddit.{subreddit}.authorName", value=authorName).add()

            # Now check the RSS
            posts = self.getPosts(subreddit)
            for p in posts:
                a = Articles(url=f"https://reddit.com{p['data']['permalink']}")
                if (a.exists() == False ):
                    allArticles.append(
                        self.getPostDetails(
                            p["data"], subreddit, authorName, authorImage
                        )
                    )

            sleep(5.0)

        self.driverClose()
        return allArticles

    def getSubRedditSoup(self, subreddit: str) -> BeautifulSoup:
        # Collect values that we do not get from the RSS
        self.uri = f"https://reddit.com/r/{subreddit}"
        self.driverGoTo(self.uri)
        soup = self.getParser(seleniumContent=self.driverGetContent())
        return soup

    def findSubThumbnail(self, soup: BeautifulSoup) -> str:
        authorImage: str = ""

        #Find the 
        subImages = soup.find_all(name="img", attrs={"class": "Mh_Wl6YioFfBc9O1SQ4Jp"})

        if len(subImages) != 0:
            # Failed to find the custom icon.  The sub might not have a custom CSS.
            authorImage = subImages[0].attrs["src"]

        if authorImage == "":
            # I am not sure how to deal with svg images at this time.  
            # Going to throw in the default reddit icon.
            subImages = soup.find_all(
                name="svg", attrs={"class": "ixfotyd9YXZz0LNAtJ25N"}
            )
            if len(subImages) == 1:
                authorImage = "https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png"
        return authorImage

    def findTagline(self, soup: BeautifulSoup) -> str:
        tagLine: str = ''
        try:
            subName = soup.find_all(name="h1", attrs={"class": "_2yYPPW47QxD4lFQTKpfpLQ"} )
            tagLine = subName[0].text
            assert subName[0].text
        except Exception as e:
            self.logger.critical(f"Failed to find the subreddit name in the html. Error {e}")
        return tagLine

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
            a = Articles(
                url=f"https://reddit.com{obj['permalink']}",
                siteName= f"Reddit {subreddit}",
                authorName=authorName,
                authorImage=authorImage,
                title=obj['title'],
                tags=obj["subreddit"],
                sourceType = "Reddit",
                sourceName = subreddit
            )

            # figure out what url we are going to display
            if obj["is_video"] == True:
                a.video = obj["media"]["reddit_video"]["fallback_url"]
                a.videoHeight = obj["media"]["reddit_video"]["height"]
                a.videoWidth = obj["media"]["reddit_video"]["width"]
                a.thumbnail = self.getVideoThumbnail(obj["preview"])

            elif obj["media_only"] == True:
                self.logger.warning(f"Found 'media_only' object. url: {a.url}")
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
            self.logger.error(
                f"Failed to extract Reddit post.  Too many connections? {e}"
            )
