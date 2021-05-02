from posix import environ
from typing import List
from dotenv import load_dotenv
from pathlib import Path
import os

class EnvDiscordDetails:
    def __init__(
        self, name: str = "", server: str = "", channel: str = "", url: str = ""
    ) -> None:
        self.name: str = name
        self.server: str = server
        self.channel: str = channel
        self.url: str = url       

class EnvRssDetails:
    """
    This class is a collection object that holds values, nothing more.
    """
    def __init__(
        self, name: str = "", url: str = "", discordLinkName: List[str] = ""
    ) -> None:
        self.name: str = name
        self.url: str = url
        self.discordLinkName: List[str] = discordLinkName

class EnvYoutubeDetails:
    """
    This class is a collection object that holds values, nothing more.
    """
    def __init__(
        self, name: str = "", url: str = "", discordLinkName: List[str] = ""
    ) -> None:
        self.name: str = name
        self.url: url = url
        self.discordLinkName: List[str] = discordLinkName

class EnvRedditDetails:
    def __init__(self, subreddit: str = "", discordLinkName: List[str] = "") -> None:
        self.subreddit: str = subreddit
        self.discordLinkName: List[str] = discordLinkName

class EnvTwitchConfig:
    def __init__(
        self,
        clientId: str = "",
        clientSecret: str = "",
        monitorClips: bool = False,
        monitorLiveStreams: bool = False,
        monitorVod: bool = False,
    ) -> None:
        self.clientId: str = clientId
        self.clientSecret: str = clientSecret
        self.monitorClips: bool = monitorClips
        self.monitorLiveStreams: bool = monitorLiveStreams
        self.monitorVod: bool = monitorVod
        pass

class EnvTwitchDetails:
    def __init__(self, user: str = "", discordLinkName: List[str] = "") -> None:
        self.user: str = user
        self.discordLinkName: List[str] = discordLinkName
        pass

class EnvTwitterConfig:
    """
    This is a collection object.  
    To get access to this, call Env().twitter_config
    """
    def __init__(
        self,
        apiKey: str = "",
        apiKeySecret: str = "",
        preferedLang: str = "",
        ignoreRetweet: bool = False,
    ) -> None:
        self.apiKey: str = apiKey
        self.apiKeySecret: str = apiKeySecret
        self.preferedLang: str = str(preferedLang)
        self.ignoreRetweet: bool = ignoreRetweet
        pass

class EnvTwitterDetails:
    def __init__(
        self, name: str = "", type: str = "", discordLinkName: List[str] = ""
    ) -> None:
        self.name: str = name
        self.type: str = type
        self.discordLinkName: List[str] = discordLinkName
        pass

class EnvInstagramDetails:
    def __init__(
        self, name: str = "", type: str = "", discordLinkName: List[str] = ""
    ) -> None:
        self.name: str = name
        self.type: str = type
        self.discordLinkName: List[str] = discordLinkName
        pass

class EnvPokemonGoDetails:
    def __init__(
        self, enabled: bool = False, discordLinkName: List[str] = list()
    ) -> None:
        self.enabled: bool = enabled
        self.discordLinkName: List[str] = discordLinkName
        pass

class EnvPhantasyStarOnline2Details:
    def __init__(
        self, enabled: bool = False, discordLinkName: List[str] = list()
    ) -> None:
        self.enabled: bool = enabled
        self.discordLinkName: List[str] = discordLinkName
        pass

class EnvFinalFantasyXIVDetails:
    def __init__(
        self,
        #allEnabled: bool = False,
        topicsEnabled: bool = False,
        noticesEnabled: bool = False,
        maintenanceEnabled: bool = False,
        updateEnabled: bool = False,
        statusEnabled: bool = False,
        discordLinkName: List[str] = list(),
    ) -> None:
        #self.allEnabled: bool = allEnabled
        self.topicsEnabled: bool = topicsEnabled
        self.noticesEnabled: bool = noticesEnabled
        self.maintenanceEnabled: bool = maintenanceEnabled
        self.updateEnabled: bool = updateEnabled
        self.statusEnabled: bool = statusEnabled
        self.discordLinkName: List[str] = discordLinkName
        pass

