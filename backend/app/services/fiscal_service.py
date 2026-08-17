from datetime import date
from decimal import Decimal, InvalidOperation

from ..extensions import db
from ..models import FiscalObligation, TaxGuide, User


def _owner(data: dict) -> User:
    owner = db.session.get(User, data.get("owner_id"))
    if owner is None or owner.role != "cliente":
        raise ValueError("Informe um cliente válido.")
    return owner


def _date(value: str) -> date:
    try: return date.fromisoformat(value)
    except (TypeError, ValueError): raise ValueError("Informe uma data válida.")


def list_guides(user: User) -> list[TaxGuide]:
    query = TaxGuide.query.order_by(TaxGuide.due_date)
    return query.filter_by(owner_id=user.id).all() if user.role == "cliente" else query.all()


def create_guide(data: dict) -> TaxGuide:
    title, competence = str(data.get("title", "")).strip(), str(data.get("competence", "")).strip()
    if not title or not competence: raise ValueError("Título e competência são obrigatórios.")
    try: amount = Decimal(str(data.get("amount")))
    except (InvalidOperation, ValueError): raise ValueError("Informe um valor válido.")
    guide = TaxGuide(owner_id=_owner(data).id, title=title[:160], competence=competence[:20], due_date=_date(data.get("due_date")), amount=amount, status=str(data.get("status", "pendente"))[:30])
    db.session.add(guide); db.session.commit(); return guide


def list_obligations(user: User) -> list[FiscalObligation]:
    query = FiscalObligation.query.order_by(FiscalObligation.due_date)
    return query.filter_by(owner_id=user.id).all() if user.role == "cliente" else query.all()


def create_obligation(data: dict) -> FiscalObligation:
    title, competence = str(data.get("title", "")).strip(), str(data.get("competence", "")).strip()
    if not title or not competence: raise ValueError("Título e competência são obrigatórios.")
    obligation = FiscalObligation(owner_id=_owner(data).id, title=title[:160], description=str(data.get("description", "")).strip() or None, competence=competence[:20], due_date=_date(data.get("due_date")), status=str(data.get("status", "pendente"))[:30])
    db.session.add(obligation); db.session.commit(); return obligation
