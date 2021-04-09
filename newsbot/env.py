from typing import List
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import RSSArticle
import os

class EnvDetails:
    def __init__(
        self,
        site: str = "",
        name: str = "",
        hooks: List[str] = list(),
        options: str = "",
        icon: str = "",
    ) -> None:
        self.enabled: bool = False
        self.site: str = site
        self.name: str = name
        self.hooks: List[str] = hooks
        self.options: str = options
        self.icon: str = icon

class EnvDiscordDetails():
    def __init__(self, name: str = '', server: str = '', channel: str = '', url: str = '') -> None:
        self.name: str = name
        self.server: str = server
        self.channel: str = channel
        self.url: str = url
        pass

class EnvDiscord():
    def __init__(self) -> None:
        self.links: List[EnvDiscordDetails] = list()
        pass

    def read(self) -> List[EnvDiscordDetails]:
        env = Path(".env")
        load_dotenv(dotenv_path=env)
        i = 0
        while i <= 9:
            edd = EnvDiscordDetails(
                name=os.getenv(f"NEWSBOT_DISCORD_{i}_NAME")
                ,server=os.getenv(f"NEWSBOT_DISCORD_{i}_SERVER")
                ,channel=os.getenv(f"NEWSBOT_DISCORD_{i}_CHANNEL")
                ,url=os.getenv(f"NEWSBOT_DISCORD_{i}_URL")
            )
            i = i +1
            if edd.url != None:
                self.links.append(edd)

        return self.links

class EnvRssDetails():
    def __init__(self, name: str = "", url: str = "", discordLinkName: str = '') -> None:
        self.name: str = name
        self.url: str = url
        self.discordLinkName: str = discordLinkName
        pass

class EnvRss():
    def __init__(self) -> None:
        load_dotenv(dotenv_path=Path(".env"))
        self.links: List[EnvRssDetails] = list()
        pass

    def read(self) -> List[EnvRssDetails]:
        i = 0
        while i <= 9:
            erd = EnvRssDetails(
                name=os.getenv(f"NEWSBOT_RSS_{i}_NAME")
                ,url=os.getenv(f"NEWSBOT_RSS_{i}_URL")
                ,discordLinkName=os.getenv(f"NEWSBOT_RSS_{i}_LINK_DISCORD")
            )
            i = i + 1
            if erd.name != None:
                self.links.append(erd)
        return self.links

