from flask import jsonify, Blueprint

api = Blueprint(name="api", import_name=__name__)

@api.route("/")
def index() -> str:
    return jsonify({'title':"hello from newsbot api"})