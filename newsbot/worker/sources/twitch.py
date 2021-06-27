from typing import List
from newsbot.core.logger import Logger
from newsbot.core.constant import SourceName
from newsbot.core.api import TwitchAPI
from newsbot.worker.sources.common import BSources
from newsbot.core.sql.tables import Articles, Sources, DiscordWebHooks
from newsbot.core.cache import Cache


class TwitchReader(BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://twitch.tv/"
        self.siteName: str = SourceName.TWITCH.value
        
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        self.session: Session = None
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
            user_id = self.cache.find(key=f"twitch.{userName}.user_id")
            display_name = self.cache.find(key=f"twitch.{userName}.display")
            profile_image_url = self.cache.find(key=f"twitch.{userName}.profile_image_url")

            enableClips = self.cache.find(key="twitch.clips.enabled")
            if enableClips == "1":
                clips: List[TwitchClip] = self.api.getClips(self.auth, user_id=user_id)
                for v in clips:
                    try:
                        a = Articles(
                            siteName=f"twitch user {display_name}",
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"twitch, clip, {display_name}",
                            title=v.title,
                            pubDate=v.created_at,
                            url=v.url,
                            thumbnail=v.thumbnail_url,
                            description="A new clip has been posted! You can watch it with the link below.",
                            sourceType=SourceName.TWITCH.value,
                            sourceName=userName,
                        )
                        allPosts.append(a)
                    except Exception as e:
                        self.logger.error(e)

            enableVoD = self.cache.find(key="twitch.vod.enable")
            if enableVoD == "1":
                videos: List[TwitchVideo] = self.api.getVideos(
                    self.auth, user_id=user_id
                )
                for v in videos:
                    try:
                        a = Articles(
                            siteName=f"twitch user {display_name}",
                            authorName=display_name,
                            authorImage=profile_image_url,
                            tags=f"twitch, vod, {display_name}",
                            # description = v.description,
                            title=v.title,
                            description="A new video has been posed! You can watch it with the link below.",
                            pubDate=v.published_at,
                            url=v.url,
                            sourceType=SourceName.TWITCH.value,
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
        user_id = self.cache.find(key=f"twitch.{userName}.user_id")
        if user_id == "":
            # Take the value and add it to the cache so we dont need to call the API for this
            user: TwitchUser = self.api.getUser(self.auth, userName)
            user_id = self.cache.add(key=f"twitch.{userName}.user_id", value=user.id)
            display_name = self.cache.add(
                key=f"twitch.{userName}.display_name", value=user.display_name
            )
            profile_image_url = self.cache.add(
                key=f"twitch.{userName}.profile_image_url",
                value=user.profile_image_url,
            )
        else:
            pass
