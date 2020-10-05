from os import system
from newsbot import Env
from typing import List
from newsbot.collections import EnvDetails
from newsbot.tables import Sources, DiscordWebHooks, Icons


class InitDb:
    def __init__(self) -> None:
        # self.runMigrations()
        # self.clearOldRecords()
        # self.runDatabaseTasks()
        self.e = Env()
        self.e.readEnv()
        pass

    def runMigrations(self) -> None:
        system("alembic upgrade head")

    def clearOldRecords(self) -> None:
        # clear our the table cache from last startup
        Sources().clearTable()
        DiscordWebHooks().clearTable()

    def checkPokemonGoHub(self):
        if self.e.pogo_enabled == True:
            # Pokemon Go Hub only has one source
            Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/rss").add()
            # Sources(name="Pokemon Go Hub", url="https://pokemongohub.net/post/category/news/").add()
            for i in self.e.pogo_hooks:
                DiscordWebHooks(name="Pokemon Go Hub", key=i).add()

    def checkPhantasyStarOnline2(self):
        if self.e.pso2_enabled == True:
            Sources(name="Phantasy Star Online 2", url="https://pso2.com/news").add()
            for i in self.e.pso2_hooks:
                DiscordWebHooks(name="Phantasy Star Online 2", key=i).add()

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

    def checkReddit(self):
        for i in self.e.reddit_values:
            r1 = f"Reddit {i.site}"
            Sources(name=r1, url=f"https://reddit.com/r/{i.site}").add()
            for h in i.hooks:
                DiscordWebHooks(name=r1, key=h).add()

    def checkSite(self, siteName: str, siteValues: List[EnvDetails]):
        for i in siteValues:
            r1 = f"{siteName} {i.name}"
            Sources(name=r1, url=i.site).add()
            for h in i.hooks:
                DiscordWebHooks(name=r1, key=h).add()

    def addStaticIcons(self) -> None:
        Icons().clearTable()
        Icons(site="Default Pokemon Go Hub", fileName="https://pokemongohub.net/wp-content/uploads/2017/04/144.png").add()
        Icons(site="Default Phantasy Star Online 2", fileName="https://raw.githubusercontent.com/jtom38/newsbot/master/mounts/icons/pso2.jpg").add()
        Icons(site="Default Final Fantasy XIV", fileName="https://img.finalfantasyxiv.com/lds/h/0/U2uGfVX4GdZgU1jASO0m9h_xLg.png").add()
        Icons(site="Default Reddit", fileName="https://www.redditstatic.com/desktop2x/img/favicon/android-icon-192x192.png").add()
        Icons(site="Default YouTube", fileName="https://www.youtube.com/s/desktop/c46c1860/img/favicon_144.png").add()
        Icons(site="Default Twitter", fileName="https://abs.twimg.com/responsive-web/client-web/icon-ios.8ea219d5.png").add()
        Icons(site="Default Instagram", fileName="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png").add()

    def runDatabaseTasks(self) -> None:
        # Inject new values based off env values
        # if the user did not request a source, we will ignore it.
        self.checkPokemonGoHub()
        self.checkPhantasyStarOnline2()
        self.checkFinalFantasyXIV()
        self.checkReddit()
        self.checkSite(siteName="YouTube", siteValues=self.e.youtube_values)
        self.checkSite(siteName="Instagram", siteValues=self.e.instagram_values)
        self.checkSite(siteName="Twitter", siteValues=self.e.twitter_values)
        self.addStaticIcons()
