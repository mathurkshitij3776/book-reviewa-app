# import pytest
# from flask import Flask
# from database import db
# from app import create_app
# import json

# from models import db, Book, Review
# from api import cache

# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['testing'] = True

# tests/conftest.py
import pytest
from app import create_app
from database import db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


