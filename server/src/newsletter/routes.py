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
from src.models.mailing_list import MailingList


@bp.route("/api/newsletter/subscribe", methods=["POST"])
def subscribe():
    """
    Subscribes a user to the newsletter.
    Sends a welcome email to the user. ONLY FOR TESTING PURPOSES.

    Returns:
        A response object with a success message if the subscription is successful,
        or an error message if something goes wrong.
    """

    data = request.get_json()
    agreement = data["agreement"]
    email = data["email"]
    if agreement is False:
        return make_response(jsonify({"message": "You must agree to subscribe!"}), 400)
    if email == "":
        return make_response(jsonify({"message": "Email cannot be empty!"}), 400)
    MailingList.add_email_adress(email)
    try:
        #! This is only for testing purposes. Remove this in production.
        mail.send_message(
            "Newsletter subscription",
            sender="sample@mailtrap.io",
            recipients=[email],
            body="Welcome to the newsletter! Stay tuned for more!",
        )

        return make_response(jsonify({"message": "Subscribed!"}), 200)
    except Exception as e:
        return make_response(
            jsonify({"message": "Something went wrong!", "error": e}), 400
        )

@bp.route("/api/newsletter/unsubscribe", methods=["POST"])
def unsubscribe():
    """
    Unsubscribes a user from the newsletter.

    Returns:
        A response object with a success message if the unsubscription is successful,
        or an error message if something goes wrong.
    """

    data = request.get_json()
    email = data["email"]
    if email == "":
        return make_response(jsonify({"message": "Email cannot be empty!"}), 400)
    MailingList.remove_email_adress(email)
    make_response(jsonify({"message": "Unsubscribed!"}), 200)



# TODO: Add admin role requirement
@bp.route("/api/newsletter/send", methods=["POST"])
def send_newsletter():
    """
    Sends a newsletter to all subscribers.

    Returns:
        A response object with a success message if the newsletter is sent successfully,
        or an error message if something goes wrong.
    """

    data = request.get_json()
    subject = data["subject"]
    body = data["body"]
    if subject == "":
        return make_response(jsonify({"message": "Subject cannot be empty!"}), 400)
    if body == "":
        return make_response(jsonify({"message": "Body cannot be empty!"}), 400)
    MailingList.send_email(subject, body)
    make_response(jsonify({"message": "Newsletter sent!"}), 200)


# TODO: Add admin role requirement
@bp.route("/api/newsletter/subscribers", methods=["GET"])
def get_subscribers():
    """
    Gets all subscribers.

    Returns:
        A response object with a list of all subscribers if the request is successful,
        or an error message if something goes wrong.
    """

    subscribers = MailingList.query.all()
    if subscribers is None:
        return make_response(jsonify({"message": "Subscribers not found!"}), 404)
    subscribers = [
        {
            "id": subscriber.id,
            "email": subscriber.email,
            "is_subscribed": subscriber.is_subscribed,
        }
        for subscriber in subscribers
    ]
    return make_response(jsonify({"subscribers": subscribers}), 200)

@