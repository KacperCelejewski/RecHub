from flask import Response, jsonify, make_response
from sqlalchemy.exc import IntegrityError

from src.error_classes import UserAlreadyExistsError
from src.extensions import db
from src.models.user import (
    Email,
    EmailNotValidError,
    Password,
    PasswordNotValidError,
    User,
)
from src.utils import LogMethod, add_to_db


class Register:
    """
    Class representing the registration process for a user.
    """

    def __init__(self, user: User):
        self.user = user
        self.user.email = Email(self.user.email)
        self.user.password = Password(self.user.password_hashed)

    @LogMethod
    def check_email_password_correcctness(self):
        """
        Checks the correctness of the email and password provided by the user.
        If either the email or password is invalid, it returns an error response.
        """

        try:
            self.user.email.is_valid()
            self.user.password.is_valid()

        except EmailNotValidError:
            raise EmailNotValidError("Email is not valid!")
        except PasswordNotValidError:
            raise PasswordNotValidError("Password is not valid!")
        else:
            return True

    @LogMethod
    def check_whether_user_exists(self):
        """
        Checks whether a user with the same email already exists in the database.
        If a user with the same email exists, it returns an error response.
        """
        try:
            if User.query.filter_by(email=self.user.email.email).first() is not None:
                raise UserAlreadyExistsError("User already exists!")
        except IntegrityError:
            db.session.rollback()
            raise UserAlreadyExistsError("User already exists!")

    @LogMethod
    def register_user(self) -> Response:
        """
        Registers a new user by performing email and password correctness checks,
        checking whether the user already exists, and adding the user to the database.
        Returns a success response if the user is created successfully.
        """
        self.check_email_password_correcctness()
        self.check_whether_user_exists()

        # Extracting the email address from the Email object
        self.user.email = self.user.email.email

        # Hashing the password in the Password object that is stored in the User object
        self.user.password_hashed = self.user.password.hash()

        # if the user is not created successfully, return False
        is_user_crearted = add_to_db(
            self.user,
        )
        return is_user_crearted  # True or False

    def __repr__(self) -> str:
        return f'Register("{self.user.name}")'
