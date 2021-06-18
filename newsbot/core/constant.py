from enum import Enum

class SourceName(Enum):
    FINALFANTASYXIV = 'finalfantasyxiv'
    PHANTASYSTARONLINE2 = 'phantasystaronline2'
    YOUTUBE = 'youtube'
    POKEMONGO = 'pokemongohub'
    REDDIT = 'reddit'
    RSS = 'rss'
    TWITCH = 'twitch'
    TWITTER = 'twitter'
    INSTAGRAM = 'instagram'
    INVALID = 'invalid'

    @staticmethod
    def fromString(item: str):
        if item == 'finalfantasyxiv': return SourceName.FINALFANTASYXIV
        elif item == 'phantasystaronline2': return SourceName.PHANTASYSTARONLINE2
        elif item == "youtube": return SourceName.YOUTUBE
        elif item == 'pokemongohub': return SourceName.POKEMONGO
        elif item == 'reddit': return SourceName.REDDIT
        elif item == "rss": return SourceName.RSS
        elif item == 'twitch': return SourceName.TWITCH
        elif item == 'twitter': return SourceName.TWITTER
        elif item == 'instagram': return SourceName.INSTAGRAM
        else: return SourceName.INVALID

class SourceType(Enum):
    USER = 'user'
    TAG = 'tag'
    INVALID = ''

    @staticmethod
    def fromString(item: str):
        if item == 'user': return SourceType.USER
        elif item == 'tag': return SourceType.TAG
        else: return SourceType.INVALID