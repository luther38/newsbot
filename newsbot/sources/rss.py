from typing import List, Dict
from newsbot import env
from newsbot.logger import Logger
from newsbot.sources.common import BSources, ISources, UnableToFindContent, UnableToParseContent
from newsbot.sources.rssHelper import *
from newsbot.common.requestContent import (
    RequestContent,
    RequestArticleContent,
    RequestSiteContent,
)
from newsbot.sql.tables import Articles, Sources, DiscordWebHooks, Icons
from newsbot.cache import Cache
from requests import get, Response
import re
from bs4 import BeautifulSoup
from json import loads


class RssReader(ISources, BSources):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri = "https://example.net/"
        self.siteName: str = "RSS"
        self.feedName: str = ""
        self.RssHelper: IRssContent = IRssContent()
        self.links: List[Sources] = list()
        self.hooks: List[DiscordWebHooks] = list()
        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False
        self.checkEnv(self.siteName)
        pass
   
    def getArticles(self) -> List[Articles]:
        allArticles: List[Articles] = list()
        for l in self.links:
            l: Sources = l

            # Check if this source was disabled in the previous run
            if l.enabled == False:
                continue

            self.logger.debug(f"{l.name} - Checking for updates")
            self.feedName = l.name.split(" ")[1]

            # Cache the root site
            self.uri = l.url
            rsc = RequestSiteContent(url=l.url)
            rsc.getPageDetails()

            # Check if the site icon has been cached
            iconsExists = Icons(site=l.name).findAllByName()
            if len(iconsExists) == 0:
                siteIcon: str = rsc.findSiteIcon(l.url)
                Icons(site=l.name, fileName=siteIcon).update()

            # Check if we have helper code for deeper RSS integration
            # hasHelper: bool = self.enableHelper(l.url)

            # Determin what typ of feed is on the site
            feed = rsc.findFeedLink(siteUrl=l.url)
            if feed["type"] == "atom":
                ap = AtomParser(url=feed["content"], siteName=l.name)
                items = ap.getPosts()
                for i in items:
                    a: Articles = ap.parseItem(i)
                    if a.title != "":
                        allArticles.append(a)

            elif feed["type"] == "rss":
                rp = RssParser(url=feed["content"], siteName=l.name)
                items = rp.getPosts()
                for item in items:
                    a = rp.processItem(item=item, title=l.name)
                    if a.title != "":
                        allArticles.append(a)

            elif feed["type"] == "json":
                jp = JsonParser(url=feed["content"], siteName=l.name)
                items = jp.getPosts()
                for i in items:
                    a: Articles = jp.parseItem(i)
                    if a.title != "":
                        allArticles.append(a)

            else:
                # Unable to find a feed in the page's source code.
                # Asumining that it is RSS
                rp = RssParser(url=l.url, siteName=l.name)
                items = rp.getPosts()
                if len(items) >= 1:
                    for item in items:
                        a = rp.processItem(item=item, title=l.name)
                        if a.title != "":
                            allArticles.append(a)
                else:
                    self.logger.error(
                        f"Unable to find a feed for '{l.name}'.  This source is getting disabled."
                    )
                    for link in self.links:
                        link: Sources = link
                        if link.name == l.name:
                            link.enabled = False

        return allArticles

    def enableHelper(self, url: str) -> bool:
        r: bool = False
        if "engadget.com" in url:
            self.RssHelper = Engadget()
            r = True
        elif "arstechnica" in url:
            self.RssHelper = ArsTechnica()
            r = True
        elif "howtogeek" in url:
            self.RssHelper = HowToGeek()
            r = True
        return r


class IParser:
    def checkSiteIcon(self) -> None:
        raise NotImplementedError()

    def getPosts(self) -> List:
        raise NotImplementedError()

    def findFeedTitle(self) -> str:
        raise NotImplementedError()

    def findItemLink(self) -> str:
        raise NotImplementedError()


