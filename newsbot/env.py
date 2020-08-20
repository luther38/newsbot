

from typing import List
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import RSSArticle
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

        # Pokemon Go Hub
        self.pogo_enabled = bool(os.getenv("NEWSBOT_POGO_ENABLED"))
        self.pogo_hooks= self.extractHooks("NEWSBOT_POGO_HOOK")

        # Phantasy Star Online 2
        self.pso2_enabled = bool(os.getenv("NEWSBOT_PSO2_ENABLED"))
        self.pso2_hooks = self.extractHooks("NEWSBOT_PSO2_HOOK")

        # Final Fantasy XIV
        self.readFfxivValues()
        self.readRedditValues()

    def readFfxivValues(self) -> None:
        self.ffxiv_all = bool(os.getenv("NEWSBOT_FFXIV_ALL"))
        self.ffxiv_topics = bool(os.getenv("NEWSBOT_FFXIV_TOPICS"))
        self.ffxiv_notices = bool(os.getenv("NEWSBOT_FFXIV_NOTICES"))
        self.ffxiv_maintenance = bool(os.getenv("NEWSBOT_FFXIV_MAINTENANCE"))
        self.ffxiv_updates = bool(os.getenv("NEWSBOT_FFXIV_UPDATES"))
        self.ffxiv_status = bool(os.getenv("NEWSBOT_FFXIV_STATUS"))

        self.ffxiv_hooks = self.extractHooks("NEWSBOT_FFXIV_HOOK")

    def readRedditValues(self) -> None:
        self.redditSub01 = os.getenv("NEWSBOT_REDDIT_SUB01")
        self.redditHook01 = self.extractHooks("NEWSBOT_REDDIT_HOOK01")

    def extractHooks(self, sourceHooks) -> List[str]:
        try:
            t: str = os.getenv(sourceHooks)
            tList = t.split(" ")
            array = list()
            for i in tList:
                array.append(i)
            return array
        except Exception as e:
            print(f"Failed to extract Webhook details from {sourceHooks}. {e}")
            return list()

    def getPso2Values(self) -> List:
        r = {"enabled": self.pso2_enabled, "hooks": self.pso2_hooks}
        return r

    def getPoGoValues(self) -> List:
        return {"enabled": self.pogo_enabled, "hooks": self.pogo_hooks}
