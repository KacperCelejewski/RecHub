from flask import jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from src.representative import bp_representatives
from src.extensions import db
from src.models.representative import Representative

@bp_representatives.route("/api/representatives/add", methods=["POST"])
def add_representative():
    data = request.get_json()
    representative = Representative(
        name=data["name"],
        surrname=data["surrname"],
        user_id=data["user_id"],
        company_id=data["company_id"],
    )
    try:
        db.session.add(representative)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "{name} exists as representative of this company!"}), 409)

    return make_response(jsonify({"message": "Representative added!"}), 201)