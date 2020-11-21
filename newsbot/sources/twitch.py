from typing import List
from newsbot import env
from newsbot.logger import logger
from newsbot.api.twitch import *
from newsbot.sources.isources import ISources, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
from newsbot.cache import Cache
from requests import get, Response
from bs4 import BeautifulSoup

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
        logger.debug("Checking Twitch for updates.")
        api = TwitchAPI()
        auth = api.auth()

        allPosts = list()
        for i in self.links:
            s = i.name.split(' ')
            userName = s[2]
            logger.debug(f"Checking Twitch user {userName} for updates.")

            user_id = Cache(key=f"twitch {userName} user_id").find()
            if user_id == "":
                # Take the value and add it to the cache so we dont need to call the API for this
                user: TwitchUser = api.getUser(auth, userName)
                user_id = Cache(key=f"twitch {userName} user_id", value=user.id).add()
                display_name = Cache(key=f"twitch {userName} display_name", value=user.display_name).add()
                profile_image_url = Cache(key=f"twitch {userName} profile_image_url", value=user.profile_image_url).add()
            else: 
                # We have cached this information already
                display_name = Cache(key=f"twitch {userName} display").find()
                profile_image_url = Cache(key=f"twitch {userName} profile_image_url").find()

            enableClips = Cache(key="twitch clips enabled").find()
            if enableClips.lower() == 'true':
                clips: List[TwitchClip] = api.getClips(auth, user_id=user_id)
                for v in clips:
                    try:
                        a = Articles(
                            siteName = f"Twitch user {display_name}",
                            authorName = display_name,
                            authorImage = profile_image_url,
                            tags = f"Twitch, clip, {display_name}",
                            title= v.title,
                            pubDate = v.created_at,
                            url = v.url,
                            thumbnail = v.thumbnail_url,
                            description= "A new clip has been posted! You can watch it with the link below."
                        )
                        allPosts.append(a)
                    except Exception as e:
                        logger.error(e)

            enableVoD = Cache(key="twitch vod enable").find()
            if enableVoD.lower() == 'true':
                videos: List[TwitchVideo] = api.getVideos(auth, user_id=user_id)
                for v in videos:
                    try:
                        a = Articles(
                            siteName=f"Twitch user {display_name}",
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"Twitch, vod, {display_name}",
                            #description = v.description,
                            title = v.title,
                            description= "A new video has been posed! You can watch it with the link below.",
                            pubDate = v.published_at,
                            url = v.url
                        )            
                        thumb: str = v.thumbnail_url
                        thumb = thumb.replace('%{width}','600')
                        thumb = thumb.replace('%{height}', '400')
                        a.thumbnail = thumb
                        allPosts.append(a)
                    except Exception as e:
                        logger.error(e)
        
        return allPosts

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
