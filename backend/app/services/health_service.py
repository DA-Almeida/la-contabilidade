from sqlalchemy import text

from ..extensions import db


def get_health_status() -> dict:
    db.session.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}