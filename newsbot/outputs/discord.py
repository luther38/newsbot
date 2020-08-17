from typing import List

from newsbot import logger, env, database

import re
from time import sleep
from newsbot.tables import DiscordQueue
from newsbot.outputs.outputs import Outputs
from newsbot.collections import RSSArticle, RssArticleLinks
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response


class Discord(Outputs):
    def __init__(self) -> None:
        self.table = DiscordQueue()
        pass

    def enableThread(self) -> None:
        while True:
            # Tell the database to give us the queue on the table.
            queue = self.table.getQueue()

            for i in queue:
                self.sendMessage(i)
                i.remove()
                sleep(env.discord_delay_seconds)

            sleep(env.discord_delay_seconds)

    # def sendMessage(self, article: RSSArticle) -> Response:
    def sendMessage(self, article: DiscordQueue) -> Response:
        webhooks: List[str] = self.getHooks(article.siteName)
        hook: DiscordWebhook = DiscordWebhook(webhooks)
        # hook.username = self.user
        # self.hook.content= 'thing'

        embed: DiscordEmbed = DiscordEmbed()
        embed.title = article.title
        embed.url = article.link

        # convert links
        # for i in article.descriptionLinks:
        #    discordLink: str = f"[{i.text}]({i.href})"
        #    article.description.replace(i.raw, discordLink)

        # TODO track if we have any images in the description and if we need to handle them
        # for i in self.articles.descriptionImages:
        #    pass

        # Discord Embed Description can only contain 2048 characters
        description: str = str(article.description)
        description = self.convertFromHtml(description)
        descriptionCount = len(description)
        if descriptionCount >= 2048:
            description = description[0:2040]
            description = f"{description}..."

        embed.description = description
        embed.set_image(url=article.thumbnail)

        hook.add_embed(embed)

        logger.debug(f"Discord - Sending article '{article.title}'")
        res = hook.execute()
        if res.ok == False:
            logger.critical(
                f"Failed to send to Discord.  Check to ensure the webhook is correct."
            )

        return res

    def getHooks(self, newsSource: str) -> List[str]:
        if newsSource == "Phantasy Star Online 2":
            return env.pso2_hooks
        elif newsSource == "Pokemon Go Hub":
            return env.pogo_hooks
        elif newsSource == "Final Fantasy XIV":
            return env.ffxiv_hooks
        else:
            logger.warning(
                f"got a request to send to {newsSource} and it's a invalid site."
            )

    def convertFromHtml(self, msg: str) -> str:
        msg = msg.replace("<h2>", "**")
        msg = msg.replace("</h2>", "**")
        msg = msg.replace("<h3>", "**")
        msg = msg.replace("</h3>", "**\r\n")
        msg = msg.replace("<strong>", "**")
        msg = msg.replace("</strong>", "**\r\n")
        msg = msg.replace("<ul>", "\r\n")
        msg = msg.replace("</ul>", "")
        msg = msg.replace("</li>", "\r\n")
        msg = msg.replace("<li>", "> ")
        msg = msg.replace("&#8220;", '"')
        msg = msg.replace("&#8221;", '"')
        msg = msg.replace("&#8230;", "...")

        msg = self.replaceLinks(msg)
        return msg

    def replaceLinks(self, msg: str) -> str:
        """
        Find the HTML links and replace them with something discord supports.
        """
        # links = re.findall("(?<=<a )(.*)(?=</a>)", msg)
        links = re.findall("<a(.*?)a>", msg)
        for l in links:
            hrefs = re.findall('href="(.*?)"', l)
            texts = re.findall(">(.*?)</", l)
            discordLink = f"[{texts[0]}]({hrefs[0]})"
            msg = msg.replace(f"<a{l}a>", discordLink)
        return msg
