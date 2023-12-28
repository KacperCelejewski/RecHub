from flask import Response, jsonify, make_response
from sqlalchemy.exc import IntegrityError
from src.extensions import db
from src.models.user import (
    EmailNotValidError,
    PasswordNotValidError,
    User,
    Password,
    Email,
)


class Register :
    """
    Class representing the registration process for a user.
    """

    def __init__(self, user: User):
        self.user = user

    def check_email_password_correcctness(self):
        """
        Checks the correctness of the email and password provided by the user.
        If either the email or password is invalid, it returns an error response.
        """
        try:
            is_valid_email = self.user.email.is_valid()
            is_valid_password = self.user.password.is_valid()
        except EmailNotValidError as e:
            return make_response(
                jsonify({"message": "Invalid email!", "error": str({e})}), 400
            )
        except PasswordNotValidError as e:
            return make_response(
                jsonify({"message": "Invalid password!", "error": str({e})}), 400
            )
        if not is_valid_email or not is_valid_password:
            return make_response(
                jsonify({"message": "Invalid email or password!"}), 400
            )

    def check_whether_user_exists(self):
        """
        Checks whether a user with the same email already exists in the database.
        If a user with the same email exists, it returns an error response.
        """
        try:
            if User.query.filter_by(email=self.user.email).first() is not None:
                return make_response(jsonify({"message": "User already exists!"}), 409)
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"message": "User not created!"}), 400)

    def register_user(self, username, email: Email, password: Password):
        """
        Registers a new user by performing email and password correctness checks,
        checking whether the user already exists, and adding the user to the database.
        Returns a success response if the user is created successfully.
        """
        self.check_email_password_correcctness()
        self.check_whether_user_exists()

        return add_to_db(
            self.user,
            f"User {username} created!",
            f"User {username} not created!",
        )
