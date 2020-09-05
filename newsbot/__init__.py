import sys
from newsbot.db import DB, Base
from newsbot.env import Env
from newsbot.logger import Logger

# Build the logger
logger = Logger().logger

# Read the env
env = Env()

# Database Connections
database = DB(Base)
