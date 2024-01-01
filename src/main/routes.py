from flask import jsonify, make_response, render_template

from src.main import bp_main


@bp_main.route("/test")
def test():
    return make_response(jsonify({"message": "App testing..."}), 200)
