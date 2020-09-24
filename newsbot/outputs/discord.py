from typing import List
from newsbot import logger, env
import re
from time import sleep
from newsbot.tables import DiscordQueue, DiscordWebHooks
from newsbot.outputs.ioutputs import IOutputs
from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response


class Discord(IOutputs):
    def __init__(self) -> None:
        self.table = DiscordQueue()
        self.tempMessage: DiscordWebhook = DiscordWebhook("placeholder")
        pass

    def enableThread(self) -> None:
        while True:
            # Tell the database to give us the queue on the table.
            try:
                queue = self.table.getQueue()

                for i in queue:
                    self.sendMessage(i)
                    i.remove()
                    sleep(env.discord_delay_seconds)
            except Exception as e:
                logger.error(f"Failed to post a message. {i.title}")

            sleep(env.discord_delay_seconds)

    def buildMessage(self, article: DiscordQueue) -> None:
        # reset the stored message
        self.tempMessage = DiscordWebhook("placeholder")

        # Extract the webhooks that relate to this site
        webhooks: List[str] = self.getHooks(article.siteName)

        # Make a new webhook with the hooks that relate to this site
        hook: DiscordWebhook = DiscordWebhook(webhooks)

        title = article.title
        if len(title) >= 128:
            title = f"{title[0:128]}..."

        # Make a new Embed object
        embed: DiscordEmbed = DiscordEmbed(title=title, url=article.link)
        # embed.title = article.title
        # embed.url = article.link

        # Discord Embed Description can only contain 2048 characters
        if article.description != "":
            description: str = str(article.description)
            description = self.convertFromHtml(description)
            descriptionCount = len(description)
            if descriptionCount >= 2048:
                description = description[0:2040]
                description = f"{description}..."
            embed.description = description

        # Figure out if we have video based content
        if article.video != "":
            embed.description = "View the video online!"
            embed.set_video(
                url=article.video, height=article.videoHeight, width=article.videoWidth
            )

        if article.thumbnail != "":
            embed.set_image(url=article.thumbnail)

        # Build our footer message
        footer = self.buildFooter(article.siteName)
        embed.set_footer(text=footer)

        embed.set_color(color=self.getEmbedColor(article.siteName))

        hook.add_embed(embed)
        self.tempMessage = hook

    def sendMessage(self, article: DiscordQueue) -> Response:
        logger.debug(f"Discord - Sending article '{article.title}'")
        self.buildMessage(article)
        try:
            res = self.tempMessage.execute()
        except Exception as e:
            logger.critical(
                f"Failed to send to Discord.  Check to ensure the webhook is correct. Error: {e}"
            )

        return res

    def getHooks(self, newsSource: str) -> List[str]:
        hooks = list()
        try:
            dwh = DiscordWebHooks(name=newsSource).findAllByName()
            for i in dwh:
                hooks.append(i.key)
            return hooks
        except Exception as e:
            logger.critical(f"Unable to find DiscordWebhook for {newsSource.siteName}")

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

    def buildFooter(self, siteName: str) -> str:
        footer = ""
        end: str = "Brought to you by NewsBot"
        if "reddit" in siteName.lower():
            s = siteName.split(" ")
            footer = f"/r/{s[1]} - {end}"
            # embed.add_embed_field(name="Source", value=f"Reddit /r/{s[1]}")
        elif "Phantasy Star Online 2" in siteName:
            footer = f"Phantasy Star Online 2 - {end}"
        elif "Final Fantasy XIV" in siteName:
            footer = f"Final Fantasy XIV - {end}"
        elif "Pokemon Go Hub" in siteName:
            footer = f"Pokemon Go Hub - {end}"
        elif "Youtube" in siteName:
            s = siteName.split(" ")
            footer = f"Youtube - {s[1]} - {end}"
        elif "Instagram" in siteName:
            s = siteName.split(" ")
            if s[1] == "tag":
                footer = f"Instagram - #{s[2]} - {end}"
            elif s[1] == "user":
                footer = f"Instagram - {s[2]} - {end}"
        else:
            footer = end

        return footer

    def getEmbedColor(self, siteName: str) -> int:
        # Decimal values can be collected from https://www.spycolor.com
        if "Youtube" in siteName:
            return 16384771
        if "Instagram" in siteName:
            return 8913151
