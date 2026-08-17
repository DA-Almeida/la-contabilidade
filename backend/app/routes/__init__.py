from flask import Flask

from .auth_routes import auth_bp
from .document_routes import document_bp
from .fiscal_routes import fiscal_bp
from .health_routes import health_bp
from .lead_routes import lead_bp
from .public_routes import public_bp
from .ticket_routes import ticket_bp
from .user_routes import user_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(fiscal_bp)
    app.register_blueprint(lead_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(user_bp)
