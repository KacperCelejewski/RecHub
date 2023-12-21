from flask import jsonify, make_response, request
from flask_login import login_required, current_user
from src.models.opinion import Opinion
from src.models.company import Company
from src.extensions import db
from sqlalchemy.exc import IntegrityError
from src.newsletter import bp_newsletter as bp
from mailbox import Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.extensions import mail
from src.models.user import User


@bp.route("/api/newsletter/subscribe", methods=["POST"])
@jwt_required()
def subscribe():
    """
    Subscribes a user to the newsletter.
    Sends a welcome email to the user. ONLY FOR TESTING PURPOSES.

    Returns:
        A response object with a success message if the subscription is successful,
        or an error message if something goes wrong.
    """
    current_user_id = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_id).first()
    data = request.get_json()
    agreement = data["agreement"]
    if agreement == False:
        return make_response(jsonify({"message": "You must agree to subscribe!"}), 400)
    email = current_user.email

    try:
        mail.send_message(
            "Newsletter subscription",
            sender="a08e4268b243ee@mailtrap.io",
            recipients=[email],
            body="Welcome to the newsletter! Stay tuned for more!",
        )

        return make_response(jsonify({"message": "Subscribed!"}), 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Something went wrong!", "error": e}), 400
        )
