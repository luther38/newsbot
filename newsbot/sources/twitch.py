from typing import List
from newsbot import logger, env
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from requests import get, Response
from bs4 import BeautifulSoup
from newsbot.api.twitch import TwitchAPI


class TwitchReader(ISources):
    def __init__(self) -> None:
        self.uri = "https://twitch.tv/"
        self.siteName: str = "Twitch"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv()
        pass

    def checkEnv(self) -> None:
        # Check if site was requested.
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
        api = TwitchAPI()
        auth = api.auth()

        user = api.getUser(auth, "fayttt")

        # we can get the game info here, but no place to store it just yet
        #channel = api.searchForUser(auth, "fayttt")
        clips = api.getClips(auth, user_id=user.id)
        videos = api.getVideos(auth, user_id=user.id)
        allPosts = list()
        for v in videos:
            a = Articles(
                siteName=f"Twitch user {user.display_name}",
                authorName= user.display_name,
                authorImage=user.profile_image_url,
                tags=f"Twitch, vod, {user.display_name}"
            )            
            a.description = v.description
            a.title = v.title
            a.description = "A new VOD has been posed! You can watch it with the link below."
            a.pubDate = v.published_at
            thumb: str = v.thumbnail_url
            thumb = thumb.replace('%{width}','600')
            thumb = thumb.replace('%{height}', '400')
            a.thumbnail = thumb
            a.url = v.url
            allPosts.append(a)
            pass

        

        return allPosts

        pass

    def getContent(self) -> str:
        try:
            headers = self.getHeaders()
            res: Response = get(self.uri, headers=headers)
            return str(res.content)
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, siteContent: str) -> BeautifulSoup:
        try:
            return BeautifulSoup(siteContent, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")
