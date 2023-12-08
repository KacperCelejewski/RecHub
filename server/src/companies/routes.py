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


@bp_companies.route("/api/companies/", methods=["GET"])
def get_companies():
    params = {
        "industry": request.args.get("industry", default=None, type=str),
        "technology": request.args.get("technology", default=None, type=str),
        "location": request.args.get("location", default=None, type=str),
    }
    print(params)
    if params:
        try:
            companies = Company.query.filter_by(
                industry=params["industry"]).all() if params["industry"] else Company.query.all()
            companies = Company.query.filter_by(
                technology=params["technology"]).all() if params["technology"] else Company.query.all()
            companies = Company.query.filter_by(
                location=params["location"]).all() if params["location"] else Company.query.all()
            
            companies = [
                {company.id:{
                    "name": company.name,
                    "location": company.location,
                    "technology": company.technology,
                    "industry": company.industry,
                    "ceo": company.ceo,
                    "description": company.description,
                }}
                for company in companies
            ]
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"message": "No companies found!"}), 404)

    return make_response(jsonify({"companies": companies}), 200)
