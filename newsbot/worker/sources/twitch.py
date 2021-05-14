from typing import List
from newsbot.core.logger import Logger
from newsbot.core.api import TwitchAPI
from newsbot.worker.sources.common import (
    ISources,
    BSources,
    UnableToFindContent,
    UnableToParseContent,
)
from newsbot.core.sql.tables import Articles, Sources, DiscordWebHooks
from newsbot.core.cache import Cache


class TwitchReader(ISources, BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://twitch.tv/"
        self.siteName: str = "Twitch"
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        pass

    def getArticles(self) -> List[Articles]:
        self.logger.debug("Checking Twitch for updates.")
        self.api = TwitchAPI()
        self.auth = self.api.auth()

        allPosts = list()
        for i in self.links:
            userName = i.name
            self.logger.debug(f"Checking Twitch user {userName} for updates.")

            self.cacheUserId(userName=userName)

            # We have cached this information already
            user_id = Cache(key=f"twitch {userName} user_id").find()
            display_name = Cache(key=f"twitch {userName} display").find()
            profile_image_url = Cache(key=f"twitch {userName} profile_image_url").find()

            enableClips = Cache(key="twitch.clips.enabled").find()
            if enableClips.lower() == "true":
                clips: List[TwitchClip] = self.api.getClips(self.auth, user_id=user_id)
                for v in clips:
                    try:
                        a = Articles(
                            siteName=f"Twitch user {display_name}",
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"Twitch, clip, {display_name}",
                            title=v.title,
                            pubDate=v.created_at,
                            url=v.url,
                            thumbnail=v.thumbnail_url,
                            description="A new clip has been posted! You can watch it with the link below.",
                            sourceType="Twitch",
                            sourceName=userName,
                        )
                        allPosts.append(a)
                    except Exception as e:
                        self.logger.error(e)

            enableVoD = Cache(key="twitch vod enable").find()
            if enableVoD.lower() == "true":
                videos: List[TwitchVideo] = self.api.getVideos(
                    self.auth, user_id=user_id
                )
                for v in videos:
                    try:
                        a = Articles(
                            siteName=f"Twitch user {display_name}",
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"Twitch, vod, {display_name}",
                            # description = v.description,
                            title=v.title,
                            description="A new video has been posed! You can watch it with the link below.",
                            pubDate=v.published_at,
                            url=v.url,
                            sourceType="Twitch",
                            sourceName=userName,
                        )
                        thumb: str = v.thumbnail_url
                        thumb = thumb.replace("%{width}", "600")
                        thumb = thumb.replace("%{height}", "400")
                        a.thumbnail = thumb
                        allPosts.append(a)
                    except Exception as e:
                        self.logger.error(e)

        return allPosts

    def cacheUserId(self, userName: str) -> None:
        user_id = Cache(key=f"twitch {userName} user_id").find()
        if user_id == "":
            # Take the value and add it to the cache so we dont need to call the API for this
            user: TwitchUser = self.api.getUser(self.auth, userName)
            user_id = Cache(key=f"twitch {userName} user_id", value=user.id).add()
            display_name = Cache(
                key=f"twitch {userName} display_name", value=user.display_name
            ).add()
            profile_image_url = Cache(
                key=f"twitch {userName} profile_image_url",
                value=user.profile_image_url,
            ).add()
        else:
            pass