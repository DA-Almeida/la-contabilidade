from flask import Flask

from .health_routes import health_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp)