from flask import Flask
from flask_cors import CORS
from config import Config
from src.extensions import db, bcrypt, jwt, mail
from src.models.company import Company
from src.models.user import User
from src.models.opinion import Opinion
from src.models.representative import Representative
from src.models.mailing_list import MailingList


config_class = Config
application = Flask(__name__)
application.config.from_object(config_class)

bcrypt.init_app(application)
db.init_app(application)
jwt.init_app(application)
mail.init_app(application)

with application.app_context():
    db.create_all()

from src.companies import bp_companies as company_bp
from src.main import bp_main as main_bp
from src.auth import bp_auth as auth_bp
from src.opinions import bp_opinion as opinion_bp
from src.representative import bp_representatives as representative_bp
from src.newsletter import bp_newsletter as newsletter_bp

application.register_blueprint(main_bp)
application.register_blueprint(company_bp)
application.register_blueprint(auth_bp)
application.register_blueprint(opinion_bp)
application.register_blueprint(representative_bp)
application.register_blueprint(newsletter_bp)

CORS(application, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    application.run(host="0.0.0.0")
