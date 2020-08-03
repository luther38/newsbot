
from dotenv import load_dotenv
from pathlib import Path
from newsbot.collections import Env as envCol
import os

class Env():
    def __init__(self) -> None:
        self.env = envCol()
        
        self.readEnv()
        pass

    def readEnv(self):
        env = Path(".env")
        load_dotenv(dotenv_path=env)
        temp = os.getenv("NEWSBOT_POGO_HOOK")
        pogo_hook = temp.split(' ')
        for i in pogo_hook:
            self.env.pogo_hooks.append(i)
