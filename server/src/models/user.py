from src.extensions import bcrypt
from src.extensions import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surrname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(), unique=True, nullable=False)

    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def is_valid_email(self):
        return "@" in self.email and "." in self.email

    def is_valid_password(self, password) -> bool:
        """
        Checks if the given password is valid.

        Parameters:
        password (str): The password to be checked.

        Returns:
        bool: True if the password is valid, False otherwise.
            """
        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        # Check the length of the password
        is_valid_length = len(password) >= 8

        # Combine all conditions
        return has_uppercase and has_lowercase and has_digit and is_valid_length
