from sqlalchemy import inspect

from ..extensions import db
from ..models import Customer, CustomerAssignment, Document, EmployeeProfile, FiscalObligation, Lead, Task, TaskTransition, TaxGuide, Ticket, TicketMessage, User


def ensure_database_schema() -> None:
    engine = db.engine
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    required_tables = {User.__tablename__, Lead.__tablename__, Document.__tablename__, Ticket.__tablename__, TicketMessage.__tablename__, TaxGuide.__tablename__, FiscalObligation.__tablename__, Customer.__tablename__, EmployeeProfile.__tablename__, CustomerAssignment.__tablename__, Task.__tablename__, TaskTransition.__tablename__}

    if not required_tables.issubset(existing_tables):
        db.create_all()
