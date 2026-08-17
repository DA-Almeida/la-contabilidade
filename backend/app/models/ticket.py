from datetime import datetime

from ..extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(60), nullable=False, default="Geral")
    priority = db.Column(db.String(20), nullable=False, default="Média")
    status = db.Column(db.String(30), nullable=False, default="aberto")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = db.relationship("User", foreign_keys=[owner_id])
    messages = db.relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan", order_by="TicketMessage.created_at")

    def to_dict(self, include_messages: bool = False) -> dict:
        data = {"id": self.id, "owner_id": self.owner_id, "subject": self.subject, "category": self.category, "priority": self.priority, "status": self.status, "created_at": self.created_at.isoformat(), "updated_at": self.updated_at.isoformat()}
        if include_messages:
            data["messages"] = [message.to_dict() for message in self.messages]
        return data


class TicketMessage(db.Model):
    __tablename__ = "ticket_messages"

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ticket = db.relationship("Ticket", back_populates="messages")
    author = db.relationship("User", foreign_keys=[author_id])

    def to_dict(self) -> dict:
        return {"id": self.id, "author_id": self.author_id, "author_name": self.author.name, "body": self.body, "created_at": self.created_at.isoformat()}
