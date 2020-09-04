
from typing import List
from newsbot.tables import Sources, DiscordWebHooks
from newsbot.sources.rssreader import RSSReader

class YoutubeReader(RSSReader):
    def __init__(self):
        self.uri: str = "https://youtube.com"
        self.siteName: str = "Youtube"

        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()

        self.checkEnv()
        pass

