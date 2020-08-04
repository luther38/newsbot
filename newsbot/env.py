from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import Env as envCol
import os


class Env:
    def __init__(self) -> None:
        self.env = envCol()

        self.readEnv()
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)

        # Global
        self.interval_seconds: int = 30 * 60
        self.discord_delay_seconds: int = 60

        # Pokemon Go Hub
        try:
            temp = os.getenv("NEWSBOT_POGO_HOOK")
            pogo_hook = temp.split(" ")
            for i in pogo_hook:
                self.env.pogo_hooks.append(i)
        except:
            self.env.pogo_hooks = list()

        # Phantasy Star Online 2
        try:
            temp = os.getenv("NEWSBOT_PSO2_HOOK")
            temp = temp.split(" ")
            for i in pogo_hook:
                self.env.pso2_hooks.append(i)
        except:
            self.env.pso2_hooks = list()
