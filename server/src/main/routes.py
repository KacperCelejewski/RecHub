from flask import jsonify, make_response, render_template

from src.main import bp_main


@bp_main.route("/test")
def test():
    return make_response(jsonify({"message": "App testing..."}), 200)


@bp_main.route("/api/")
def index_json(methods=["GET"]):

    return make_response(jsonify({"meassege": "This message is only for sample purpose!"}), 200)

@bp_main.route("/web/")
def index_html():
    return render_template("main/index.html")
