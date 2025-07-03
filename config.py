# config.py

import os

# Project ke base directory ka path nikalta hai.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration, isse baaki classes settings inherit karengi."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Aapke local machine par development ke liye settings."""
    DEBUG = True
    # Yeh aapke project folder mein 'book_review_dev.db' naam ki file banayega.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'book_review_dev.db')

class TestingConfig(Config):
    """Pytest ke liye settings."""
    TESTING = True
    # Yeh sabse zaroori hai: Yeh database file nahi banata, balki memory mein banata hai.
    # Isse aapke tests bahut fast hote hain aur aapki asli DB file ko nahi chhedte.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 
    
class ProductionConfig(Config):
    """Jab aapka app live jaayega, uske liye settings (future ke liye)."""
    DEBUG = False
    TESTING = False
    # Yahan asli database (jaise PostgreSQL ya MySQL) ka URL aayega.
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')