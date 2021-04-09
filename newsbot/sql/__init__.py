

#from .iTables import ITables
#from .exceptions import (
#    FailedToAddRecord
#    ,FailedToAddToDatabase
#)
#from .articles import Articles
#from .discordQueue import DiscordQueue
#from .discordWebHooks import DiscordWebHooks
#from .icons import Icons
#from .logs import Logs
#from .settings import Settings
#from .sourceLinks import SourceLinks
#from .sources import Sources
from .db import DB, Base

database = DB(Base)
