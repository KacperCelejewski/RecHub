from email_validator import EmailNotValidError, validate_email
from flask_login import UserMixin

from src.error_classes import PasswordNotValidError
from src.extensions import bcrypt, db


class Email:
    """
    Represents an email address.

    Attributes:
        email (str): The email address.

    Methods:
        is_valid: Checks if the email address is valid.
    """

    def __init__(self, email):
        self.email = email

    def is_valid(self):
        """
        Checks if the email address is valid.

        Returns:
            bool: True if the email address is valid, False otherwise.

        Raises:
            EmailNotValidError: If the email address is not valid.
        """
        try:
            valid = validate_email(self.email, check_deliverability=True)
            self.email = valid.normalized
            return True
        except EmailNotValidError:
            raise EmailNotValidError("Email is not valid!")

    def __repr__(self) -> str:
        return str(self.email)

    def __str__(self) -> str:
        return f"{self.email}"


class Password:
    """
    Represents a password object with validation and hashing functionality.
    """

    def __init__(self, password):
        self.password = password

    special_characters = "!@#$%^&*()-+?_=,<>/"

    def is_valid_length(self):
        """
        Checks if the password has a valid length.

        Returns:
            bool: True if the password has a valid length, False otherwise.

        Raises:
            PasswordNotValidError: If the password is too short (minimum 8 characters).
        """
        if len(self.password) >= 8:
            return True
        else:
            raise PasswordNotValidError("Password is too short! Minimum 8 characters!")

    def has_uppercase(self):
        """
        Checks if the password has at least one uppercase letter.

        Returns:
            bool: True if the password has at least one uppercase letter, False otherwise.

        Raises:
            PasswordNotValidError: If the password has no uppercase letters.
        """
        if any(c.isupper() for c in self.password):
            return True
        else:
            raise PasswordNotValidError("Password has no uppercase!")

    def has_lowercase(self):
        """
        Checks if the password has at least one lowercase letter.

        Returns:
            bool: True if the password has at least one lowercase letter, False otherwise.

        Raises:
            PasswordNotValidError: If the password has no lowercase letters.
        """
        if any(c.islower() for c in self.password):
            return True
        else:
            raise PasswordNotValidError("Password has no lowercase!")

    def has_digit(self):
        """
        Checks if the password has at least one digit.

        Returns:
            bool: True if the password has at least one digit, False otherwise.

        Raises:
            PasswordNotValidError: If the password has no digits.
        """
        if any(c.isdigit() for c in self.password):
            return True
        else:
            raise PasswordNotValidError("Password has no digit!")

    def has_special_character(self):
        """
        Checks if the password has at least one special character.

        Returns:
            bool: True if the password has at least one special character, False otherwise.

        Raises:
            PasswordNotValidError: If the password has no special characters.
        """
        if any(c in self.special_characters for c in self.password):
            return True
        else:
            raise PasswordNotValidError(
                "Password has no special character! Approved: !@#$%^&*()-+?_=,<>/"
            )

    def is_valid(self):
        """
        Checks if the password is valid by performing all validation checks.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        return (
            self.is_valid_length()
            and self.has_uppercase()
            and self.has_lowercase()
            and self.has_digit()
            and self.has_special_character()
        )

    def hash(self):
        """
        Hashes the password using bcrypt.

        Returns:
            str: The hashed password.
        """
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
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The user's name.
        surrname (str): The user's surname.
        email (str): The user's email address.
        password_hashed (str): The hashed password for the user.
        opinions (list): A list of opinions written by the user.
        representative (list): A list of representatives associated with the user.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surrname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password_hashed = db.Column(db.String(), unique=True, nullable=False)
    opinions = db.relationship("Opinion", backref="author", lazy=True)
    representative = db.relationship("Representative", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.name} {self.surrname} {self.email}>"
