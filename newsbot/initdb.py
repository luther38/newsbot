from newsbot.env import (
    EnvDiscordDetails,
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
from newsbot.collections import EnvDetails
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
from os import getenv


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

    #    def checkPokemonGoHub(self):
    #        if self.e.pogo_enabled == True:
    #            # Pokemon Go Hub only has one source
    #            Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/rss").add()
    #            if self.e.pogo_icon != "":
    #                Icons(site=f"Custom Pokemon Go Hub", fileName=self.e.pogo_icon).update()
    #            for i in self.e.pogo_hooks:
    #                DiscordWebHooks(name="Pokemon Go Hub", key=i).add()

    #    def checkPhantasyStarOnline2(self):
    #        """
    #        This has been replaced by self.checkSite()
    #        """
    #        if self.e.pso2_values[0] == True:
    #            Sources(
    #                name="Phantasy Star Online 2",
    #                url="https://pso2.com/news"
    #            ).add()
    #            if self.e.pso2_icon != "":
    #                Icons(
    #                    site=f"Custom Phantasy Star Online 2",
    #                    fileName=self.e.pso2_icon
    #                ).update()
    #            for i in self.e.pso2_hooks:
    #                DiscordWebHooks(name="Phantasy Star Online 2", key=i).add()

    def checkFinalFantasyXIV(self):

        if self.e.ffxiv_all == True or self.e.ffxiv_topics == True:
            Sources(
                name="Final Fantasy XIV Topics",
                url="https://na.finalfantasyxiv.com/lodestone/topics/",
            ).add()

        if self.e.ffxiv_all == True or self.e.ffxiv_notices == True:
            Sources(
                name="Final Fantasy XIV Notices",
                url="https://na.finalfantasyxiv.com/lodestone/news/category/1",
            ).add()

        if self.e.ffxiv_all == True or self.e.ffxiv_maintenance == True:
            Sources(
                name="Final Fantasy XIV Maintenance",
                url="https://na.finalfantasyxiv.com/lodestone/news/category/2",
            ).add()

        if self.e.ffxiv_all == True or self.e.ffxiv_updates == True:
            Sources(
                name="Final Fantasy XIV Updates",
                url="https://na.finalfantasyxiv.com/lodestone/news/category/3",
            ).add()

        if self.e.ffxiv_all == True or self.e.ffxiv_status == True:
            Sources(
                name="Final Fantasy XIV Status",
                url="https://na.finalfantasyxiv.com/lodestone/news/category/4",
            ).add()

        for i in self.e.ffxiv_hooks:
            DiscordWebHooks(name="Final Fantasy XIV", key=i).add()
        if self.e.ffxiv_icon != "":
            Icons(site=f"Custom Final Fantasy XIV", fileName=self.e.ffxiv_icon).update()

    def checkSite(self, siteName: str, siteValues: List[EnvDetails]):
        for i in siteValues:
            if siteName == i.name:
                r1 = i.name
            elif siteName == "Reddit":
                r1 = f"{siteName} {i.site}"
            else:
                r1 = f"{siteName} {i.name}"
            Sources(name=r1, url=i.site).add()
            if i.icon != "":
                Icons(site=f"Custom {r1}", fileName=i.icon).update()
            for h in i.hooks:
                DiscordWebHooks(name=r1, key=h).add()

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

    def runDatabaseTasks(self) -> None:
        # Inject new values based off env values
        self.updateDiscordValues(values=self.e.discord_values)
        self.updateRss(values=self.e.rss_values)
        self.updateYoutube(values=self.e.youtube_values)
        self.updateReddit(values=self.e.reddit_values)
        self.updateTwitch(values=self.e.twitch_values)
        self.updateTwitter(values=self.e.twitter_values)
        self.updatePokemonGo(values=self.e.pogo_values)
        self.updatePhantasyStarOnline2(values=self.e.pso2_values)

        # self.checkFinalFantasyXIV()
        # self.checkSite(siteName="Instagram", siteValues=self.e.instagram_values)
        self.addStaticIcons()
        self.rebuildCache(
            twitchConfig=self.e.twitch_config, twitterConfig=self.e.twitter_config
        )
