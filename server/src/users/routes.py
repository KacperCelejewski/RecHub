from src.main import bp
from flask import make_response, jsonify, render_template, request
from src.models.company import Company
from src.extensions import db


@bp.route("/api/companies", methods=["GET"])
def get_companies():
    params = {
        "industry": request.args.get("industry"),
        "technology": request.args.get("technology"),
        "location": request.args.get("location"),
    }
    if params:
        try:
            companies = Company.query.filter_by(
                industry=params["industry"],
                technology=params["technology"],
                location=params["location"],
            ).all()
        except IntegrityError:
            return make_response(
                jsonify({"message": "No companies found!"}), 404
            )
    else:
        companies = Company.query.all()

    return make_response(
        jsonify({"companies": [company.to_dict() for company in companies]}), 200
    )
