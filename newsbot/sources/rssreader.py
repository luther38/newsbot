from typing import List
import requests
from bs4 import BeautifulSoup
import re
from newsbot.collections import RssArticleImages, RSSArticle, RssArticleLinks
from newsbot.html import Html


class RSSReader:
    def __init__(self, rootUrl: str = "") -> None:
        self.rootUrl = rootUrl
        pass

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

    def getLinks(self, description: str) -> List[RssArticleLinks]:
        links = list()
        h = Html()
        # res = h.getByElement("a ", 'a', description)
        res = re.findall("<a(.*?)a>", description)
        for r in res:
            a = RssArticleLinks()
            a.raw = f"<a{r}a>"

            href = re.findall('href="(.*?)"', r)
            # href = h.getByAttribute('href', r)
            a.href = href[0]

            text = re.findall(">(.*?)</", r)
            # text = h.getByElement('>', '</', r)
            a.text = text[0]

            links.append(a)
        return links

    def removeLinks(self, text: str) -> str:
        res = re.findall("(?<=<a )(.*)(?=</a>)", text)
        for i in res:
            text = text.replace(i, "")

        text = text.replace("<a </a>", "")
        return text

    def getImages(self, text: str) -> List[RssArticleImages]:
        images = list()
        # Select all the images in the context with regex
        # res = re.findall("(?<=<img )(.*)(?=>)", text)
        res = re.findall("<img(.*?)>", text)
        for r in res:
            image = RssArticleImages()
            image.raw = f"<img{r}>"
            src = re.findall('src="(.*?)"', r)
            image.src = src[0]

            try:
                title = re.findall('title="(.*?)"', r)
                image.title = title[0]
            except:
                # print("failed to find title on img.")
                pass

            try:
                alt = re.findall('alt="(.*?)"', r)
                image.alt = alt[0]
            except:
                pass

            try:
                height = re.findall('height="(.*?)"', r)
                image.height = height[0]
            except:
                pass

            try:
                width = re.findall('width="(.*?)"', r)
                image.width = width[0]
            except:
                pass

            images.append(image)

        return images

    def removeImageLinks(self, text: str) -> str:
        res = re.findall("(?<=<img )(.*)(?=>)", text)
        for i in res:
            text = text.replace(i, "")

        text = text.replace("<img >", "")
        return text

    def getArticleContent(self) -> None:
        raise NotImplementedError

    def getParser(self) -> BeautifulSoup:
        raise NotImplementedError

    def getArticles(self) -> None:
        raise NotImplementedError

    def processItem(self, parameter_list) -> RSSArticle:
        raise NotImplementedError
