import sys

from newsbot.db import DB, Base, Articles
from newsbot.env import Env
from newsbot.logger import Logger

# Read the env
env = Env().env

# Build the logger
logger = Logger().logger

# Database Connections
database = DB(Base)
