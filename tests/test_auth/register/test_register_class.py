import pytest
from email_validator import EmailNotValidError

from src.auth.register import Register, UserAlreadyExistsError
from src.extensions import db
from src.models.user import Email, Password, PasswordNotValidError, User


@pytest.fixture
def create_user(email, password_hashed):
    """
    Fixture that creates a user with a given email and password.
    """
    user = User(
        name="John",
        surrname="Doe",
        email=email,
        password_hashed=password_hashed,
    )
    return user


@pytest.mark.parametrize(
    "email, password_hashed", [("sample@gmail.com", "Sam222ssple123!")]
)
def test_should_return_True_when_email_and_password_are_correct(
    create_user, email, password_hashed
):
    """
    GIVEN: A valid email and password.
    WHEN: The check_email_password_correcctness method is called.
    THEN: The method should return True.
    """
    register_instance = Register(create_user)
    result = register_instance.check_email_password_correcctness()
    assert result is True


@pytest.mark.parametrize("email, password_hashed", [("sample@gmail.com", "2!")])
def test_should_raise_PasswordNotValidError_when_password_is_not_valid(
    create_user, email, password_hashed
):
    """
    GIVEN: A password that is not valid.
    WHEN: The check_email_password_correcctness method is called.
    THEN: The method should raise a PasswordNotValidError.
    """
    register_instance = Register(create_user)
    with pytest.raises(PasswordNotValidError):
        register_instance.check_email_password_correcctness()


@pytest.mark.parametrize(
    "email, password_hashed", [("samplegmail.com", "Sam222ssple123!")]
)
def test_should_raise_EmailNotValidError_when_email_is_not_valid(
    create_user, email, password_hashed
):
    """
    GIVEN: An email that is not valid.
    WHEN: The check_email_password_correcctness method is called.
    THEN: The method should raise an EmailNotValidError."""
    register_instance = Register(create_user)
    with pytest.raises(EmailNotValidError):
        register_instance.check_email_password_correcctness()


@pytest.mark.parametrize(
    "email, password_hashed", [("sample@gmail.com", "Sam222ssple123!")]
)
def test_check_whether_user_exists_when_user_already_exists(
    create_user, client, email, password_hashed
):
    """
    GIVEN: A user with a given email already exists in the database.
    WHEN: The check_whether_user_exists method is called.
    THEN: The method should raise a UserAlreadyExistsError.
    """
    client.post(
        "/api/auth/register",
        json={
            "name": "John",
            "surrname": "Doe",
            "email": email,
            "password": password_hashed,
        },
    )
    register_instance = Register(create_user)

    with pytest.raises(UserAlreadyExistsError):
        register_instance.check_whether_user_exists()


@pytest.mark.parametrize(
    "email, password_hashed", [("samplse@gmail.com", "Sam222ssple123!")]
)
def test_check_whether_user_exists_when_user_does_not_exist(
    create_user, mocker, client, email, password_hashed
):
    """
    GIVEN: A user with a given email does not exist in the database.
    WHEN: The check_whether_user_exists method is called.
    THEN: The method should return None.
    """
    User.query.filter_by(email=create_user.email).delete()
    db.session.commit()

    register_instance = Register(create_user)

    result = register_instance.check_whether_user_exists()
    assert result is None
