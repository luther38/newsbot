
from newsbot.startup import Startup
from os import system

system("alembic upgrade head")

s = Startup()
s.startProgram()