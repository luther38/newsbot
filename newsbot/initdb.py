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
from json import loads, dumps


class InitDb:
    def __init__(self) -> None:
        self.e = Env()
        # self.e.readEnv()
        pass

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

    def updateRss(self, values: List[EnvRssDetails]) -> None:
        # loop over all the objects found in the env
        for i in values:
            # Run update the value based on its existing name
            Sources(name=i.name, source="RSS", url=i.url).update()

            # Get the Source object by name
            s = Sources(name=i.name).findByName()

            # Get the DiscordWebHook by Name
            for h in i.discordLinkName:
                l = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_{s.name}_>_{l.name}",
                    sourceID=s.id,
                    discordID=l.id,
                )
                sl.update()

        # print('l')

    def updateYoutube(self, values: List[EnvYoutubeDetails]) -> None:
        # loop over all the objects found in the env
        for i in values:
            # Run update the value based on its existing name
            Sources(name=i.name, source="Youtube", url=i.url).update()

            # Get the Source object by name
            s: Sources = Sources(name=i.name).findByName()

            # Get the DiscordWebHook by Name
            for h in i.discordLinkName:
                l = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_{s.name}_>_{l.name}",
                    sourceID=s.id,
                    discordID=l.id,
                )
                sl.update()

    def updateReddit(self, values: List[EnvRedditDetails]) -> None:
        # loop over all the objects found in the env
        for i in values:
            uri = f"https://reddit.com/r/{i.subreddit}/"
            Sources(name=i.subreddit, source="reddit", url=uri).update()
            s: Sources = Sources(name=i.subreddit).findByName()
            for h in i.discordLinkName:
                l = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_{s.name}_>_{l.name}",
                    sourceID=s.id,
                    discordID=l.id,
                )
                sl.update()

    def updateTwitch(self, values: List[EnvTwitchDetails]) -> None:
        for i in values:
            uri = f"https://twitch.tv/{i.user}/"
            Sources(name=i.user, source="twitch", url=uri).update()
            s: Sources = Sources(name=i.user).findByName()
            for h in i.discordLinkName:
                l = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_{s.name}_>_{l.name}",
                    sourceID=s.id,
                    discordID=l.id,
                )
                sl.update()

    def updateTwitter(self, values: List[EnvTwitterDetails]) -> None:
        for i in values:
            if i.type.lower() == "user":
                uri = f"https://twitter.com/{i.name}/"
            elif i.type.lower() == "tag":
                uri = f"https://twitter.com/hashtag/{i.name}"
            else:
                uri = "https://twitter.com"
            Sources(
                name=i.name, source="twitter", type=i.type.lower(), url=uri
            ).update()
            s: Sources = Sources(name=i.name).findByName()
            for h in i.discordLinkName:
                l = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_{s.name}_>_{l.name}",
                    sourceID=s.id,
                    discordID=l.id,
                )
                sl.update()

    def updateInstagram(self, values: List[EnvInstagramDetails]) -> None:
        for i in values:
            if i.type.lower() == "user":
                uri = f"https://instagram.com/{i.name}/"
            elif i.type.lower() == "tag":
                uri = f"https://instagram.com/explore/tags/{i.name}"
            else:
                uri = "https://instagram.com"
            Sources(
                name=i.name, source="instagram", type=i.type.lower(), url=uri
            ).update()
            s: Sources = Sources(name=i.name).findByName()
            for h in i.discordLinkName:
                l = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_{s.name}_>_{l.name}",
                    sourceID=s.id,
                    discordID=l.id,
                )
                sl.update()

    def updatePokemonGo(self, values: EnvPokemonGoDetails) -> None:
        try:
            Sources(
                name="Pokemon Go Hub",
                source="Pokemon Go Hub",
                enabled=values.enabled,
                url="https://pokemongohub.net",
            ).update()
            s: Sources = Sources(name="Pokemon Go Hub").findByName()
            for h in values.discordLinkName:
                l: DiscordWebHooks = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_>_{l.name}", sourceID=s.id, discordID=l.id
                )
                sl.update()
        except Exception as e:
            print(f"Failed to enable 'Pokemon Go Hub' source. Error: {e}")

    def updatePhantasyStarOnline2(self, values: EnvPhantasyStarOnline2Details) -> None:
        try:
            Sources(
                name="Phantasy Star Online 2",
                source="Phantasy Star Online 2",
                enabled=values.enabled,
                url="https://pso2.com",
            ).update()
            s: Sources = Sources(name="Phantasy Star Online 2").findByName()
            for h in values.discordLinkName:
                l: DiscordWebHooks = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_>_{l.name}", sourceID=s.id, discordID=l.id
                )
                sl.update()
        except Exception as e:
            print(f"Failed to enabled 'Phantasy Star Online 2' source. Error: {e}")

    def updateFinalFantasyXIV(self, values: EnvFinalFantasyXIVDetails) -> None:
        name: str = "Final Fantasy XIV"
        url: str = "https://finalfantasyxiv.com"
        try:
            s = Sources(
                name=name,
                source=name,
                enabled=values.allEnabled,
                value= dumps([
                    { 'key':'all','value':values.allEnabled },
                    { 'key':'topics','value':values.topicsEnabled },
                    { 'key':'notices','value':values.noticesEnabled },
                    { 'key':'maintenance','value':values.maintenanceEnabled },
                    { 'key':'updates','value':values.updateEnabled },
                    { 'key':'status','value':values.statusEnabled }
                ]),
                url=url,
            )
            s.update()

            s: Sources = Sources(name=name).findByName()
            for h in values.discordLinkName:
                l: DiscordWebHooks = DiscordWebHooks(name=h).findByName()
                sl = SourceLinks(
                    name=f"{s.source}_>_{l.name}", sourceID=s.id, discordID=l.id
                )
                sl.update()
        except Exception as e:
            print(f"Failed to enabled '{name}' source. Error: {e}")

    def runDatabaseTasks(self) -> None:
        # Inject new values based off env values
        self.updateDiscordValues(values=self.e.discord_values)
        self.updateRss(values=self.e.rss_values)
        self.updateYoutube(values=self.e.youtube_values)
        self.updateReddit(values=self.e.reddit_values)
        self.updateTwitch(values=self.e.twitch_values)
        self.updateTwitter(values=self.e.twitter_values)
        self.updateInstagram(values=self.e.instagram_values)
        self.updatePokemonGo(values=self.e.pogo_values)
        self.updatePhantasyStarOnline2(values=self.e.pso2_values)
        self.updateFinalFantasyXIV(values=self.e.ffxiv_values)
        
        self.addStaticIcons()
        self.rebuildCache(
            twitchConfig=self.e.twitch_config, twitterConfig=self.e.twitter_config
        )
