from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import false, update
from wtforms import form
from newsbot.core.sql.tables import DiscordWebHooks, Sources, SourcesTable
from newsbot.web.ui.config.forms import DiscordWebhookAddForm, YoutubeNew

configSource = Blueprint(name="config.source", import_name=__name__, template_folder="templates")

@configSource.route("/<string:source>/list")
def list(source: str) -> None:
    r = SourcesTable().findAllBySource(source)
    #r:Sources = Sources(source=source).findAllBySource()
    if source == "finalfantasyxiv":
        return render_template("config/sources/ffxiv/list.html", items=r, sourceName=source)

    return render_template("config/sources/list.html", items=r, sourceName=source)


@configSource.route("/<string:source>/new", methods=["GET", "POST"])
def multiNew(source: str) -> None:
    discord = DiscordWebHooks().findAll()
    if request.method == "POST":
        if "youtube" in source:
            form = YoutubeNew(formdata=request.form)
            
            Sources(name=request.form[''], source='youtube',)
    
    return render_template(
        "/config/sources/new.html", discord=discord, sourceName=source
    )

@configSource.route("/<string:source>/edit/<string:id>", methods=["GET", "POST"])
def edit(source: str, id: str) -> None:
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
