from typing import List
from json import loads
from newsbot import env, logger
from newsbot.sources.isources import ISources
from newsbot.tables import Sources, DiscordWebHooks, Articles
from time import sleep
from requests import get, Response
from bs4 import BeautifulSoup


class RedditReader(ISources):
    def __init__(self) -> None:
        self.uri = "https://reddit.com/r/aww/top.json"
        self.siteName = "Reddit"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False

        self.checkEnv()

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
        # TODO Flag NSFW
        allowNSFW = True

        # rss = RSSRoot()
        allArticles: List[Articles] = list()
        for source in self.links:
            subreddit = source.name.replace("Reddit ", "")

            logger.debug(f"Collecting posts for '/r/{subreddit}'...")

            self.uri = f"https://reddit.com/r/{subreddit}/top.json"

            siteContent = self.getContent()
            page = self.getParser(siteContent)
            json = loads(page.text)

            try:
                if json["error"] == 404:
                    logger.error(
                        f"Tried to access subreddit '{subreddit}' but got a 404.  Check to ensure that the name is correct and try again.'"
                    )
            except:
                # This only does the thing if we error out.
                pass

            try:
                for i in json["data"]["children"]:
                    a = Articles()
                    a.siteName = f"Reddit {subreddit}"

                    d = i["data"]

                    a.title = f"{d['title']}"
                    a.tags = d["subreddit"]
                    a.url = f"https://reddit.com{d['permalink']}"

                    # figure out what url we are going to display
                    if d["is_video"] == True:
                        a.video = d["media"]["reddit_video"]["fallback_url"]
                        a.videoHeight = d["media"]["reddit_video"]["height"]
                        a.videoWidth = d["media"]["reddit_video"]["width"]
                        a.thumbnail = self.getVideoThumbnail(d["preview"])

                    elif d["media_only"] == True:
                        print("review dis")
                    else:
                        a.thumbnail = d["url"]

                    allArticles.append(a)
            except Exception as e:
                logger.error(
                    f"Failed to extract Reddit post.  Too many connections? {e}"
                )

            sleep(5.0)

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

    def getVideoThumbnail(self, preview) -> str:
        try:
            return preview["images"][0]["source"]["url"]
        except:
            return ""
