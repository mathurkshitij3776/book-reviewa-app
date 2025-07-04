# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from database import db
from flask_migrate import Migrate
from api import api
from config import *
from flasgger import swag_from
#from flask_graphql import GraphQL
#from schema import schema

#from fastapi import FastAPI
migrate = Migrate() 
app = None
def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Book Review API',
        'uiversion': 3,
        'description': 'A REST API for managing books and reviews',
        'version': '1.0.0'
    }
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_reviewdb.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    api.init_app(app)

    
    migrate.init_app(app, db) 
  
    return app

app = create_app()

if __name__ == "__main__":
    # On startup, create tables if they don’t exist yet
    with app.app_context():
        db.create_all()
    app.run(debug=True)
