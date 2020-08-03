
import logging
import sys

from newsbot.db import DB, Base, Articles
from newsbot.env import Env
from newsbot.logger import Logger

# Read the env
env = Env().env

# Build the logger
logger = Logger().logger
logger.info("NewsBot has started.")

# Database Connections
database = DB(Base)
