from flask import json, jsonify, Blueprint
from sqlalchemy.ext.declarative import api
from newsbot.core.sql.tables import DiscordWebHooks, DiscordWebHooksTable

apiDiscordWebHooks = Blueprint(name="ApiDiscordWebHooks", import_name=__name__)

@apiDiscordWebHooks.route('/list', methods=['GET'])
def list() -> jsonify:
    s = DiscordWebHooksTable().findAll()
    return jsonify(DiscordWebHooksTable().toListDict(s))

@apiDiscordWebHooks.route('/add', methods=['POST'])
def add() -> jsonify:
    s = DiscordWebHooksTable().add(DiscordWebHooks())