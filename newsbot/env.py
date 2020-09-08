from typing import List
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import RSSArticle, EnvDetails
import os


class Env:
    def __init__(self) -> None:
        # self.newDatabase: bool = False
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 15
        self.threadSleepTimer: int = 60 * 30

        self.pogo_enabled: bool = False
        self.pogo_hooks: List[str] = list()

        self.newsbot_pso2_enabled: bool = False
        self.pso2_hooks: List[str] = list()

        self.ffxiv_all: bool = False
        self.ffxiv_hooks: List[str] = list()

        self.readEnv()
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)

        # self.db_name = os.getenv("NEWSBOT_DATABASE_NAME")

        # Pokemon Go Hub
        self.pogo_enabled = self.readBoolEnv("NEWSBOT_POGO_ENABLED")
        self.pogo_hooks = self.extractHooks("NEWSBOT_POGO_HOOK")

        # Phantasy Star Online 2
        self.pso2_enabled = self.readBoolEnv("NEWSBOT_PSO2_ENABLED")
        self.pso2_hooks = self.extractHooks("NEWSBOT_PSO2_HOOK")

        # Final Fantasy XIV
        self.readFfxivValues()
        self.readRedditValues()

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
        items = list()

        while counter <= 10:
            sub = os.getenv(f"NEWSBOT_REDDIT_SUB_{counter}")
            hooks = self.extractHooks(f"NEWSBOT_REDDIT_HOOK_{counter}")

            if sub != None or len(hooks) >= 1:
                details = EnvDetails()
                details.enabled = True
                details.site = sub
                details.hooks = hooks
                items.append(details)

            counter = counter + 1

        self.reddit_values = items

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
