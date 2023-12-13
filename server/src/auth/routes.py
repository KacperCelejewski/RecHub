from flask import jsonify, make_response, request, session
from sqlalchemy.exc import IntegrityError

from src.auth import bp_auth
from src.extensions import db
from src.models.user import User, Password, Email
import pickle
from email_validator import EmailNotValidError
from src.models.user import PasswordNotValidError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)
from flask_jwt_extended import (
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
    jwt_refresh_token_required,
)


@bp_auth.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    for key in data:
        if key is None or data[key] == "":
            return make_response(jsonify({"message": f"Missing {key} parameter!"}), 400)
    password = Password(data["password"])
    email = Email(data["email"])
    try:
        is_valid_email = email.is_valid()
        is_valid_password = password.is_valid()
    except EmailNotValidError as e:
        return make_response(
            jsonify({"message": "Invalid email!", "error": str({e})}), 400
        )
    except PasswordNotValidError as e:
        return make_response(
            jsonify({"message": "Invalid password!", "error": str({e})}), 400
        )
    if is_valid_email and is_valid_password:
        if User.query.filter_by(email=email.email).first() is not None:
            return make_response(jsonify({"message": "User already exists!"}), 409)
        user = User(
            name=data["name"],
            surrname=data["surrname"],
            email=email.email,
            password_hashed=password.hash(),
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print(user)
            return make_response(jsonify({"message": "User already exists!"}), 409)
        return make_response(jsonify({"message": "User registered!"}), 201)
    else:
        return make_response(jsonify({"message": "Invalid email or password!"}), 400)


@bp_auth.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["email"] == "" or data["password"] == "":
        return make_response(jsonify({"message": "Missing email or password!"}), 400)
    email = data["email"]
    user = User.query.filter_by(email=email).first()
    if user is None:
        return make_response(jsonify({"message": "User not found!"}), 404)
    if not Password.check_corectness(data["password"], user.password_hashed):
        return make_response(jsonify({"message": "Invalid password!"}), 400)
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return make_response(
        jsonify(
            {
                "message": "User logged in!",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        200,
    )


@bp_auth.route("/api/auth/logout", methods=["GET"])
@jwt_required
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


@bp_auth.route("/api/auth/refresh", methods=["POST"])
@jwt_refresh_token_required()
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    new_refresh_token = create_refresh_token(identity=current_user_id)
    response = jsonify(
        {"access_token": new_access_token, "refresh_token": new_refresh_token}
    )
    set_access_cookies(response, new_access_token)
    set_refresh_cookies(response, new_refresh_token)

    return make_response(response, 200)
