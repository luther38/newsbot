from flask import json, jsonify, Blueprint
from sqlalchemy.ext.declarative import api
from newsbot.core.sql.tables import Sources, SourcesTable

apiSources = Blueprint(name="Sources", import_name=__name__)

@apiSources.route("/list", methods=["GET"])
def list() -> jsonify:
    s = Sources().findAll()
    return jsonify(SourcesTable().toListDict(s))
    
@apiSources.route('/add', methods=['POST'])
def add() -> jsonify:
    SourcesTable().add(Sources(name="Demo"))
    s = Sources().add()

