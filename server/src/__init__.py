from flask import Flask

from config import Config
from src.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    # Initialize Flask extensions here
    with app.app_context():
        db.create_all()
    # Register blueprints here
    from src.main import bp as main_bp

    app.register_blueprint(main_bp)

    @app.route("/test/")
    def test_page():
        return "<h1>Testing the Flask Application Factory Pattern</h1>"

    return app
