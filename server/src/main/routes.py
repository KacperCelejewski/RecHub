from src.main import bp
from flask import make_response, jsonify


@bp.route("/test")
def test():
    return make_response(jsonify({"message": "App testing..."}), 200)


@bp.route("/")
def index(methods=["GET"]):
    return make_response(jsonify({"message": "Hello World!"}), 200)
