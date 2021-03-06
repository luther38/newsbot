from typing import List


class RSSRoot:
    def __init__(self) -> None:
        raise NotImplementedError()
        self.title: str = ""
        self.link: str = ""
        self.articles: List[RSSArticle] = list()


class RSSArticle:
    def __init__(self) -> None:
        raise NotImplementedError()
        self.siteName: str = ""
        self.tags: str = ""
        self.title: str = ""
        self.thumbnail: str = ""
        self.link: str = ""
        self.pubDate: str = ""
        self.description: str = ""
        self.descriptionImages: List[RssArticleImages] = list()
        self.descriptionLinks: List[RssArticleLinks] = list()
        self.content: str = ""
        self.contentImages: List[RssArticleImages] = list()
        self.contentLinks: List[RssArticleLinks] = list()
        # self.tags: List[str] = list()


class RssArticleImages:
    def __init__(self) -> None:
        raise NotImplementedError()
        self.raw: str = ""
        self.src: str = ""
        self.title: str = ""
        self.alt: str = ""
        self.width: int = 0
        self.height: int = 0


class RssArticleLinks:
    def __init__(self) -> None:
        raise NotImplementedError()
        self.raw: str = ""
        self.href: str = ""
        self.text: str = ""
        pass


class Env:
    def __init__(self) -> None:
        raise NotImplementedError()
        self.interval_seconds: int = 60 * 30
        self.discord_delay_seconds: int = 60
        self.pogo_hooks: List[str] = list()
        self.pso2_hooks: List[str] = list()


class EnvDetails:
    def __init__(
        self,
        site: str = "",
        name: str = "",
        hooks: List[str] = list(),
        options: str = "",
        icon: str = "",
    ) -> None:
        raise NotImplementedError()
        self.enabled: bool = False
        self.site: str = site
        self.name: str = name
        self.hooks: List[str] = hooks
        self.options: str = options
        self.icon: str = icon
