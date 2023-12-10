from flask import jsonify, make_response, request, session
from sqlalchemy.exc import IntegrityError

from src.auth import bp_auth
from src.extensions import db
from src.models.user import User, Password, Email
import pickle
from email_validator import EmailNotValidError
from src.models.user import PasswordNotValidError
from flask_login import login_user, logout_user, current_user, login_required


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
    if data["email"] is None or data["password"] is None:
        return make_response(jsonify({"message": "Missing email or password!"}), 400)
    email = data["email"]
    user = User.query.filter_by(email=email).first()
    if user is None:
        return make_response(jsonify({"message": "User not found!"}), 404)
    if not Password.check_corectness(data["password"], user.password_hashed):
        return make_response(jsonify({"message": "Invalid password!"}), 400)
    login_user(user)
    return make_response(jsonify({"message": "User logged in!"}), 200)


@login_required
@bp_auth.route("/api/auth/logout", methods=["GET"])
def logout():
    logout_user()
    return make_response(jsonify({"message": "User logged out!"}), 200)



@bp_auth.route("/api/auth/is_logged", methods=["GET"])
def is_logged():
    if current_user.is_authenticated:
        return make_response(jsonify({"message": "User is logged in!"}), 200)
    else:
        return make_response(jsonify({"message": "User is not logged in!"}), 200)
