from typing import List
from newsbot.logger import Logger
from requests import get, Response
from bs4 import BeautifulSoup


class SiteContent:
    """
    This object contains information returned from BeautifulSoup.
    It acts as a buffer layer incase any changes to the API
    """

    attrs: dict = {}
    source: str = ""

    def __init__(self) -> None:
        pass


class RequestContent:
    """
    This is a common class that will request site information.
    This class will make use of the Requests and BeautifulSoup librarys.

    Examples:
    RequestContent(url='www').
    RequestContent().setUrl("www").
    """

    def __init__(self, url: str = "") -> None:
        self.url = url
        self.logger = Logger(__class__)
        pass

    def setUrl(self, url: str) -> None:
        """
        If you want to parse a URL, set the value here.
        """
        self.url = url

    def setSoup(self, soup: BeautifulSoup) -> None:
        """
        If the source has already been parsed elsewhere, pass the BeautifulSoup object here.
        """
        self.soup = soup

    def __getHeaders__(self) -> dict:
        return {"User-Agent": "NewsBot - Automated News Delivery"}

    def __getSource__(self) -> str:
        try:
            res: Response = get(self.url, headers=self.__getHeaders__())
            if res.ok == True:
                self.__response__: Response = res
                return res.text
            else:
                self.logger.error(
                    f"Attempted to get data from '{self.url}' but did not get any data.  StatusCode={res.status_code}"
                )
                return ""
        except Exception as e:
            self.logger.critical(
                f"Failed to get data from '{self.url}' but resulted in an error. {e} "
            )

    def __getSoup__(self) -> BeautifulSoup:
        try:
            soup = BeautifulSoup(self.__source__, features="html.parser")
            return soup
        except Exception as e:
            self.logger.error(e)
            return BeautifulSoup()

    def getPageDetails(self) -> None:
        """
        This pulls the source code and converts it into a BeautifulSoup object.
        """
        if self.url == "":
            self.logger.error(
                "Was requested to pull data from a site, but no URL was passed."
            )
        else:
            self.__source__ = self.__getSource__()

        try:
            if self.__soup__.text == "":
                self.__soup__ = self.__getSoup__()
            else:
                pass
        except:
            self.__soup__ = self.__getSoup__()

        pass

    def findSingle(
        self, name: str = "", attrKey: str = "", attrValue: str = ""
    ) -> BeautifulSoup:
        if attrKey != "":
            attrs = {attrKey: attrValue}
            res = self.__soup__.find(name=name, attrs=attrs)
            return res
        else:
            return self.__soup__.find(name=name)

    def findMany(
        self, name: str = "", attrKey: str = "", attrValue: str = ""
    ) -> List[BeautifulSoup]:
        if attrKey != "":
            return self.__soup__.find_all(name=name, attrs={attrKey: attrValue})
        else:
            return self.__soup__.find_all(name=name)

    def findFeedLink(self) -> dict:
        atom = self.findSingle(
            name="link", attrKey="type", attrValue="application/atom+xml"
        )
        rss = self.findSingle(
            name="link", attrKey="type", attrValue="application/rss+xml"
        )
        json = self.findSingle(
            name="link", attrKey="type", attrValue="application/json"
        )

        if atom != None:
            return self.__buildFeedDict__("atom", atom.attrs["href"])
        elif rss != None:
            return self.__buildFeedDict__("rss", rss.attrs["href"])
        elif json != None:
            return self.__buildFeedDict__("json", json.attrs["href"])
        else:
            return self.__buildFeedDict__("none", None)

    def __buildFeedDict__(self, type: str, content: str) -> dict:
        return {"type": type, "content": content}

    def findSiteIcon(self, siteUrl: str) -> str:
        """
        This will go and attempt to extract the 'apple-touch-icon' from the header.

        return: str
        """
        # if a site url contains the / lets remove it
        if siteUrl.endswith("/") == True:
            siteUrl = siteUrl.strip("/")

        bestSize: int = -1
        icons = self.findMany(name="link", attrKey="rel", attrValue="apple-touch-icon")
        # look though all the icons given, find the largest one.
        for icon in icons:
            size: int = int(icon.attrs["sizes"].split("x")[0])
            if size > bestSize:
                bestSize = size

        # take what we found as the largest icon and store it.
        for icon in icons:
            size: int = int(icon.attrs["sizes"].split("x")[0])
            if size == bestSize:
                href = icon.attrs["href"]
                if "http" in href or "https" in href:
                    return href
                else:
                    return f"{siteUrl}{href}"
        return ""

    def findArticleThumbnail(self) -> str:
        """
        This is best used on articles, not on root the main site page.
        It will go and check the page for defined thumbnails and return the first one it finds, if any.

        return: str
        """
        meta = (
            {"name": "meta", "attrKey": "property", "attrValue": "og:image"},
            {"name": "meta", "attrKey": "name", "attrValue": "twitter:image:src"},
        )

        for i in meta:
            try:
                item = self.findSingle(
                    name=i["name"], attrKey=i["attrKey"], attrValue=i["attrValue"]
                )
                if item.attrs["content"] != "":
                    thumb = item.attrs["content"]
                    return thumb
            except:
                pass
        return ""

    def findArticleDescription(self) -> str:
        lookups = (
            {"name": "div", "key": "class", "value": "entry-content e-content"},
            {"name": "div", "key": "class", "value": "engadget-post-contents"},
            {"name": "div", "key": "class", "value": "article-content post-page"},
        )

        for l in lookups:
            content = self.findSingle(
                name=l["name"], attrKey=l["key"], attrValue=l["value"]
            )
            if content.text != "":
                return content.text


