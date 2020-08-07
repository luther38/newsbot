from typing import List
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import RSSArticle
import os


class Env:
    def __init__(self) -> None:
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 60
        self.threadSleepTimer: int = 60 * 30

        self.pogo_hooks: List[str] = list()
        self.pso2_hooks: List[str] = list()

        self.discordQueue: List[RSSArticle] = list()

        self.readEnv()
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)

        # Pokemon Go Hub
        try:
            temp: str = os.getenv("NEWSBOT_POGO_HOOK")
            tempList = temp.split(" ")
            for i in tempList:
                self.pogo_hooks.append(i)
        except:
            self.pogo_hooks = list()

        # Phantasy Star Online 2
        try:
            temp: str = os.getenv("NEWSBOT_PSO2_HOOK")
            tempList = temp.split(" ")
            for i in tempList:
                self.pso2_hooks.append(i)
        except:
            self.pso2_hooks = list()