class EnvReader:
    def __init__(self) -> None:
        load_dotenv(dotenv_path=Path(".env"))
        pass

    def readDiscord(self) -> List[EnvDiscordDetails]:
        links: List[EnvDiscordDetails] = list()
        i = 0
        while i <= 9:
            edd = EnvDiscordDetails(
                name=os.getenv(f"NEWSBOT_DISCORD_{i}_NAME"),
                server=os.getenv(f"NEWSBOT_DISCORD_{i}_SERVER"),
                channel=os.getenv(f"NEWSBOT_DISCORD_{i}_CHANNEL"),
                url=os.getenv(f"NEWSBOT_DISCORD_{i}_URL"),
            )
            i = i + 1
            if edd.url != None:
                links.append(edd)
        return links

    def __splitDiscordLinks__(self, raw: str) -> List[str]:
        res = list()
        if raw == "" or raw == None:
            return list()
        else:
            for i in raw.split(","):
                i = i.lstrip()
                i = i.rstrip()
                res.append(i)
        return res

    def readRss(self) -> List[EnvRssDetails]:
        links: List[EnvRssDetails] = list()
        i = 0
        while i <= 9:
            erd = EnvRssDetails(
                name=os.getenv(f"NEWSBOT_RSS_{i}_NAME"),
                url=os.getenv(f"NEWSBOT_RSS_{i}_URL"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_RSS_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if erd.name != None:
                links.append(erd)
        return links

    def readYoutube(self) -> List[EnvYoutubeDetails]:
        links: List[EnvYoutubeDetails] = list()
        i = 0
        while i <= 9:
            eytd = EnvYoutubeDetails(
                name=os.getenv(f"NEWSBOT_YOUTUBE_{i}_NAME"),
                url=os.getenv(f"NEWSBOT_YOUTUBE_{i}_URL"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_YOUTUBE_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if eytd.name != None:
                links.append(eytd)
        return links

    def readReddit(self) -> List[EnvRedditDetails]:
        links: List[EnvRedditDetails] = list()
        i = 0
        while i <= 9:
            item = EnvRedditDetails(
                subreddit=os.getenv(f"NEWSBOT_REDDIT_{i}_SUBREDDIT"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_REDDIT_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.subreddit != None:
                links.append(item)
        return links

    def readTwitchConfig(self) -> EnvTwitchConfig:
        item = EnvTwitchConfig(
            clientId=os.getenv("NEWSBOT_TWITCH_CLIENT_ID"),
            clientSecret=os.getenv("NEWSBOT_TWITCH_CLIENT_SECRET"),
            monitorClips=self.__parseBool__("NEWSBOT_TWITCH_MONITOR_CLIPS"),
            monitorLiveStreams=self.__parseBool__("NEWSBOT_TWITCH_MONITOR_LIVE_STREAMS"),
            monitorVod=self.__parseBool__("NEWSBOT_TWITCH_MONITOR_VOD"),
        )
        return item

    def readTwitch(self) -> List[EnvTwitchDetails]:
        links: List[EnvTwitchDetails] = list()
        i = 0
        while i <= 9:
            item = EnvTwitchDetails(
                user=os.getenv(f"NEWSBOT_TWITCH_{i}_USER"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_TWITCH_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.user != None:
                links.append(item)
        return links

    def readTwitter(self) -> List[EnvTwitterDetails]:
        links: List[EnvTwitterDetails] = list()
        i = 0
        while i <= 9:
            item = EnvTwitterDetails(
                name=os.getenv(f"NEWSBOT_TWITTER_{i}_NAME"),
                type=os.getenv(f"NEWSBOT_TWITTER_{i}_TYPE"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_TWITTER_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.name != None:
                links.append(item)
        return links

    def readTwitterConfig(self) -> EnvTwitterConfig:
        item = EnvTwitterConfig(
            apiKey=os.getenv(f"NEWSBOT_TWITTER_API_KEY"),
            apiKeySecret=os.getenv(f"NEWSBOT_TWITTER_API_KEY_SECRET"),
            preferedLang=os.getenv(f"NEWSBOT_TWITTER_PERFERED_LANG"),
            ignoreRetweet=self.__parseBool__(f"NEWSBOT_TWITTER_IGNORE_RETWEET")
        )
        return item

    def readInstagram(self) -> List[EnvInstagramDetails]:
        links: List[EnvInstagramDetails] = list()
        i = 0
        while i <= 9:
            item = EnvInstagramDetails(
                name=os.getenv(f"NEWSBOT_INSTAGRAM_{i}_NAME"),
                type=os.getenv(f"NEWSBOT_INSTAGRAM_{i}_TYPE"),
                discordLinkName=self.__splitDiscordLinks__(
                    os.getenv(f"NEWSBOT_INSTAGRAM_{i}_LINK_DISCORD")
                ),
            )
            i = i + 1
            if item.name != None:
                links.append(item)
        return links

    def readPogo(self) -> EnvPokemonGoDetails:
        item = EnvPokemonGoDetails(
            enabled=self.__parseBool__(f"NEWSBOT_POGO_ENABLED"),
            discordLinkName=self.__splitDiscordLinks__(
                os.getenv(f"NEWSBOT_POGO_LINK_DISCORD")
            ),
        )
        return item

    def readPhantasyStarOnline2(self) -> EnvPhantasyStarOnline2Details:
        return EnvPhantasyStarOnline2Details(
            enabled=self.__parseBool__(f"NEWSBOT_PSO2_ENABLED"),
            discordLinkName=self.__splitDiscordLinks__(
                os.getenv(f"NEWSBOT_PSO2_LINK_DISCORD")
            ),
        )

    def readFinalFantasyXIV(self) -> EnvFinalFantasyXIVDetails:
        return EnvFinalFantasyXIVDetails(
            #allEnabled=self.__parseBool__("NEWSBOT_FFXIV_ALL"),
            topicsEnabled=self.__parseBool__(f"NEWSBOT_FFXIV_TOPICS"),
            noticesEnabled=self.__parseBool__(f"NEWSBOT_FFXIV_NOTICES"),
            maintenanceEnabled=self.__parseBool__(f"NEWSBOT_FFXIV_MAINTENANCE"),
            updateEnabled=self.__parseBool__(f"NEWSBOT_FFXIV_UPDATES"),
            statusEnabled=self.__parseBool__(f"NEWSBOT_FFXIV_STATUS"),
            discordLinkName=self.__splitDiscordLinks__(
                os.getenv(f"NEWSBOT_FFXIV_LINK_DISCORD")
            ),
        )

    def __parseBool__(self, envFlag: str) -> bool:
        value:str = os.getenv(envFlag).lower()
        if value == 'false':
            return False
        elif value == 'true':
            return True
        else:
            raise Exception(f"Unknown value type for '{envFlag}'.  Expected True or False.")


class Env:
    def __init__(self) -> None:
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 15
        self.threadSleepTimer: int = 60 * 30

        reader = EnvReader()
        self.pogo_values: EnvPokemonGoDetails = reader.readPogo()
        self.pso2_values: EnvPhantasyStarOnline2Details = reader.readPhantasyStarOnline2()
        self.ffxiv_values: EnvFinalFantasyXIVDetails = reader.readFinalFantasyXIV()
        self.reddit_values: List[EnvRedditDetails] = reader.readReddit()
        self.youtube_values: List[EnvYoutubeDetails] = reader.readYoutube()
        self.instagram_values: List[EnvInstagramDetails] = reader.readInstagram()
        self.twitter_values: List[EnvTwitterDetails] = reader.readTwitter()
        self.twitter_config: EnvTwitterConfig = reader.readTwitterConfig()

        self.twitch_values: List[EnvTwitchDetails] = reader.readTwitch()
        self.twitch_config: EnvTwitchConfig = reader.readTwitchConfig()

        self.rss_values: List[EnvRssDetails] = reader.readRss()

        self.discord_values: List[EnvDiscordDetails] = reader.readDiscord()
