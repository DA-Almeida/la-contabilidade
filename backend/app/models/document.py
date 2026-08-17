from datetime import datetime

from ..extensions import db


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    content_type = db.Column(db.String(120), nullable=False)
    size_bytes = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False, default="Outros")
    direction = db.Column(db.String(20), nullable=False, default="enviado")
    status = db.Column(db.String(30), nullable=False, default="recebido")
    content = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owner = db.relationship("User", foreign_keys=[owner_id])
    uploaded_by = db.relationship("User", foreign_keys=[uploaded_by_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "original_filename": self.original_filename,
            "content_type": self.content_type,
            "size_bytes": self.size_bytes,
            "category": self.category,
            "direction": self.direction,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }
