from typing import List
from json import loads
from newsbot.core.logger import Logger
from newsbot.core.sql.tables import Articles, Sources, DiscordWebHooks
from newsbot.core.cache import Cache
from newsbot.worker.sources.common import BChrome, ISources, BSources
from time import sleep

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
            authorImage = Cache(key=f"reddit {subreddit} authorImage").find()
            authorName = Cache(key=f"reddit {subreddit} authorName").find()
            if authorImage == "":
                # Collect values that we do not get from the RSS
                self.uri = f"https://reddit.com/r/{subreddit}"
                self.driverGoTo(self.uri)
                # source = self.driverGetContent()
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
                    Articles(url=f"https://reddit.com{p['data']['permalink']}").exists()
                    == False
                ):
                    allArticles.append(
                        self.getPostDetails(
                            p["data"], subreddit, authorName, authorImage
                        )
                    )

            sleep(5.0)

        self.driverClose()
        return allArticles

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
            a.sourceType = "Reddit"
            a.sourceName = subreddit

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
            self.logger.error(
                f"Failed to extract Reddit post.  Too many connections? {e}"
            )