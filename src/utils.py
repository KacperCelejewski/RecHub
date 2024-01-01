from functools import wraps

from flask import jsonify, make_response
from sqlalchemy.exc import IntegrityError

from src.extensions import db


def add_to_db(
    object_to_add,
):
    """
    Adds an object to the database.

    Parameters:
    object_to_add (object): The object to be added to the database.

    Returns:
    bool: True if the object was successfully added, False if there was an integrity error.
    """
    try:
        db.session.add(object_to_add)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False


def LogMethod(func):
    """
    Decorator that logs the method name, arguments, and keyword arguments before calling the method.

    Args:
        func: The method to be decorated.

    Returns:
        The decorated method.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args {args} and kwargs {kwargs}")
        return func(*args, **kwargs)

    return wrapper


def check_missing_data(data) -> bool or tuple:
    """
    Checks whether the data contains any missing values.

    Args:
        data (dict): The data to be checked.

    Returns:
        bool: True if the data contains missing values, False otherwise.
    """
    for key in data:
        if key is None or not data[key]:
            return True, key
    return False, None
