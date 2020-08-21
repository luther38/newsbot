
from typing import List
from json import loads
from newsbot import env, logger
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSRoot, RSSArticle
from newsbot.tables import Sources, DiscordWebHooks

class RedditReader(RSSReader):
    def __init__(self) -> None:
        self.uri = "https://reddit.com/r/aww/top.json"
        #self.rootUrl = "https://reddit.com/r/aww/top.rss"

        self.siteName = "Reddit"
        self.subreddits: List[str] = list()
        self.hooks = list()

        self.checkEnv()
        pass

    def checkEnv(self):
        # So we know what subreddits to pull
        res = Sources(name="Reddit").findAllByName()
        for r in res:
            r = r.replace("Reddit ", "")
            self.subreddits.append(r)

        # so we know later on if we pass this to discord
        dwh = DiscordWebHooks(name="Reddit").findAllByName()
        for r in dwh:
            r = r.replace("Reddit ", "")
            self.hooks.append(r)

    def getArticles(self):
        #TODO Flag NSFW
        allowNSFW = True

        rss = RSSRoot()
        for sr in self.subreddits:
            logger.debug(f"Collecting posts for '/r/{sr}'...")
            
            self.uri = f"https://reddit.com/r/{sr}/top.json"

            page = self.getParser()
            json = loads(page.text)
            
            try:
                if json['error'] == 404:
                    logger.error(f"Tried to access subreddit '{self.subreddit}' but got a 404.  Check to ensure that the name is correct and try again.'")
            except:
                # This only does the thing if we error out.
                pass

            for i in json['data']['children']:
                a = RSSArticle()
                a.siteName = f"Reddit {sr}"
                d = i['data']

                a.title = d['title']
                a.tags = d['subreddit']
                a.link = f"https://reddit.com{d['permalink']}"
                a.description = f"Subreddit: {sr}\r\nAuthor: {d['author']}"

                if d['is_video'] == True:
                    # Thumbnail needs to be the video content
                    a.thumbnail = d['media']['reddit_video']['fallback_url']
                    pass
                elif d['media_only'] == True:
                    print("review dis")
                else:
                    a.thumbnail = d['url']

                rss.articles.append(a)

        return rss