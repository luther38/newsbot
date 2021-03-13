from typing import List
from sqlalchemy.sql.expression import false

from sqlalchemy.sql.selectable import FromClause
from newsbot.tables import Sources, DiscordWebHooks

class BSources():
    """
    This class contains some common code found in the sources.  Do not use this on its own!
    """
    def __init__(self) -> None:
        pass

    def getSource(self, siteName: str) -> List[Sources]:
        l = list()
        res = Sources(name=siteName).findAllByName()
        for i in res:
            l.append(i)
        return l

    def isSourceEnabled(self, siteName: str) -> bool:
        res = Sources(name=siteName).findAllByName()
        if len(res) >= 1:
            return True
        else:
            return False

    def isDiscordOutputEnabled(self, siteName: str) -> List[DiscordWebHooks]:
        h = list()
        dwh = DiscordWebHooks(name=siteName).findAllByName()
        if len(dwh) >= 1:
            for i in dwh:
                h.append(i)
        return h

    def getDiscordEnabled(self, siteName: str) -> bool:
        dwh = DiscordWebHooks(name=siteName).findAllByName()
        if len(dwh) >= 1:
            return True 
        else:
            return False
        
    