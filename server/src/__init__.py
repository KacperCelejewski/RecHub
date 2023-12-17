from flask import Flask
from flask_cors import CORS
from config import Config
from src.extensions import db, bcrypt, jwt
from src.models.company import Company
from src.models.user import User
from src.models.opinion import Opinion
from src.models.representative import Representative


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()


    from src.companies import bp_companies as company_bp
    from src.main import bp_main as main_bp
    from src.auth import bp_auth as auth_bp
    from src.opinions import bp_opinion as opinion_bp
    from src.representative import bp_representatives as representative_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(opinion_bp)
    app.register_blueprint(representative_bp)
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app
