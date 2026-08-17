from datetime import datetime

from ..extensions import db


class TaxGuide(db.Model):
    __tablename__ = "tax_guides"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    competence = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="pendente")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owner = db.relationship("User", foreign_keys=[owner_id])

    def to_dict(self) -> dict:
        return {"id": self.id, "owner_id": self.owner_id, "title": self.title, "competence": self.competence, "due_date": self.due_date.isoformat(), "amount": float(self.amount), "status": self.status, "created_at": self.created_at.isoformat()}


class FiscalObligation(db.Model):
    __tablename__ = "fiscal_obligations"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=True)
    competence = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="pendente")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owner = db.relationship("User", foreign_keys=[owner_id])

    def to_dict(self) -> dict:
        return {"id": self.id, "owner_id": self.owner_id, "title": self.title, "description": self.description, "competence": self.competence, "due_date": self.due_date.isoformat(), "status": self.status, "created_at": self.created_at.isoformat()}
