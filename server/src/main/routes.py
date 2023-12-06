from src.main import bp
from flask import make_response, jsonify
from src.models.company import Company
from src.extensions import db


@bp.route("/test")
def test():
    return make_response(jsonify({"message": "App testing..."}), 200)


@bp.route("/")
def index(methods=["GET"]):
    companies = Company.query.all()
    companies = [company.to_dict() for company in companies]

    return make_response(jsonify({"companies": companies}), 200)
