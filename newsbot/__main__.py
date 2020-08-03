import newsbot
from newsbot.sources.pokemongohub import RSSPogohub
from newsbot.collections import RSSRoot
from newsbot.outputs.discord import Discord
from newsbot.db import Articles
from time import sleep
from threading import Thread




pogo = RSSPogohub()
pogoNews: RSSRoot = pogo.getArticles()

print(f"got news")
for i in pogoNews.articles:
    d = Discord(i)
    d.sendMessage()
    sleep(30)
