from typing import List
from json import loads
from newsbot import env, logger
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSRoot, RSSArticle
from newsbot.tables import Sources, DiscordWebHooks, Articles
from time import sleep


class RedditReader(RSSReader):
    def __init__(self) -> None:
        self.uri = "https://reddit.com/r/aww/top.json"
        # self.rootUrl = "https://reddit.com/r/aww/top.rss"

        self.siteName = "Reddit"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()

        self.checkEnv()
        pass

    def checkEnv(self):
        # So we know what subreddits to pull
        res = Sources(name="Reddit").findAllByName()
        if len(res) >= 1:
            for r in res:
                self.links.append(r)

            # so we know later on if we pass this to discord
            dwh = DiscordWebHooks(name="Reddit").findAllByName()
            for r in dwh:
                self.hooks.append(r)

    def getArticles(self) -> List[Articles]:
        # TODO Flag NSFW
        allowNSFW = True

        #rss = RSSRoot()
        allArticles: List[Articles] = list()
        for source in self.links:
            subreddit = source.name.replace("Reddit ", "")

            logger.debug(f"Collecting posts for '/r/{subreddit}'...")

            self.uri = f"https://reddit.com/r/{subreddit}/top.json"

            page = self.getParser()
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
                    #a = RSSArticle()
                    a = Articles()
                    a.siteName = f"Reddit {subreddit}"

                    d = i["data"]

                    a.title = f"{d['title']}"
                    a.tags = d["subreddit"]
                    a.url = f"https://reddit.com{d['permalink']}"

                    # figure out what url we are going to display
                    if d["is_video"] == True:
                        a.video = d["media"]["reddit_video"]["fallback_url"]
                        a.videoHeight = d['media']['reddit_video']['height']
                        a.videoWidth = d['media']['reddit_video']['width']
                        pass
                    elif d["media_only"] == True:
                        print("review dis")
                    else:
                        a.thumbnail = d["url"]

                    allArticles.append(a)
            except Exception as e:
                logger.error(f"Failed to extract Reddit post.  Too many connections? {e}")

            sleep(15.0)

        return allArticles
