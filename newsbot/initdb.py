from newsbot.env import (
    EnvDiscordDetails,
    EnvFinalFantasyXIVDetails,
    EnvInstagramDetails,
    EnvPhantasyStarOnline2Details,
    EnvPokemonGoDetails,
    EnvRedditDetails,
    EnvRssDetails,
    EnvTwitchConfig,
    EnvTwitchDetails,
    EnvTwitterConfig,
    EnvTwitterDetails,
    EnvYoutubeDetails,
)
from os import name, system
from newsbot.env import Env
from typing import List
from abc import ABC, abstractclassmethod
from newsbot.sql.tables import (
    Sources,
    DiscordWebHooks,
    Icons,
    Settings,
    SourceLinks,
    DiscordWebHooks,
    SourceLinks,
    settings,
)

class FailedToIUpdateSource(Exception):
    """
    This is raised when the source is checked and the results are null.
    """

class IUpdateSource(ABC):
    @abstractclassmethod
    def update(self, values) -> None:
        pass

class UpdateSource(IUpdateSource):
    def updateSourceLinks(self, source: Sources, hookNames: List[str]) -> None:
        try:
            for h in hookNames:
                l: DiscordWebHooks = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{source.source}_{source.name}_>_{l.name}", sourceID=source.id, discordID=l.id
                )
                sl.update()
        except Exception as e:
            print(f"Failed to update SourceLinks for {source.source} {source.name}. Error: {e}")

class IUpdateSourceURL(ABC):
    @abstractclassmethod
    def __getUrl__(self, type:str, name: str) -> str:
        pass

class UpdateRSSSource(UpdateSource):
    sourceName: str = "rss"
    def update(self, values: List[EnvRssDetails]) -> None:
        for i in values:
            Sources(name=i.name, source=self.sourceName, url=i.url).update()
            s = Sources(name=i.name, source=self.sourceName).findBySourceAndName()
            self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

class UpdateYoutubeSource(UpdateSource):
    sourceName: str = "youtube"
    def update(self, values: List[EnvYoutubeDetails]) -> None:
        for i in values:
            Sources(name=i.name, source=self.sourceName, url=i.url).update()
            s: Sources = Sources(name=i.name, source=self.sourceName).findBySourceAndName()
            self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

class UpdateRedditSource(UpdateSource):
    sourceName: str = 'reddit'
    def update(self, values: List[EnvRedditDetails]) -> None:
        for i in values:
            Sources(name=i.subreddit, source=self.sourceName, url=f"https://reddit.com/r/{i.subreddit}/").update()
            s: Sources = Sources(name=i.subreddit, source=self.sourceName).findBySourceAndName()
            self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

class UpdateTwitchSource(UpdateSource):
    sourceName: str = "twitch"
    def update(self, values: List[EnvTwitchDetails]) -> None:
        for i in values:
            Sources(name=i.user, source=self.sourceName, url=f"https://twitch.tv/{i.user}/").update()
            s: Sources = Sources(name=i.user, source=self.sourceName).findBySourceAndName()
            self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

class UpdateTwitterSource(UpdateSource, IUpdateSourceURL): 
    sourceName: str = "twitter"
    def update(self, values: List[EnvTwitterDetails]) -> None:
        for i in values:
            s = Sources(
                name=i.name, 
                source=self.sourceName, 
                type=i.type.lower(), 
                url=self.__getUrl__(
                    type=i.type.lower(), 
                    name=i.name
                )
            )
            s.update()
            s: Sources = Sources(name=i.name, source=self.sourceName, type=i.type.lower()).findBySourceNameType()
            self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

    def __getUrl__(self, type: str, name: str) -> str:
        root: str = "https://twitter.com"
        if   type == "user": return f"{root}/{name}/"
        elif type == "tag":  return f"{root}/hashtag/{name}"
        else:                return root

class UpdateInstagramSource(UpdateSource, IUpdateSourceURL):
    sourceName: str = "instagram"
    def update(self, values: List[EnvInstagramDetails]) -> None:
        for i in values:
            uri: str = self.__getUrl__(type=i.type.lower(), name=i.name)
            Sources(
                name=i.name, source=self.sourceName, type=i.type.lower(), url=uri
            ).update()
            s: Sources = Sources(name=i.name, source=self.sourceName).findBySourceAndName()
            self.updateSourceLinks(source=s, hookNames=i.discordLinkName)

    def __getUrl__(self, type: str, name: str) -> str:
        root: str = "https://instagram.com"
        if type == "user":  return f"{root}/{name}/"
        elif type == "tag": return f"{root}/explore/tags/{name}"
        else:               return root

class UpdatePokemonGoHubSource(UpdateSource):
    sourceName: str = 'pokemongohub'
    def update(self, values: EnvPokemonGoDetails) -> None:
        try:
            Sources(
                name=self.sourceName,
                source=self.sourceName,
                enabled=values.enabled,
                url="https://pokemongohub.net",
            ).update()
            s: Sources = Sources(name=self.sourceName).findByName()
            self.updateSourceLinks(source=s, hookNames=values.discordLinkName)
        except Exception as e:
            print(f"Failed to enable 'Pokemon Go Hub' source. Error: {e}")

