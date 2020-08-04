import newsbot
from newsbot.collections import RSSRoot, RSSArticle
from newsbot.sources.rssreader import RSSReader
from newsbot.db import Articles

import requests
from bs4 import BeautifulSoup


class RSSPogohub(RSSReader):
    def __init__(self) -> None:
        self.logger = newsbot.logger
        self.rootUrl = "https://pokemongohub.net/rss"
        pass

    def getParser(self) -> BeautifulSoup:
        try:
            r = requests.get(self.rootUrl)
        except Exception as e:
            print(f"Failed to collect data from '{self.rootUrl}'. Error:{e}")

        try:
            bs = BeautifulSoup(r.content, features="html.parser")
            return bs
        except Exception as e:
            print(f"Failed to parse data returned from requests. Error:{e}")

    def getArticles(self) -> RSSRoot:
        rss = RSSRoot()
        rss.link = self.removeHTMLTags(self.rootUrl)

        bs = self.getParser()
        mainLoop = bs.contents[1].contents[1].contents

        for i in mainLoop:
            if i == "\n":
                continue
            elif i.name == "title":
                rss.title = self.removeHTMLTags(i.next)
            elif i.name == "item":
                item: RSSArticle = self.processItem(i)

                exists = self.exists(item)
                if exists == False:
                    #self.add(item)

                    # get thumbnail
                    item.thumbnail = self.getArticleThumbnail(item.link)

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
    
                    self.logger.debug(f"Pokemon Go Hub - {item.title}")
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
                a.tags.append(i.next)
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

    def exists(self, item: RSSArticle) -> bool:
        session = newsbot.database.newSession()
        result = Articles()
        try:
            for res in session.query(Articles).filter(Articles.title == item.title):
                result = res
        except Exception as e:
            print(e)

        session.close()

        if result.title == item.title:
            return True
        else:
            return False

    def add(self, item: RSSArticle) -> None:
        session = newsbot.database.newSession()
        a = Articles()
        a.title = item.title
        a.url = item.link
        a.pubDate = item.pubDate
        try:
            session.add(a)
            session.commit()
        except Exception as e:
            print(f"Failed to add record to the DB. {e}")
