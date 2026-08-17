from ..extensions import db
from ..models import Ticket, TicketMessage, User


def get_ticket(ticket_id: int, user: User) -> Ticket | None:
    ticket = db.session.get(Ticket, ticket_id)
    return ticket if ticket and (user.role != "cliente" or ticket.owner_id == user.id) else None


def list_tickets(user: User) -> list[Ticket]:
    query = Ticket.query.order_by(Ticket.updated_at.desc())
    return query.filter_by(owner_id=user.id).all() if user.role == "cliente" else query.all()


def create_ticket(data: dict, user: User) -> Ticket:
    subject = str(data.get("subject", "")).strip()
    body = str(data.get("message", "")).strip()
    if not subject or not body:
        raise ValueError("Assunto e mensagem são obrigatórios.")
    owner_id = user.id if user.role == "cliente" else data.get("owner_id")
    owner = db.session.get(User, owner_id)
    if owner is None or owner.role != "cliente":
        raise ValueError("Informe um cliente válido para o ticket.")
    ticket = Ticket(owner_id=owner.id, subject=subject[:200], category=str(data.get("category", "Geral"))[:60], priority=str(data.get("priority", "Média"))[:20])
    ticket.messages.append(TicketMessage(author_id=user.id, body=body))
    db.session.add(ticket); db.session.commit()
    return ticket


def add_message(ticket: Ticket, body: str, user: User) -> TicketMessage:
    body = body.strip()
    if not body:
        raise ValueError("A mensagem não pode ficar vazia.")
    message = TicketMessage(ticket_id=ticket.id, author_id=user.id, body=body)
    ticket.status = "respondido" if user.role != "cliente" else "aberto"
    db.session.add(message); db.session.commit()
    return message


def update_status(ticket: Ticket, status: str) -> Ticket:
    if status not in {"aberto", "respondido", "resolvido"}:
        raise ValueError("Status de ticket inválido.")
    ticket.status = status; db.session.commit()
    return ticket
