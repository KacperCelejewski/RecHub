from src.main import bp
from flask import make_response, jsonify, render_template
from src.models.company import Company
from src.extensions import db


@bp.route("/test")
def test():
    return make_response(jsonify({"message": "App testing..."}), 200)


@bp.route("/api/")
def index_json(methods=["GET"]):

    return make_response(jsonify({"meassege": "This message is only for sample purpose!"}), 200)

@bp.route("/web/")
def index_html():
    return render_template("main/index.html")
