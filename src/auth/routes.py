import pickle

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
from src.auth.register import Register, UserAlreadyExistsError
from src.extensions import db
from src.models.user import Email, Password, PasswordNotValidError, User
from src.utils import add_to_db, check_missing_data


@bp_auth.route("/api/auth/register", methods=["POST"])
def register():
    """
    Register a new user.

    This function handles the registration of a new user by receiving a JSON payload
    containing the user's name, email, password, and surname. It checks for missing
    parameters, validates the email and password, and creates a new User instance.
    The User instance is then passed to the Register class to register the user.
    If the registration is successful, a response with status code 201 is returned,
    indicating that the user has been created. If there are any errors during the
    registration process, appropriate error messages with corresponding status codes
    are returned.

    Returns:
        A JSON response with a message indicating the result of the registration.

    Raises:
        EmailNotValidError: If the provided email is not valid.
        PasswordNotValidError: If the provided password is not valid.
        UserAlreadyExistsError: If a user with the same email already exists.
    """
    data = request.get_json()
    is_missing, key = check_missing_data(data)
    if is_missing:
        return make_response(jsonify({"message": f"Missing {key} parameter"}), 400)

    user_to_register = User(
        name=data["name"],
        email=data["email"],
        password_hashed=data["password"],
        surrname=data["surrname"],
    )
    register_instance = Register(user_to_register)
    try:
        result_of_user_register = register_instance.register_user()
    except EmailNotValidError:
        return make_response(
            jsonify({"message": "Email is not valid!", "error": EmailNotValidError}),
            400,
        )
    except PasswordNotValidError:
        return make_response(jsonify({"message": "Password is not valid!"}), 400)
    except UserAlreadyExistsError:
        return make_response(jsonify({"message": "User already exists!"}), 400)

    if result_of_user_register is False:
        return make_response(jsonify({"message": "User not created!"}), 409)
    else:
        return make_response(jsonify({"message": "User created!"}), 201)


@bp_auth.route("/api/auth/login", methods=["POST"])
def login():
    """
    Logs in a user by validating their credentials and generating access and refresh tokens.

    Returns:
        A response object with a JSON containing the following keys:
            - "message": A message indicating whether the login was successful or not.
            - "access_token": An access token for the authenticated user.
            - "refresh_token": A refresh token for the authenticated user.
    """
    data = request.get_json()
    is_missing, key = check_missing_data(data)
    if is_missing:
        return make_response(jsonify({"message": f"Missing {key} parameter"}), 400)

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
def check_token_status():
    """
    Check the status of the token.

    Returns:
        A response with a message indicating whether the token is valid or invalid.
    """
    if get_jwt_identity():
        return make_response(jsonify({"message": "Token is valid!"}), 200)
    else:
        return make_response(jsonify({"message": "Token is invalid!"}), 401)


@bp_auth.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout the user by removing the JWT cookies from the response.

    Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


@bp_auth.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    Refreshes the access token and refresh token for the authenticated user.

    Returns:
        A response object with the new access token and refresh token.
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    new_refresh_token = create_refresh_token(identity=current_user_id)
    response = jsonify(
        {"access_token": new_access_token, "refresh_token": new_refresh_token}
    )
    set_access_cookies(response, new_access_token)
    set_refresh_cookies(response, new_refresh_token)

    return make_response(response, 200)
