from newsbot.startup import Startup
from newsbot import env
from os import system
from pathlib import Path

env.newDatabase: bool = True
dbPath = Path("./mounts/database/newsbot.db")
if dbPath.exists:
    env.newDatabase = False

system("alembic upgrade head")

s = Startup()
s.startProgram()
