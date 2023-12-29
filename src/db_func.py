from flask import jsonify, make_response
from src.extensions import db
from sqlalchemy.exc import IntegrityError


def add_to_db(
    object_to_add,
):
    try:
        db.session.add(object_to_add)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False