class RequestSiteContent(RequestContent):
    def findFeedLink(self, siteUrl: str) -> dict:
        atom = self.findSingle(
            name="link", attrKey="type", attrValue="application/atom+xml"
        )
        rss = self.findSingle(
            name="link", attrKey="type", attrValue="application/rss+xml"
        )
        json = self.findSingle(
            name="link", attrKey="type", attrValue="application/json"
        )

        if atom != None:
            href = self.__cleanUrl__(atom.attrs["href"], siteUrl)
            return self.__buildFeedDict__("atom", href)
        elif rss != None:
            href = self.__cleanUrl__(rss.attrs["href"], siteUrl)
            return self.__buildFeedDict__("rss", href)
        elif json != None:
            href = self.__cleanUrl__(json.attrs["href"], siteUrl)
            return self.__buildFeedDict__("json", href)
        else:
            return self.__buildFeedDict__("none", None)

    def __cleanUrl__(self, href: str, siteUrl: str) -> str:
        if href.startswith("//") == True:
            href = href.replace("//", "")
        if "http://" in href or "https://" in href:
            return href
        elif "http://" in siteUrl:
            return f"http://{href}"
        elif "https://" in siteUrl:
            return f"https://{href}"

    def __buildFeedDict__(self, type: str, content: str) -> dict:
        return {"type": type, "content": content}

    def findSiteIcon(self, siteUrl: str) -> str:
        """
        This will go and attempt to extract the 'apple-touch-icon' from the header.

        return: str
        """
        # if a site url contains the / lets remove it
        if siteUrl.endswith("/") == True:
            siteUrl = siteUrl.strip("/")

        bestSize: int = -1
        href = ""
        icons = self.findMany(name="link", attrKey="rel", attrValue="apple-touch-icon")
        if len(icons) >= 2:
            try:
                # look though all the icons given, find the largest one.
                for icon in icons:
                    try:
                        size: int = int(icon.attrs["sizes"].split("x")[0])
                        if size > bestSize:
                            bestSize = size
                    except:
                        self.logger.warning(
                            f"'{siteUrl}' did not have sizes present on the site icon."
                        )
                        pass

                # take what we found as the largest icon and store it.
                for icon in icons:
                    size: int = int(icon.attrs["sizes"].split("x")[0])
                    if size == bestSize:
                        href = icon.attrs["href"]
            except Exception as e:
                self.logger.warning(f"Failed to find the size of the siteIcon. {e}")
        elif len(icons) == 1:
            href = icons[0].attrs["href"]
        else:
            href = ""

        if "http" in href or "https" in href:
            return href
        elif href == "":
            return href
        else:
            return f"{siteUrl}{href}"


class RequestArticleContent(RequestContent):
    def findArticleThumbnail(self) -> str:
        """
        This is best used on articles, not on root the main site page.
        It will go and check the page for defined thumbnails and return the first one it finds, if any.

        return: str
        """
        meta = (
            {"name": "meta", "attrKey": "property", "attrValue": "og:image"},
            {"name": "meta", "attrKey": "name", "attrValue": "twitter:image:src"},
        )

        for i in meta:
            try:
                item = self.findSingle(
                    name=i["name"], attrKey=i["attrKey"], attrValue=i["attrValue"]
                )
                if item.attrs["content"] != "":
                    thumb = item.attrs["content"]
                    return thumb
            except:
                pass
        return ""

    def findArticleDescription(self) -> str:
        lookups = (
            {
                "name": "div",
                "key": "class",
                "value": "entry-content e-content",
            },  # HowToGeek
            {
                "name": "div",
                "key": "class",
                "value": "engadget-post-contents",
            },  # Engadget
            {
                "name": "div",
                "key": "class",
                "value": "article-content post-page",
            },  # ArsTechnica
        )

        for l in lookups:
            try:
                content = self.findSingle(
                    name=l["name"], attrKey=l["key"], attrValue=l["value"]
                )
                if content.text != "":
                    text = ""
                    # Look for just p blocks to avoid ads and junk we dont care about
                    pBlocks = self.findMany(name="p")
                    if len(pBlocks) >= 1:
                        for p in pBlocks:
                            text += f"{p} \r\n"
                    return content.text
            except:
                pass
        return ""
