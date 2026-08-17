from datetime import datetime

from ..extensions import db


class Lead(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False)
    company_type = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(50), nullable=False, default="site")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company_type": self.company_type,
            "message": self.message,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
        }
