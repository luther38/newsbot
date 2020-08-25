from newsbot import logger, env
from newsbot.collections import RSSRoot, RSSArticle
from newsbot.sources.rssreader import RSSReader
from newsbot.tables import Articles, Sources, DiscordWebHooks

import requests
from bs4 import BeautifulSoup

class PogohubReader(RSSReader):
    def __init__(self) -> None:
        self.rootUrl = "https://pokemongohub.net/rss"
        self.siteName: str = "Pokemon Go Hub"
        self.links = list()
        self.hooks = list()

        self.checkEnv()
        pass

    def checkEnv(self):
        # Check if Pokemon Go was requested
        res = Sources(name="Pokemon Go Hub").findAllByName()
        if len(res) >= 1:
            self.links.append(res[0])

            dwh = DiscordWebHooks(name="Pokemon Go Hub").findAllByName()
            for i in dwh:
                self.hooks.append(i)

    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.removeHTMLTags(self.rootUrl)

        for site in self.links:
            logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url

            bs = self.getParser()
            mainLoop = bs.contents[1].contents[1].contents

            for i in mainLoop:
                if i == "\n":
                    continue
                elif i.name == "title":
                    rss.title = self.removeHTMLTags(i.next)
                elif i.name == "item":
                    item: RSSArticle = self.processItem(i)
                    item.siteName = "Pokemon Go Hub"
                    # self.add(item)

                    # get thumbnail
                    # item.thumbnail = self.getArticleThumbnail(item.link)

                    images = self.getImages(item.content)
                    for i in images:
                        item.contentImages.append(i)
                    # item.content = self.removeImageLinks(item.content)
                    links = self.getLinks(item.content)
                    for i in links:
                        item.contentLinks.append(i)

                    images = list()
                    images = self.getImages(item.description)
                    for i in images:
                        item.descriptionImages.append(i)

                    links = list()
                    links = self.getLinks(item.description)
                    for i in links:
                        item.descriptionLinks.append(i)

                    rss.articles.append(item)

            logger.debug(f"Pokemon Go Hub - Finished checking.")
        return rss

    def processItem(self, item: object) -> RSSArticle:
        a = RSSArticle()

        for i in item.contents:
            if i == "\n":
                continue
            elif i.name == "title":
                a.title = i.next
            elif i.name == "link":
                a.link = self.removeHTMLTags(i.next)
            elif i.name == "pubdate":
                a.pubDate = i.next
            elif i.name == "category":
                a.tags = i.next
            elif i.name == "description":
                a.description = self.removeHTMLTags(i.next)
            elif i.name == "content:encoded":
                a.content = i.next
        return a

    def getArticleThumbnail(self, link: str) -> str:
        r = requests.get(link)
        bs: BeautifulSoup = BeautifulSoup(r.content, features="html.parser")
        res = bs.find_all("img", class_="entry-thumb")
        return res[0].attrs["src"]
