import base64

from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from src.companies import bp_companies
from src.extensions import db
from src.models.company import Company, Logo
from src.models.representative import Representative


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
        website=data["website"],
    )
    try:
        db.session.add(company)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "Company already exists!"}), 409)

    return make_response(
        jsonify({"message": "Company added!", "company_id": company.id}), 201
    )


@bp_companies.route("/api/companies/", methods=["GET"])
def get_companies():
    params = {
        "industry": request.args.get("industry", default=None, type=str),
        "technology": request.args.get("technology", default=None, type=str),
        "location": request.args.get("location", default=None, type=str),
    }
    print(params["industry"])
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
    avg_rating = company.average_rating()
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
                    "website": company.website,
                    "avg_rating": avg_rating,
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


@bp_companies.route("/api/companies/edit/<int:company_id>", methods=["PUT"])
@jwt_required()
def edit_company(company_id):
    company = Company.query.get_or_404(company_id)
    representative = Representative.query.filter_by(company_id=company_id).first()
    if representative is None:
        return make_response(jsonify({"message": "You are not a representative!"}), 401)
    current_user_id = get_jwt_identity()
    if current_user_id != representative.user_id:
        return make_response(jsonify({"message": "You are not a representative!"}), 401)
    data = request.get_json()
    company.name = data["name"]
    company.industry = data["industry"]
    company.technology = data["technology"]
    company.location = data["location"]
    company.ceo = data["ceo"]
    company.description = data["description"]
    company.website = data["website"]
    db.session.commit()

    return make_response(jsonify({"message": "Company updated!"}), 200)


@bp_companies.route("/api/companies/delete/<int:company_id>", methods=["DELETE"])
@jwt_required()
def delete_company(company_id):
    company = Company.query.get_or_404(company_id)
    current_user_id = get_jwt_identity()
    representatives = Representative.query.filter_by(company_id=company_id)
    for representative in representatives:
        if representative is None:
            return make_response(
                jsonify({"message": "You are not a representative!"}), 401
            )
        if current_user_id != representative.user_id:
            return make_response(
                jsonify({"message": "You are not a representative!"}), 401
            )
    db.session.delete(company)
    db.session.commit()
    return make_response(jsonify({"message": "Company deleted!"}), 200)


@bp_companies.route("/api/companies/logo/upload", methods=["POST"])
def upload_logo():
    logo = request.files["logo"]
    if not logo:
        return make_response(jsonify({"message": "No logo uploaded!"}), 400)
    filename = secure_filename(logo.filename)
    mimetype = logo.mimetype
    company_id = request.form.get("company_id")

    logo = Logo(
        logo=logo.read(), mimetype=mimetype, name=filename, company_id=company_id
    )
    if logo.check_mimetype() is False:
        return make_response(
            jsonify(
                {"message": "Invalid mimetype! Only jpeg or png types are available"}
            ),
            415,  # Unsupported Media Type
        )
    print(logo.check_size())
    if logo.check_size() is False:
        return make_response(
            jsonify({"message": "File too large! Max size is 1MB "}),
            413,  # Payload Too Lar
        )
    db.session.add(logo)
    db.session.commit()
    return make_response(jsonify({"message": "Logo uploaded!"}), 201)


@bp_companies.route("/api/companies/logo/<int:company_id>", methods=["GET"])
def get_logo(company_id):
    Company.query.get_or_404(company_id)
    logo = Logo.query.filter_by(company_id=company_id).first()
    if logo is None:
        return make_response(jsonify({"message": "Logo not found!"}), 404)

    logo_data_base64 = base64.b64encode(logo.logo).decode("utf-8")
    return make_response(
        jsonify(
            {
                "logo": {
                    "logo": logo_data_base64,
                    "name": logo.name,
                    "mimetype": logo.mimetype,
                }
            }
        ),
        200,
    )
