from flask import jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from src.auth import bp_auth
from src.extensions import db
from src.models.user import User, Password, Email
import pickle
from email_validator import EmailNotValidError
from src.models.user import PasswordNotValidError


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
        password.hash()
        email = pickle.dumps(Email(data["email"]))
        password = pickle.dumps(password)
        user = User(
            name=data["name"],
            surrname=data["surrname"],
            email=email,
            password_hashed=password,
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
