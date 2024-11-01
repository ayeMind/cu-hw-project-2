from flask import Flask
from .routes import index_bp

def register_blueprints(app: Flask):
    app.register_blueprint(index_bp)