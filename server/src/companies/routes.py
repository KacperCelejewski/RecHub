from flask import jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from src.companies import bp_companies
from src.extensions import db
from src.models.company import Company


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
    try:
        if params["industry"] is not None:
            companies = Company.query.filter_by(industry=params["industry"]).all()


        elif params["technology"] is not None:
            companies = Company.query.filter_by(technology=params["technology"]).all()

        elif params["location"] is not None:
            companies = Company.query.filter_by(location=params["location"]).all()
        else:
            companies = Company.query.all()

        companies = [
            {
                "id": company.id,
                "name": company.name,
                "location": company.location,
                "technology": company.technology,
                "industry": company.industry,
                "ceo": company.ceo,
                "description": company.description,
            }
            for company in companies
        ]
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "No companies found!"}), 404)

    return make_response(jsonify({"companies": companies}), 200)


@bp_companies.route("/api/companies/<int:company_id>", methods=["GET"])
def get_company(company_id):
    company = Company.query.get_or_404(company_id)
    return make_response(
        jsonify(
            {
                "company": {
                    "name": company.name,
                    "location": company.location,
                    "technology": company.technology,
                    "industry": company.industry,
                    "ceo": company.ceo,
                    "description": company.description,
                }
            }
        ),
        200,
    )


@bp_companies.route("/api/companies/<int:company_id>", methods=["PUT"])
def update_company(company_id):
    company = Company.query.get_or_404(company_id)
    data = request.get_json()
    company.name = data["name"]
    company.industry = data["industry"]
    company.technology = data["technology"]
    company.location = data["location"]
    company.ceo = data["ceo"]
    company.description = data["description"]
    db.session.commit()
    return make_response(jsonify({"message": "Company updated!"}), 200)
