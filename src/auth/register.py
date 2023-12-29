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
from src.db_func import add_to_db


class Register:
    """
    Class representing the registration process for a user.
    """

    def __init__(self, user: User):
        self.user = user
        self.user.email = Email(self.user.email)
        self.user.password = Password(self.user.password_hashed)

    def check_email_password_correcctness(self):
        """
        Checks the correctness of the email and password provided by the user.
        If either the email or password is invalid, it returns an error response.
        """
        try:
            is_valid_email = self.user.email.is_valid()
            is_valid_password = self.user.password.is_valid()
        except EmailNotValidError as:
        except PasswordNotValidError as :
            raise PasswordNotValidError("Password is not valid!")
        if not is_valid_email or not is_valid_password:
            raise ValueError("Email or password is not valid!")

    def check_whether_user_exists(self):
        """
        Checks whether a user with the same email already exists in the database.
        If a user with the same email exists, it returns an error response.
        """
        try:
            if User.query.filter_by(email=self.user.email.email).first() is not None:
                raise ValueError("User already exists!")
        except IntegrityError:
            db.session.rollback()
            raise ValueError("User already exists!")

    def register_user(self) -> Response:
        """
        Registers a new user by performing email and password correctness checks,
        checking whether the user already exists, and adding the user to the database.
        Returns a success response if the user is created successfully.
        """
        self.check_email_password_correcctness()
        self.check_whether_user_exists()
        self.user.email = self.user.email.email
        response = add_to_db(
            self.user,
        )
        return response
