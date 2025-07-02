# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from database import db
from api import *
app = None
def create_app():
    app = Flask(__name__)
    # load configuration
    
# Use SQLite, which will create a file named 'book_review.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviewdb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config.from_object("app.config.Config")

    # initialize database extension
    #app.app_context.push()
    db.init_app(app)
    api.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    # On startup, create tables if they don’t exist yet
    with app.app_context():
        db.create_all()
    app.run(debug=True)
