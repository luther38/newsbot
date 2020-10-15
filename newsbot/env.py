from typing import List
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import RSSArticle, EnvDetails
import os


class Env():
    def __init__(self) -> None:
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 15
        self.threadSleepTimer: int = 60 * 30

        self.pogo_enabled: bool = False
        self.pogo_hooks: List[str] = list()

        self.newsbot_pso2_enabled: bool = False
        self.pso2_hooks: List[str] = list()

        self.ffxiv_all: bool = False
        self.ffxiv_hooks: List[str] = list()

        self.reddit_values: List[EnvDetails] = list()
        self.youtube_values: List[EnvDetails] = list()
        self.instagram_values: List[EnvDetails] = list()
        self.twitter_values: List[EnvDetails] = list()
        self.twitch_values: List[EnvDetails] = list()

        self.readEnv()
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)

        # Pokemon Go Hub
        self.pogo_enabled = self.readBoolEnv("NEWSBOT_POGO_ENABLED")
        self.pogo_hooks = self.extractHooks("NEWSBOT_POGO_HOOK")

        # Phantasy Star Online 2
        self.pso2_enabled = self.readBoolEnv("NEWSBOT_PSO2_ENABLED")
        self.pso2_hooks = self.extractHooks("NEWSBOT_PSO2_HOOK")

        # Final Fantasy XIV
        self.readFfxivValues()
        self.readRedditValues()
        self.readYoutubeValues()
        self.readInstagramValues()
        self.readTwitterValues()
        self.readTwitchValues()

    def readFfxivValues(self) -> None:
        self.ffxiv_all = self.readBoolEnv("NEWSBOT_FFXIV_ALL")
        self.ffxiv_topics = self.readBoolEnv("NEWSBOT_FFXIV_TOPICS")
        self.ffxiv_notices = self.readBoolEnv("NEWSBOT_FFXIV_NOTICES")
        self.ffxiv_maintenance = self.readBoolEnv("NEWSBOT_FFXIV_MAINTENANCE")
        self.ffxiv_updates = self.readBoolEnv("NEWSBOT_FFXIV_UPDATES")
        self.ffxiv_status = self.readBoolEnv("NEWSBOT_FFXIV_STATUS")

        self.ffxiv_hooks = self.extractHooks("NEWSBOT_FFXIV_HOOK")

    def readRedditValues(self) -> List[EnvDetails]:
        counter = 0
        self.reddit_values.clear()

        while counter <= 10:
            sub = os.getenv(f"NEWSBOT_REDDIT_SUB_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_REDDIT_HOOK_{counter}")

            if sub != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = sub
                details.hooks = hooks
                self.reddit_values.append(details)

            counter = counter + 1

        # self.reddit_values = items

    def readYoutubeValues(self) -> None:
        counter = 0
        self.youtube_values.clear()

        while counter <= 10:
            sub = os.getenv(f"NEWSBOT_YOUTUBE_URL_{counter}")
            name = os.getenv(f"NEWSBOT_YOUTUBE_NAME_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_YOUTUBE_HOOK_{counter}")

            if sub != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = sub
                details.hooks = hooks
                details.name = name
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
            sub = os.getenv(f"{base}_USER_NAME_{counter}")
            hooks = self.extractHooks(f"{base}_USER_HOOK_{counter}")

            if sub != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = sub
                details.hooks = hooks
                details.name = f"user {sub}"
                self.instagram_values.append(details)

            # Tags Posts
            tag = os.getenv(f"{base}_TAG_NAME_{counter}")
            hooks = self.extractHooks(f"{base}_TAG_HOOK_{counter}")

            if tag != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = tag
                details.hooks = hooks
                details.name = f"tag {tag}"
                self.instagram_values.append(details)

            counter = counter + 1

    def readTwitterValues(self) -> None:
        counter = 0
        self.twitter_values.clear()
        base = "NEWSBOT_TWITTER"
        while counter <= 10:
            # User Posts
            sub = os.getenv(f"{base}_USER_NAME_{counter}")
            hooks = self.extractHooks(f"{base}_USER_HOOK_{counter}")

            if sub != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = sub
                details.hooks = hooks
                details.name = f"user {sub}"
                self.twitter_values.append(details)

            # Tags Posts
            tag = os.getenv(f"{base}_TAG_NAME_{counter}")
            hooks = self.extractHooks(f"{base}_TAG_HOOK_{counter}")

            if tag != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = tag
                details.hooks = hooks
                details.name = f"tag {tag}"
                self.twitter_values.append(details)

            counter = counter + 1

    def readTwitchValues(self) -> None:
        counter = 0
        self.twitch_values.clear()

        while counter <= 10:
            name = os.getenv(f"NEWSBOT_TWITCH_USER_NAME_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_TWITCH_HOOK_{counter}")

            if name != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = name
                details.hooks = hooks
                details.name = f"user {name}"
                self.twitch_values.append(details)

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

    def getPso2Values(self) -> List:
        r = {"enabled": self.pso2_enabled, "hooks": self.pso2_hooks}
        return r

    def getPoGoValues(self) -> List:
        return {"enabled": self.pogo_enabled, "hooks": self.pogo_hooks}
