from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import false, update
from wtforms import form
from newsbot.core.sql.tables import DiscordWebHooks, Sources, SourcesTable, DiscordWebHooksTable, SourceLinksTable
from newsbot.web.ui.config.forms import DiscordWebhookAddForm, YoutubeNew

configSource = Blueprint(name="config.source", import_name=__name__, template_folder="templates")

@configSource.route("/<string:source>/")
def list(source: str) -> None:
    r = SourcesTable().findAllBySource(source)
    #r:Sources = Sources(source=source).findAllBySource()
    if source == "finalfantasyxiv":
        return render_template("config/sources/ffxiv/list.html", items=r, sourceName=source)

    return render_template("config/sources/list.html", items=r, sourceName=source)

@configSource.route("/<string:source>/new", methods=["GET", "POST"])
def multiNew(source: str) -> None:
    discord = DiscordWebHooksTable().findAll()
    if request.method == "GET":
        return render_template(
            "/config/sources/new.html", discord=discord, sourceName=source,
        )

    if request.method == "POST":
        isUpdated: bool = False
        if "youtube" in source:
            form = YoutubeNew(formdata=request.form)
            s = Sources(
                name = form.name.data,
                source = source,
                enabled=form.enabled.data,
                url= form.url.data,
                tags='',
                fromEnv=False
            )
            SourcesTable().add(s)
            isUpdated = True
            
        return render_template(
            "/config/sources/new.html", 
            discord=discord, sourceName=source, 
            isUpdated=isUpdated, form=form
        )

@configSource.route("/<string:source>/edit/<string:id>", methods=["GET", "POST"])
def edit(source: str, id: str) -> None:
    updated:bool = false
    err: str = ""
    table = SourcesTable()
    res = table.findById(id=id)
    hooks = DiscordWebHooksTable().findAll()
    linksTable = SourceLinksTable()

    if request.method == "POST":
        if source.lower() == "youtube":
            form = YoutubeNew(formdata=request.form)
            try:
                res.name = form.name.data
                res.url = form.url.data
                res.enabled = form.enabled.data
                #linksTable.
                table.add(res)
                updated: bool = True
            except Exception as e:
                err = f"Failed to update {source}.{res.name}. Error: {e}"
                print(err)
            
    return render_template(
        "/config/sources/edit.html", 
        sourceName=source, discord=hooks, 
        item=res, isUpdated=updated, err=err
    )
