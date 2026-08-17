from sqlalchemy import inspect

from ..extensions import db
from ..models import User


def ensure_database_schema() -> None:
    engine = db.engine
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    required_tables = {User.__tablename__}

    if not required_tables.issubset(existing_tables):
        db.create_all()