class Env:
    def __init__(self) -> None:
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 15
        self.threadSleepTimer: int = 60 * 30

        #self.pogo_values: List[EnvDetails] = list()
        #self.pogo_enabled: bool = False
        #self.pogo_hooks: List[str] = list()

        #self.pso2_values: List[EnvDetails] = list()
        # self.newsbot_pso2_enabled: bool = False
        # self.pso2_hooks: List[str] = list()

        #self.ffxiv_values: List[EnvDetails] = list()
        #self.ffxiv_all: bool = False
        #self.ffxiv_hooks: List[str] = list()

        #self.reddit_values: List[EnvDetails] = list()
        #self.youtube_values: List[EnvDetails] = list()
        #self.instagram_values: List[EnvDetails] = list()
        # self.instagram_user_values: List[EnvDetails] = list()
        # self.instagram_tag_values: List[EnvDetails] = list()
        #self.twitter_values: List[EnvDetails] = list()
        #self.twitch_values: List[EnvDetails] = list()
        self.rss_values: List[EnvRssDetails] = EnvRss().read()
        self.discord_values: List[EnvDiscordDetails] = EnvDiscord().read()

        # self.readEnv()
        print('l')
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)

        # Pokemon Go Hub
        self.pogo_values.clear()
        if self.readBoolEnv("NEWSBOT_POGO_ENABLED") == True:
            self.pogo_values.append(
                EnvDetails(
                    name="Pokemon Go Hub",
                    site="https://pokemongohub.net/rss",
                    hooks=self.extractHooks("NEWSBOT_POGO_HOOK"),
                    icon=self.getCustomIcon("NEWSBOT_POGO_ICON"),
                )
            )

        # Phantasy Star Online 2
        self.pso2_values.clear()
        if self.readBoolEnv("NEWSBOT_PSO2_ENABLED") == True:
            self.pso2_values.append(
                EnvDetails(
                    name="Phantasy Star Online 2",
                    site="https://pso2.com/news",
                    hooks=self.extractHooks("NEWSBOT_PSO2_HOOK"),
                    icon=self.getCustomIcon("NEWSBOT_PSO2_ICON"),
                )
            )

        # Final Fantasy XIV
        self.ffxiv_values.append(EnvDetails())
        self.readFfxivValues()
        # self.readRedditValues()
        self.reddit_values.clear()
        self.reddit_values = self.readValues(
            site="NEWSBOT_REDDIT_SUB",
            hooks="NEWSBOT_REDDIT_HOOK",
            icon="NEWSBOT_REDDIT_ICON",
        )
        # self.readYoutubeValues()
        self.youtube_values.clear()
        self.youtube_values = self.readValues(
            site="NEWSBOT_YOUTUBE_URL",
            hooks="NEWSBOT_YOUTUBE_HOOK",
            icon="NEWSBOT_YOUTUBE_ICON",
            name="NEWSBOT_YOUTUBE_NAME",
        )
        # self.readInstagramValues()
        self.instagram_values.clear()
        for igu in self.readValues(
            site="NEWSBOT_INSTAGRAM_USER_NAME",
            hooks="NEWSBOT_INSTAGRAM_USER_HOOK",
            icon="NEWSBOT_INSTAGRAM_USER_ICON",
            type="user",
        ):
            self.instagram_values.append(igu)

        for igt in self.readValues(
            site="NEWSBOT_INSTAGRAM_TAG_NAME",
            hooks="NEWSBOT_INSTAGRAM_TAG_HOOK",
            icon="NEWSBOT_INSTAGRAM_TAG_ICON",
            type="tag",
        ):
            self.instagram_values.append(igt)

        t = "NEWSBOT_TWITTER"
        self.twitter_values.clear()
        for tu in self.readValues(
            site=f"{t}_USER_NAME",
            hooks=f"{t}_USER_HOOK",
            icon=f"{t}_USER_ICON",
            type="user",
        ):
            self.twitter_values.append(tu)

        for tt in self.readValues(
            site=f"{t}_TAG_NAME",
            hooks=f"{t}_TAG_HOOK",
            icon=f"{t}_TAG_ICON",
            type="tag",
        ):
            self.twitter_values.append(tt)

        # self.readTwitterValues()
        t = "NEWSBOT_TWITCH"
        self.twitch_values.clear()
        self.twitch_values = self.readValues(
            site=f"{t}_USER_NAME", hooks=f"{t}_HOOK", icon=f"{t}_ICON", type="user"
        )
        # self.readTwitchValues()
        t = "NEWSBOT_RSS"
        self.rss_values.clear()
        self.rss_values = self.readValues(
            site=f"{t}_LINK", hooks=f"{t}_HOOK", icon=f"{t}_ICON", name=f"{t}_NAME"
        )
        # self.readRssValues()

    def readFfxivValues(self) -> None:
        self.ffxiv_all = self.readBoolEnv("NEWSBOT_FFXIV_ALL")
        self.ffxiv_topics = self.readBoolEnv("NEWSBOT_FFXIV_TOPICS")
        self.ffxiv_notices = self.readBoolEnv("NEWSBOT_FFXIV_NOTICES")
        self.ffxiv_maintenance = self.readBoolEnv("NEWSBOT_FFXIV_MAINTENANCE")
        self.ffxiv_updates = self.readBoolEnv("NEWSBOT_FFXIV_UPDATES")
        self.ffxiv_status = self.readBoolEnv("NEWSBOT_FFXIV_STATUS")
        self.ffxiv_hooks = self.extractHooks("NEWSBOT_FFXIV_HOOK")
        self.ffxiv_icon = self.getCustomIcon("NEWSBOT_FFXIV_ICON")

    def readValues(
        self, site: str, hooks: str, icon: str, name: str = "", type: str = ""
    ) -> List[EnvDetails]:
        counter = 0
        items: List[EnvDetails] = list()
        while counter <= 10:
            s = os.getenv(f"{site}_{counter}")
            h = self.extractHooks(f"{hooks}_{counter}")
            i = self.getCustomIcon(f"{icon}_{counter}")
            if s != None or len(h) >= 1:
                e = EnvDetails(site=s, hooks=h, icon=i)
                e.enabled = True

                # check if we need to pull the name.
                # Not all sources use a name
                if name != "":
                    n = os.getenv(f"{name}_{counter}")
                    e.name = n

                # Check if we have a source that collects either user or tag objects
                if type != "":
                    e.name = f"{type} {s}"

                items.append(e)
            counter = counter + 1
        return items

    def readRedditValues(self) -> List[EnvDetails]:
        counter = 0
        self.reddit_values.clear()

        while counter <= 10:
            site = os.getenv(f"NEWSBOT_REDDIT_SUB_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_REDDIT_HOOK_{counter}")
            icon = self.getCustomIcon(f"NEWSBOT_REDDIT_ICON_{counter}")
            if site != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = site
                details.hooks = hooks
                details.icon = icon
                self.reddit_values.append(details)
            counter = counter + 1

    def readYoutubeValues(self) -> None:
        counter = 0
        self.youtube_values.clear()

        while counter <= 10:
            site = os.getenv(f"NEWSBOT_YOUTUBE_URL_{counter}")
            name = os.getenv(f"NEWSBOT_YOUTUBE_NAME_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_YOUTUBE_HOOK_{counter}")
            icon = self.getCustomIcon(f"NEWSBOT_YOUTUBE_ICON_{counter}")

            if site != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = site
                details.hooks = hooks
                details.name = name
                details.icon = icon
                self.youtube_values.append(details)
                # items.append(details)

            counter = counter + 1

        # self.youtube_values = items

    def readInstagramValues(self) -> None:
        counter = 0
        self.instagram_values.clear()
        base = "NEWSBOT_INSTAGRAM"
        while counter <= 10:
            # User Posts
            types: List["str"] = ("USER", "TAG")
            for t in types:
                #tbase = f"{base}_{t}"
                site = os.getenv(f"{base}_USER_NAME_{counter}")
                hooks = self.extractHooks(f"{base}_USER_HOOK_{counter}")
                icon = self.getCustomIcon(f"{base}_USER_ICON_{counter}")
                if site != None or len(hooks) >= 1:
                    details = EnvDetails()
                    details.enabled = True
                    details.site = site
                    details.hooks = hooks
                    details.name = f"{t.lower()} {site}"
                    details.icon = icon
                    self.instagram_values.append(details)

            counter = counter + 1

    def readTwitterValues(self) -> None:
        counter = 0
        self.twitter_values.clear()
        base = "NEWSBOT_TWITTER"
        while counter <= 10:
            # User Posts
            types: List["str"] = ("USER", "TAG")
            for t in types:
                tbase = f"{base}_{t}"
                site = os.getenv(f"{tbase}_NAME_{counter}")
                hooks = self.extractHooks(f"{base}_USER_HOOK_{counter}")
                icon = self.getCustomIcon(f"{base}_USER_ICON_{counter}")

                if site != None or len(hooks) >= 1:
                    details = EnvDetails()
                    details.enabled = True
                    details.site = site
                    details.hooks = hooks
                    details.name = f"{t.lower()} {site}"
                    details.icon = icon
                    self.twitter_values.append(details)

            counter = counter + 1

    def readTwitchValues(self) -> None:
        counter = 0
        self.twitch_values.clear()

        while counter <= 10:
            site = os.getenv(f"NEWSBOT_TWITCH_USER_NAME_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_TWITCH_HOOK_{counter}")
            icon = self.getCustomIcon(f"NEWSBOT_TWITCH_ICON_{counter}")
            if site != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = site
                details.hooks = hooks
                details.name = f"user {site}"
                details.icon = icon
                self.twitch_values.append(details)

            counter = counter + 1

    def readRssValues(self) -> None:
        counter = 0
        self.rss_values.clear()

        while counter <= 10:
            name = os.getenv(f"NEWSBOT_RSS_NAME_{counter}")
            link = os.getenv(f"NEWSBOT_RSS_LINK_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_RSS_HOOK_{counter}")
            icon = self.getCustomIcon(f"NEWSBOT_RSS_ICON_{counter}")
            if link != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = link
                details.hooks = hooks
                details.name = name
                details.icon = icon
                self.rss_values.append(details)
            counter = counter + 1

    def extractHooks(self, sourceHooks) -> List[str]:
        try:
            t: str = os.getenv(sourceHooks)
            if t != None:
                tList = t.split(" ")
                array = list()
                for i in tList:
                    array.append(i)
                return array
            else:
                return list()

        except Exception as e:
            print(f"Failed to extract Webhook details from {sourceHooks}. {e}")
            return list()

    def readBoolEnv(self, env: str) -> bool:
        res = os.getenv(env)
        if res == None:
            return False

        if res.lower() == "true":
            return True
        elif res.lower() == "false":
            return False
        else:
            return False

    def getCustomIcon(self, env: str) -> str:
        res = os.getenv(env)
        if res == None:
            return ""
        else:
            return res

    def getPso2Values(self) -> List:
        r = {"enabled": self.pso2_enabled, "hooks": self.pso2_hooks}
        return r

    def getPoGoValues(self) -> List:
        return {"enabled": self.pogo_enabled, "hooks": self.pogo_hooks}
