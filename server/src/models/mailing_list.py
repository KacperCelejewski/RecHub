from src.extensions import db
from src.extensions import mail


class MailingList(db.Model):
    __tablename__ = "mailing_list"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_subscribed = db.Column(db.Boolean, nullable=False, default=True)
    sender = db.Column(db.String(120), nullable=False, default="rechub@mailtrap.io")

    def __repr__(self) -> str:
        return f"Subscriber {self.email} is subscribed: {self.is_subscribed}"

    @staticmethod
    def add_email_adress(email):
        """
        Add a new email subscriber to the mailing list.

        Args:
            email (str): The email address of the subscriber.
            is_subscribed (bool): Whether the subscriber is subscribed or not.

        Returns:
            MailingList: The newly created subscriber object.
        """
        subscriber = MailingList(email=email)
        db.session.add(subscriber)
        db.session.commit()
        return subscriber

    def remove_subscriber(self):
        """
        Remove a subscriber from the mailing list.

        Returns:
            MailingList: The deleted subscriber object.
        """
        db.session.delete(self)
        db.session.commit()
        return self

    def unsubscribe(self):
        """
        Unsubscribe a subscriber from the mailing list.

        Returns:
            MailingList: The updated subscriber object.
        """
        self.is_subscribed = False
        db.session.commit()
        return self

    @staticmethod
    def send_email(subject, body):
        """
        Send an email to a subscriber.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.

        Returns:
            MailingList: The updated subscriber object.
        """
        subscribers = (MailingList.query.filter_by(is_subscribed=True).all(),)
        recepients = [subscriber.email for subscriber in subscribers]
        mail.send_message(
            subject,
            sender=MailingList.sender,
            body=body,
            recepients=recepients,
        )
