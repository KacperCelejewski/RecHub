import pickle

from src.db_func import add_to_db
from email_validator import EmailNotValidError
from flask import jsonify, make_response, request, session
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from sqlalchemy.exc import IntegrityError
from src.auth import bp_auth
from src.extensions import db
from src.models.user import Email, Password, PasswordNotValidError, User
from src.auth.register import Register


@bp_auth.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    for key in data:
        if key is None or not data[key]:
            return make_response(jsonify({"message": f"Missing {key} parameter!"}), 409)

    user_to_register = User(
        name=data["name"],
        email=data["email"],
        password_hashed=data["password"],
        surrname=data["surrname"],
    )
    register_instance = Register(user_to_register)
    try:
        response = register_instance.register_user()
    except EmailNotValidError:
        return make_response(jsonify({"message": "Email is not valid!"}), 400)
    except PasswordNotValidError:
        return make_response(jsonify({"message": "Password is not valid!"}), 400)
    except ValueError as e:
        return make_response(jsonify({"message": str(e)}), 400)

    if response is False:
        return make_response(jsonify({"message": "User not created!"}), 400)
    else:
        return make_response(jsonify({"message": "User created!"}), 201)


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


@bp_auth.route("/api/auth/check-token-status", methods=["POST"])
@jwt_required()
def check_token_status():
    if get_jwt_identity():
        return make_response(jsonify({"message": "Token is valid!"}), 200)
    else:
        return make_response(jsonify({"message": "Token is invalid!"}), 401)


@bp_auth.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


@bp_auth.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
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
