from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import false
from wtforms import form
from newsbot.core.sql.tables import DiscordWebHooks, Sources
from newsbotUi.config.forms import DiscordWebhookAddForm, YoutubeNew
from json import loads

configDiscord = Blueprint(name="config.discord", import_name=__name__, template_folder="templates")

@configDiscord.route("/")
def list() -> None:
    res = DiscordWebHooks().findAll()
    return render_template("config/discord/list.html", items=res)

@configDiscord.route("/new", methods=["GET", "POST"])
def new() -> None:
    form = DiscordWebhookAddForm(request.form)
    if request.method == "POST":
        print(f"Server = {request.form['server']}")
        print(f"Channel = {request.form['channel']}")
        print(f"URI = {request.form['url']}")

        name = f"{request.form['server']} - {request.form['channel']}"
        DiscordWebHooks(
            name=name,
            server=request.form["server"],
            channel=request.form["channel"],
            url=request.form["url"],
        ).add()

    return render_template("config/discord/new.html", form=form)


@configDiscord.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id: str) -> None:
    hook = DiscordWebHooks()
    hook.id = id
    res: DiscordWebHooks = hook.findById()

    wasUpdated: bool = False

    if request.method == "POST":
        res.server = request.form["server"]
        res.channel = request.form["channel"]
        res.url = request.form["url"]
        res.name = f"{request.form['server']} - {request.form['channel']}"
        res.update()
        wasUpdated = True

    return render_template("config/discord/edit.html", res=res, updated=wasUpdated)


@configDiscord.route("/delete/")
def delete() -> None:
    return render_template("config/discord/delete.html")

