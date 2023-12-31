from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from src.extensions import db
from src.models.representative import Representative
from src.models.user import User
from src.representative import bp_representatives


@bp_representatives.route("/api/representatives/add", methods=["POST"])
@jwt_required()
def add_representative():
    data = request.get_json()
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    representative = {
        "name": current_user.name,
        "surrname": current_user.surrname,
        "user_id": current_user.id,
        "company_id": data["company_id"],
    }
    representative = Representative(
        name=representative["name"],
        surrname=representative["surrname"],
        user_id=representative["user_id"],
        company_id=representative["company_id"],
    )
    try:
        db.session.add(representative)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return make_response(
            jsonify({"message": "{name} exists as representative of this company!"}),
            409,
        )

    return make_response(jsonify({"message": "Representative added!"}), 201)


@bp_representatives.route("/api/representatives/delete", methods=["DELETE"])
@jwt_required()
def delete_representative():
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    representative = Representative.query.filter_by(user_id=current_user.id).first()
    db.session.delete(representative)
    db.session.commit()
    return make_response(jsonify({"message": "Representative deleted!"}), 200)
