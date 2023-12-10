import pytest
from flask import Flask
from src import create_app
from flask_sqlalchemy import SQLAlchemy
from src.extensions import db
@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    
    return app.test_client()
