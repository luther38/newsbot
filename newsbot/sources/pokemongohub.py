from typing import List
from newsbot import logger, env
#from newsbot.collections import RSSRoot, RSSArticle
from newsbot.sources.rssreader import RSSReader, UnableToFindContent, UnableToParseContent
from newsbot.tables import Articles, Sources, DiscordWebHooks
import re
from requests import get, Request
from bs4 import BeautifulSoup

class PogohubReader(RSSReader):
    def __init__(self) -> None:
        self.rootUrl = "https://pokemongohub.net/rss"
        self.siteName: str = "Pokemon Go Hub"
        self.links = list()
        self.hooks = list()

        self.sourceEnabled: bool = False
        self.outputDiscord: bool = False

        self.checkEnv()
        pass

    def checkEnv(self):
        # Check if Pokemon Go was requested
        self.isSourceEnabled()
        self.checkDiscordOutput()

    def isSourceEnabled(self) -> bool:
        res = Sources(name="Pokemon Go Hub").findAllByName()
        if len(res) >= 1:
            self.links.append(res[0])
            self.sourceEnabled = True
            return self.sourceEnabled

        return self.sourceEnabled

    def checkDiscordOutput(self) -> None:
        dwh = DiscordWebHooks(name="Pokemon Go Hub").findAllByName()
        if len(dwh) >= 1:
            self.outputDiscord = True
            for i in dwh:
                self.hooks.append(i)

    def getArticles(self) -> List[Articles]:
        for site in self.links:
            logger.debug(f"{site.name} - Checking for updates.")
            self.uri = site.url

            siteContent: Request = self.getContent()
            bs: BeautifulSoup = self.getParser()

            allArticles: List[Articles] = list()
            try:
                mainLoop = bs.contents[1].contents[1].contents

                for i in mainLoop:
                    if i.name == "item":
                        item: Articles = self.processItem(i)

                        # we are doing the check here to see if we need to fetch the thumbnail.
                        # if we have seen the link already, move on and save on time.
                        seenAlready = item.exists()
                        if seenAlready == False:
                            # get thumbnail
                            item.thumbnail = self.getArticleThumbnail(item.url)
                            allArticles.append(item)

                logger.debug(f"Pokemon Go Hub - Finished checking.")
            except Exception as e:
                logger.error(f"Failed to parse articles from Pokemon Go Hub.  Chances are we have a malformed responce. {e}")
            
        return allArticles

    def getContent(self) -> Request:
        try:
            return get(self.uri, headers=self.headers)
        except Exception as e:
            logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def getParser(self, siteContent: Request) -> BeautifulSoup:
        try:
            return BeautifulSoup(siteContent.content, features="html.parser")
        except Exception as e:
            logger.critical(f"failed to parse data returned from requests. {e}")

    def processItem(self, item: object) -> Articles:
        a = Articles()
        a.siteName = "Pokemon Go Hub"

        for i in item.contents:
            if i.name == "title":
                a.title = i.next
            elif i.name == "link":
                a.url = self.removeHTMLTags(i.next)
            elif i.name == "pubdate":
                a.pubDate = i.next
            elif i.name == "category":
                a.tags = i.next
            elif i.name == "description":
                a.description = self.removeHTMLTags(i.next)
            elif i.name == "content:encoded":
                a.content = i.next
        return a

    def removeHTMLTags(self, text: str) -> str:
        tags = ("<p>", "</p>", "<img >", "<h2>")
        text = text.replace("\n", "")
        text = text.replace("\t", "")
        text = text.replace("<p>", "")
        text = text.replace("</p>", "\r\n")
        text = text.replace("&#8217;", "'")
        spans = re.finditer("(?<=<span )(.*)(?=>)", text)
        try:
            if len(spans) >= 1:
                print("money")
        except:
            pass

        return text

    def getArticleThumbnail(self, link: str) -> str:
        try:
            r = get(link)
            bs: BeautifulSoup = BeautifulSoup(r.content, features="html.parser")
            res = bs.find_all("img", class_="entry-thumb")
            return res[0].attrs["src"]
        except Exception as e:
            logger.error(f"Failed to pull Pokemon Go Hub thumbnail or {link}. {e}")
