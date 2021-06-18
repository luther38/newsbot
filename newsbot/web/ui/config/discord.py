from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import false, update
from newsbot.core.sql.tables import DiscordWebHooks, DiscordWebHooksTable
from wtforms import Form, StringField
from wtforms import validators
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, URL

configDiscord = Blueprint(name="config.discord", import_name=__name__, template_folder="templates")

@configDiscord.route("/")
def list() -> None:
    res = DiscordWebHooks().findAll()
    return render_template("config/discord/list.html", items=res)

class DiscordWebhookAddForm(Form):
    server = StringField("server", validators=[DataRequired()])
    channel = StringField("channel", validators=[DataRequired()])
    url = StringField("url", validators=[URL()])
    pass

@configDiscord.route("/new", methods=["GET", "POST"])
def new() -> None:
    isUpdated: bool = false
    if request.method == "POST":
        form = DiscordWebhookAddForm(request.form)
        item = DiscordWebHooks(
            name = f"{request.form['server']} - {request.form['channel']}",
            server=form.server.data,
            channel=form.channel.data,
            url=form.url.data,
        )
        DiscordWebHooksTable().add(item)
        isUpdated = True
        return render_template("config/discord/new.html", form=item, isUpdated=isUpdated)
    else:
        return render_template("config/discord/new.html", update=isUpdated)

@configDiscord.route("/edit/<string:id>", methods=["GET", "POST"])
def edit(id: str) -> None:  
    table = DiscordWebHooksTable()
    res = table.findById(id)
    wasUpdated: bool = False
    if request.method == "POST":
        server = request.form['server']
        channel= request.form['channel']

        res.server = server
        res.channel = channel
        res.url = request.form['url']
        res.name = f"{server} - {channel}"
        
        table.add(item=res)
        wasUpdated = True

    return render_template("config/discord/edit.html", res=res, updated=wasUpdated)

@configDiscord.route("/delete/<string:id>", methods=["GET", "POST"])
def delete(id:str) -> None:
    res = DiscordWebHooksTable().findById(id)
    isDeleted = False
    if request.method == "POST":
        isDeleted = DiscordWebHooksTable().delete(id=id)
    return render_template("config/discord/delete.html", form=res, updated=isDeleted)

