from src.extensions import bcrypt
from src.extensions import db
from email_validator import validate_email, EmailNotValidError
from flask_login import UserMixin


class Email:
    def __init__(self, email):
        self.email = email

    def is_valid(self):
        try:
            valid = validate_email(self.email, check_deliverability=True)
            self.email = valid.normalized
            return True
        except EmailNotValidError:
            raise EmailNotValidError("Email is not valid!")


class PasswordNotValidError(Exception):
    pass


class Password:
    def __init__(self, password):
        self.password = password

    special_characters = "!@#$%^&*()-+?_=,<>/"

    def is_valid_length(self):
        if len(self.password) >= 8:
            return True
        else:
            raise PasswordNotValidError("Password is too short! Minimum 8 characters!")

    def has_uppercase(self):
        if any(c.isupper() for c in self.password):
            return True
        else:
            raise PasswordNotValidError("Password has no uppercase!")

    def has_lowercase(self):
        if any(c.islower() for c in self.password):
            return True
        else:
            raise PasswordNotValidError("Password has no lowercase!")

    def has_digit(self):
        if any(c.isdigit() for c in self.password):
            return True
        else:
            raise PasswordNotValidError("Password has no digit!")

    def has_special_character(self):
        if any(c in self.special_characters for c in self.password):
            return True
        else:
            raise PasswordNotValidError(
                "Password has no special character! Approved: !@#$%^&*()-+?_=,<>/"
            )

    def is_valid(self):
        return (
            self.is_valid_length()
            and self.has_uppercase()
            and self.has_lowercase()
            and self.has_digit()
            and self.has_special_character()
        )

    def hash(self):
        self._password_hash = bcrypt.generate_password_hash(self.password)
        self._password_hash = self._password_hash.decode("utf-8")
        return self._password_hash

    @staticmethod
    def check_corectness(plain_password: str, password_hashed) -> bool:
        """
        Check the correctness of a plain password against a hashed password.

        Args:
            plain_password (str): The plain password to be checked.
            password_hashed (str): The hashed password to be compared against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return bcrypt.check_password_hash(password_hashed, plain_password)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surrname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password_hashed = db.Column(db.String(), unique=True, nullable=False)
    opinions = db.relationship("Opinion", backref="author", lazy=True)


    def __repr__(self):
        return f"<User {self.name} {self.surrname} {self.email} {self.password_hashed}>"
