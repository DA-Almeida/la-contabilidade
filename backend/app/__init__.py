from pathlib import Path
from flask import Flask

from .config import get_config
from .extensions import cors, db
from .routes import register_blueprints
from .services.migration_service import ensure_database_schema


def create_app() -> Flask:
    # Define static folder path
    static_folder = Path(__file__).resolve().parent.parent / "static"
    
    app = Flask(__name__, static_folder=str(static_folder), static_url_path="/static")
    app.config.from_object(get_config())

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    register_blueprints(app)

    with app.app_context():
        ensure_database_schema()

    return app
