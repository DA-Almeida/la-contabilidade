from ..extensions import db
from ..models import Lead

REQUIRED_FIELDS = ("name", "email", "phone", "company_type")


def create_lead(data: dict) -> Lead:
    missing = [field for field in REQUIRED_FIELDS if not str(data.get(field, "")).strip()]
    if missing:
        raise ValueError("Campos obrigatórios: " + ", ".join(missing) + ".")
    lead = Lead(
        name=data["name"].strip(),
        email=data["email"].strip().lower(),
        phone=data["phone"].strip(),
        company_type=data["company_type"].strip(),
        message=str(data.get("message", "")).strip() or None,
    )
    db.session.add(lead)
    db.session.commit()
    return lead


def list_leads() -> list[Lead]:
    return Lead.query.order_by(Lead.created_at.desc()).all()
