# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from database import db
from flask_migrate import Migrate
from api import *
from config import *
#from fastapi import FastAPI
migrate = Migrate() 
app = None
def create_app():
    app = Flask(__name__)
    # load configuration
    # app.config.from_object(config_class)
# Use SQLite, which will create a file named 'book_review.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviewdb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config.from_object("app.config.Config")
    migrate.init_app(app, db) 
    # initialize database extension
    #app.app_context.push()
    db.init_app(app)
    api.init_app(app)

    return app

app = create_app()

#app = FastAPI()  # FastAPI auto‑generates /docs for you

# @app.get("/books")
# def list_books():
#     return [{"id": 1, "title": "Dune"}]

if __name__ == "__main__":
    # On startup, create tables if they don’t exist yet
    with app.app_context():
        db.create_all()
    app.run(debug=True)
