# This file makes the directory a Python package 
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Just for development
    
    # Register routes directly from app.py
    from . import app as routes
    app.register_blueprint(routes.bp)
    
    return app 