from flask import jsonify, make_response, request
from flask_login import login_required, current_user
from src.models.opinion import Opinion
from src.models.company import Company
from src.extensions import db
from sqlalchemy.exc import IntegrityError
from src.newsletter import bp_newsletter as bp

from flask_jwt_extended import jwt_required, get_jwt_identity


@bp.route("/api/subscribe", methods=["POST"])
@jwt_required()
def subscribe():
    pass