class UpdatePhantasyStarOnline2Source(UpdateSource):
    sourceName: str = "phantasystaronline2"
    def update(self, values: EnvPhantasyStarOnline2Details) -> None:
        try:
            Sources(
                name=self.sourceName,
                source=self.sourceName,
                enabled=values.enabled,
                url="https://pso2.com",
            ).update()
            s: Sources = Sources(name=self.sourceName).findByName()
            self.updateSourceLinks(source=s, hookNames=values.discordLinkName)
        except Exception as e:
            print(f"Failed to enabled 'Phantasy Star Online 2' source. Error: {e}")

class UpdateFinalFantasyXIVSource(UpdateSource):
    def __init__(self, topic: str, enabled: bool) -> None:
        self.topic: str = topic
        self.enabled: bool = enabled
        self.sourceName: str = "finalfantasyxiv"
        self.url: str = "https://finalfantasyxiv.com"

    def update(self, values: EnvFinalFantasyXIVDetails) -> None:  
        try:
            s = Sources(name=self.topic, source=self.sourceName, enabled=self.enabled, url=self.url)
            s.update()
            s = Sources(name=self.topic, source=self.sourceName).findBySourceAndName()
            self.updateSourceLinks(source=s, hookNames=values.discordLinkName)
        except Exception as e:
            print(f"Failed to enabled '{self.topic}' in '{self.sourceName}' source. Error: {e}")


class InitDb:
    def __init__(self) -> None:
        self.e = Env()

    def runMigrations(self) -> None:
        system("alembic upgrade head")

    def clearOldRecords(self) -> None:
        # clear our the table cache from last startup
        Sources().clearTable()
        DiscordWebHooks().clearTable()

    def addStaticIcons(self) -> None:
        # Icons().clearTable()
        Icons(
            site="Default Pokemon Go Hub",
            fileName="https://pokemongohub.net/wp-content/uploads/2017/04/144.png",
        ).update()
        Icons(
            site="Default Phantasy Star Online 2",
            fileName="https://raw.githubusercontent.com/jtom38/newsbot/master/mounts/icons/pso2.jpg",
        ).update()
        Icons(
            site="Default Final Fantasy XIV",
            fileName="https://img.finalfantasyxiv.com/lds/h/0/U2uGfVX4GdZgU1jASO0m9h_xLg.png",
        ).update()
        Icons(
            site="Default Reddit",
            fileName="https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png",
        ).update()
        Icons(
            site="Default YouTube",
            fileName="https://www.youtube.com/s/desktop/c46c1860/img/favicon_144.png",
        ).update()
        Icons(
            site="Default Twitter",
            fileName="https://abs.twimg.com/responsive-web/client-web/icon-ios.8ea219d5.png",
        ).update()
        Icons(
            site="Default Instagram",
            fileName="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png",
        ).update()
        Icons(
            site="Default Twitch",
            fileName="https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png",
        ).update()

        # RSS based sites
        Icons(
            site="Default Engadget",
            fileName="https://s.yimg.com/kw/assets/apple-touch-icon-120x120.png",
        ).update()
        Icons(
            site="Default GitHub",
            fileName="https://github.githubassets.com/images/modules/open_graph/github-logo.png",
        ).update()

    def rebuildCache(
        self, twitchConfig: EnvTwitchConfig, twitterConfig: EnvTwitterConfig
        ) -> None:
        Settings().clearTable()
        Settings(key="twitch clips enabled", value=twitchConfig.monitorClips).add()
        Settings(key="twitch vod enabled", value=twitchConfig.monitorVod).add()
        Settings(
            key="twitch livestreams enabled", value=twitchConfig.monitorLiveStreams
        ).add()
        Settings(key="twitter.prefered.lang", value=twitterConfig.preferedLang).add()
        Settings(key="twitter.ignore.retweet", value=twitterConfig.ignoreRetweet).add()

    def updateDiscordValues(self, values: List[EnvDiscordDetails]) -> None:
        for v in values:
            if v.name == "":
                v.name = f"{v.server} - {v.channel}"

            d = DiscordWebHooks(
                name=v.name, server=v.server, channel=v.channel, url=v.url
            )
            d.update()

    def runDatabaseTasks(self) -> None:
        self.updateDiscordValues(values=self.e.discord_values)
        UpdateRSSSource().update(values=self.e.rss_values)
        UpdateYoutubeSource().update(values=self.e.youtube_values)
        UpdateRedditSource().update(values=self.e.reddit_values)
        UpdateTwitchSource().update(values=self.e.twitch_values)
        UpdateTwitterSource().update(values=self.e.twitter_values)
        UpdateInstagramSource().update(values=self.e.instagram_values)
        UpdatePokemonGoHubSource().update(values=self.e.pogo_values)
        UpdatePhantasyStarOnline2Source().update(values=self.e.pso2_values)
        UpdateFinalFantasyXIVSource("topics", self.e.ffxiv_values.topicsEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("notices", self.e.ffxiv_values.noticesEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("maintenance", self.e.ffxiv_values.maintenanceEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("updates", self.e.ffxiv_values.updateEnabled).update(values=self.e.ffxiv_values)
        UpdateFinalFantasyXIVSource("status", self.e.ffxiv_values.statusEnabled).update(values=self.e.ffxiv_values)
        
        self.addStaticIcons()
        self.rebuildCache(
            twitchConfig=self.e.twitch_config, twitterConfig=self.e.twitter_config
        )
