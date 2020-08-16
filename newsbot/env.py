from typing import List
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import RSSArticle
import os


class Env:
    def __init__(self) -> None:
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 30
        self.threadSleepTimer: int = 60 * 30

        self.pogo_enabled: bool = False
        self.pogo_hooks: List[str] = list()

        self.newsbot_pso2_enabled: bool = False
        self.pso2_hooks: List[str] = list()

        self.ffxiv_enabled: bool = False
        self.ffxiv_hooks: List[str] = list()

        self.discordQueue: List[RSSArticle] = list()

        self.readEnv()
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)

        # Pokemon Go Hub
        self.pogo_enabled = bool(os.getenv("NEWSBOT_POGO_ENABLED"))
        try:
            temp: str = os.getenv("NEWSBOT_POGO_HOOK")
            tempList = temp.split(" ")
            for i in tempList:
                self.pogo_hooks.append(i)
        except:
            self.pogo_hooks = list()

        # Phantasy Star Online 2
        self.pso2_enabled = bool(os.getenv("NEWSBOT_PSO2_ENABLED"))
        try:
            temp: str = os.getenv("NEWSBOT_PSO2_HOOK")
            tempList = temp.split(" ")
            for i in tempList:
                self.pso2_hooks.append(i)
        except:
            self.pso2_hooks = list()

        # Final Fantasy XIV
        self.ffxiv_enabled = bool(os.getenv("NEWSBOT_FFXIV_ENABLED"))
        try:
            temp: str = os.getenv("NEWSBOT_FFXIV_HOOK")
            tempList = temp.split(" ")
            for i in tempList:
                self.ffxiv_hooks.append(i)
        except:
            self.ffxiv_hooks = list()

    def getFfxivValues(self) -> List:
        r = {
            'enabled': self.ffxiv_enabled,
            'hooks': self.ffxiv_hooks
        }
        return r

    def getPso2Hooks(self) -> List:
        r = {
            'enabled': self.pso2_enabled,
            'hooks': self.pso2_hooks
        }
        return r
    
    def getPoGoValues(self) -> List:
        return {
            'enabled': self.pogo_enabled,
            'hooks': self.pogo_hooks
        }