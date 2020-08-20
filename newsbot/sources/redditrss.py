
from json import loads
from newsbot import env, logger
from newsbot.sources.rssreader import RSSReader
from newsbot.collections import RSSRoot, RSSArticle

class RedditReader(RSSReader):
    def __init__(self) -> None:
        self.uri = "https://reddit.com/r/aww/top.json"
        self.rootUrl = "https://reddit.com/r/aww/top.rss"
        self.siteName = "Reddit"
        self.subreddit:str = "ProgrammerHumor"
        self.links = list()
        self.hooks = list()

        self.checkEnv()
        pass

    def checkEnv(self):
        self.hooks = env.redditHook01
        

    def getArticles(self):
        allowNSFW = True
        rss = RSSRoot()
        
        self.uri = f"https://reddit.com/r/{self.subreddit}/top.json"

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
            a.siteName = f"Reddit - {self.subreddit}"
            d = i['data']

            a.title = d['title']
            a.tags = d['subreddit']
            a.link = f"https://reddit.com{d['permalink']}"
            a.description = f"Subreddit: {self.subreddit}\r\nAuthor: {d['author']}"

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