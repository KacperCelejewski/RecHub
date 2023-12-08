from src.companies import bp_companies
from flask import make_response, jsonify, render_template, request
from src.models.company import Company
from src.extensions import db
from sqlalchemy.exc import IntegrityError

@bp_companies.route("/api/companies/add", methods=["POST"])
def add_company():
    data = request.get_json()
    company = Company(
        name=data["name"],
        industry=data["industry"],
        technology=data["technology"],
        location=data["location"],
        ceo=data["ceo"],
        description=data["description"],
    )
    try:
        db.session.add(company)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "Company already exists!"}), 409)

    return make_response(jsonify({"message": "Company added!"}), 201)
@bp_companies.route("/api/companies", methods=["GET"])
def get_companies():
    params = {
        "industry": request.args.get("industry", default=None, type=str),
        "technology": request.args.get("technology", default=None, type=str),
        "location": request.args.get("location", default=None, type=str),
    }
    if params:
        try:
            companies = Company.query.filter_by(
                industry=params["industry"],
                technology=params["technology"],
                location=params["location"],
            ).all()
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"message": "No companies found!"}), 404)
    else:
        companies = Company.query.all()

    return make_response(
        jsonify({"companies": [company.to_dict() for company in companies]}), 200
    )
