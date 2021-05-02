from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import false, update
from wtforms import form
from newsbot.core.sql.tables import DiscordWebHooks, Sources
from newsbotUi.config.forms import DiscordWebhookAddForm, YoutubeNew
from json import loads

config = Blueprint(name="config", import_name=__name__, template_folder="templates")


@config.route("/")
def index() -> None:
    return render_template("config/index.html")

@config.route("/source/<string:source>/list")
def sourceList(source: str) -> None:
    r:Sources = Sources(source=source).findAllBySource()
    if source == "finalfantasyxiv":
        return render_template("config/sources/ffxiv/list.html", items=r, sourceName=source)

    return render_template("config/sources/list.html", items=r, sourceName=source)


@config.route("/source/<string:source>/new", methods=["GET", "POST"])
def sourceMultiNew(source: str) -> None:
    discord = DiscordWebHooks().findAll()
    if request.method == "POST":
        if "youtube" in source:
            form = YoutubeNew(formdata=request.form)
            Sources(name=request.form[''], source='youtube',)
    
    return render_template(
        "/config/sources/new.html", discord=discord, sourceName=source
    )

@config.route("/source/<string:source>/edit/<string:id>", methods=["GET", "POST"])
def sourceEdit(source: str, id: str) -> None:
    updated:bool = false
    err: str = ""
    s = Sources()
    s.id = id
    res: Sources = s.findById()

    if request.method == "POST":
        try:
            res.name = request.form['name']
            res.url = request.form['url']
            res.enabled = bool(request.form['enabled'])
            res.updateId(id)
            updated: bool = True
        except Exception as e:
            err = f"Failed to update {source}.{res.name}. Error: {e}"
            print(err)
            
    return render_template("/config/sources/edit.html", sourceName=source, item=res, updated=updated, err=err)


@config.route("/wizzard")
def wizzard() -> None:
    return render_template("config/wizzard.html")
