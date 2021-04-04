from flask import Blueprint, render_template, request
from sqlalchemy.sql.expression import false
from wtforms import form
from newsbot.sql import DiscordWebHooks, Sources
from newsbotUi.config.forms import DiscordWebhookAddForm

config = Blueprint(
    name='config'
    ,import_name=__name__
    ,template_folder='templates'
)

@config.route('/')
def index() -> None:
    return render_template("config/index.html")


@config.route('/discord/list')
def discordList() -> None:
    res = DiscordWebHooks().findAll()
    return render_template('config/discord/list.html', items=res)

@config.route('/discord/new', methods=['GET','POST'])
def discordNew() -> None:
    form = DiscordWebhookAddForm(request.form)
    if request.method == "POST":
        print(f"Server = {request.form['server']}")
        print(f"Channel = {request.form['channel']}")
        print(f"URI = {request.form['url']}")

        name=f"{request.form['server']} - {request.form['channel']}"
        DiscordWebHooks(
            name = name
            ,server=request.form['server']
            ,channel=request.form['channel']
            ,url=request.form['url']
        ).add()
    
    return render_template('config/discord/new.html', form=form)

@config.route('/discord/edit/<string:id>', methods=['GET','POST'])
def discordEdit(id: str) -> None:
    hook = DiscordWebHooks()
    hook.id = id
    res: DiscordWebHooks = hook.findById()

    wasUpdated: bool = False

    if request.method == 'POST':
        res.server = request.form['server']
        res.channel = request.form['channel']
        res.url = request.form['url']
        res.name = f"{request.form['server']} - {request.form['channel']}"
        res.update()
        wasUpdated = True

    return render_template('config/discord/edit.html', res=res, updated=wasUpdated)

@config.route('/discord/delete/')
def discordDelete() -> None:
    return render_template('config/discord/delete.html')

def convertSourceName(source: str) -> str:
    if "ffxiv" in source:
        return "final fantasy xiv"
    elif "final fantasy xiv" in source:
        return "ffxiv"
    else:
        return source

def convertRouteName(source: str) -> str:
    if "final fantasy xiv":
        return "ffxiv"
    else:
        return source

@config.route('/source/<string:source>/list')
def sourceList(source:str) -> None:
    source = convertSourceName(source)
    r = Sources(source).findAllByName()
    return render_template('config/sources/list.html', items=r, sourceName=source)

@config.route('/source/<string:source>/new', methods=['GET', 'POST'])
def sourceMultiNew(source:str) -> None:
    source = convertSourceName(source)
    discord = DiscordWebHooks().findAll()
    if request.method == "POST":
        Sources()
    return render_template('/config/sources/new.html', discord=discord, sourceName=source)

@config.route('/source/<string:source>/edit')
def sourceEdit(source:str) -> None:
    source = convertSourceName(source)
    return render_template('/config/sources/edit.html', sourceName=source)

@config.route('/wizzard')
def wizzard() -> None:
    return render_template('config/wizzard.html')

