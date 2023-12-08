from flask import jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from src.auth import bp_auth
from src.extensions import db
from src.models.user import User


@bp_auth.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    user = User(name=data["name"], surname=data["surrname"], email=data["email"])
    if user.is_valid_email() and user.is_valid_password(data["password"]):
        return make_response(jsonify({"message": "Invalid email or password!"}), 400)
    user.password_hash(data["password"])
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "User already exists!"}), 409)

    return make_response(jsonify({"message": "User registered!"}), 201)