class AtomParser(IParser):
    def __init__(self, url: str, siteName: str) -> None:
        self.url: str = url
        self.siteName: str = siteName
        self.content = RequestSiteContent(url=url)
        self.content.getPageDetails()
        pass

    def findFeedTitle(self) -> str:
        title = self.content.findSingle(name="title")
        return title

    def getPosts(self) -> List:
        return self.content.findMany(name="entry")

    def parseItem(self, item: BeautifulSoup) -> Articles:
        feedTitle: str = self.content.findSingle(name="title")

        a = Articles()
        a.url = item.find(name="link", attrs={"type": "text/html"}).attrs["href"]
        if a.exists() == False:
            rc = RequestContent(url=a.url)
            rc.getPageDetails()
            thumbnail = rc.findArticleThumbnail()

            a.siteName = self.siteName
            a.tags = f"RSS, {self.siteName}"
            a.title = item.find(name="title").text.replace("\n", "").strip()
            a.pubDate = item.find(name="updated").text
            text: str = item.find(name="content").text
            a.thumbnail = thumbnail

            # this works on github commits
            if ">" in text and "<" in text:
                text = re.findall(">(.*?)<", text)[0]
            a.description = text

            author = item.find(name="author")
            if "github.com" in self.url:
                a.authorName = author.find(name="name").text
            else:
                a.authorName = author.text

        return a


class RssParser:
    def __init__(self, url: str, siteName: str) -> None:
        self.logger = Logger(__class__)
        self.url: str = url
        self.siteName: str = siteName
        self.content: RequestSiteContent = RequestContent(url=url)
        self.content.getPageDetails()
        # self.rssHelper: IRssContent = rssHelper
        pass

    def getPosts(self) -> List:
        return self.content.findMany(name="item")

    def processItem(self, item: BeautifulSoup, title: str) -> Articles:
        # get the link for the article
        url = self.findItemLink(item)
        if url == "" or url == None or url == "https://":

            # did not find a valid url, pass back a blank object
            return Articles()

        # Check if we have already looked atthis link
        if Articles(url=url).exists() == False:
            # Set the new URI and store the source for now to avoid extra calls
            # rc = RequestContent(url=url)
            ra = RequestArticleContent(url=url)
            ra.getPageDetails()
            thumb = ra.findArticleThumbnail()

            description = ""
            # description = ra.findArticleDescription()

            a = Articles(
                siteName=title,
                title=item.find(name="title").text,
                description=self.findItemDescription(item, description),
                tags=self.findItemTags(item),
                url=url,
                pubDate=item.find(name="pubdate").text,
                authorName=self.findItemAuthor(item),
            )
            a.thumbnail = thumb
        else:
            return Articles()
        return a

    def findItemDescription(self, item: BeautifulSoup, desc: str) -> str:
        i: str = ""
        if desc != "":
            return desc
        else:
            items = ("description", "content:encoded")
            for i in items:
                try:
                    # i:str = item.find(name="description").text
                    i = item.find(name=i).text
                    if i != "":
                        return i
                except:
                    pass

            if i == "":
                self.logger.critical(
                    f"Failed to locate RSS body.  Review {self.url} for the reason"
                )
            return ""

    def findItemLink(self, item: BeautifulSoup) -> str:
        url: str = item.find(name="link").next
        url = url.replace("\n", "")
        url = url.replace("\t", "")
        url = url.replace("\r", "")
        url = url.strip()
        return url

    def findItemTags(self, item: BeautifulSoup) -> str:
        tags: List[str] = list()
        for i in item.find_all(name="category"):
            # lets vsc see the expected class
            i: BeautifulSoup = i
            tags.append(i.text)

        s = str(tags)
        return s

    def findItemAuthor(self, item: BeautifulSoup) -> str:
        items = ("author", "dc:creator")
        for i in items:
            try:
                itemAuthor = item.find(name=i).text
                if itemAuthor != "":
                    return itemAuthor
            except:
                pass

        return ""


class JsonParser:
    def __init__(self, url: str, siteName: str):
        self.url: str = url
        self.siteName: str = siteName
        self.rc = RequestArticleContent(url=url)
        self.rc.getPageDetails()
        self.json = loads(self.rc.__source__)

    def getPosts(self) -> List:
        return self.json["items"]

    def parseItem(self, item: Dict) -> Articles:
        a = Articles(url=item["url"])
        if a.exists() == False:
            rc = RequestContent(url=item["url"])
            rc.getPageDetails()
            a = Articles(
                siteName=self.siteName,
                tags=f"RSS, {self.siteName}",
                title=item["title"],
                url=item["url"],
                pubDate=item["date_published"],
                thumbnail=rc.findArticleThumbnail(),
                authorName=item["author"]["name"],
                description=item["content_html"],
            )
        return a
