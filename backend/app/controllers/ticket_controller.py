from flask import g, jsonify, request

from ..services.ticket_service import add_message, create_ticket, get_ticket, list_tickets, update_status


def get_tickets(): return jsonify(tickets=[ticket.to_dict() for ticket in list_tickets(g.current_user)])

def create_new_ticket():
    try: ticket = create_ticket(request.get_json(silent=True) or {}, g.current_user)
    except ValueError as error: return jsonify(error=str(error)), 400
    return jsonify(ticket=ticket.to_dict(include_messages=True)), 201

def get_ticket_detail(ticket_id: int):
    ticket = get_ticket(ticket_id, g.current_user)
    return (jsonify(error="Ticket não encontrado."), 404) if ticket is None else jsonify(ticket=ticket.to_dict(include_messages=True))

def create_ticket_message(ticket_id: int):
    ticket = get_ticket(ticket_id, g.current_user)
    if ticket is None: return jsonify(error="Ticket não encontrado."), 404
    try: message = add_message(ticket, str((request.get_json(silent=True) or {}).get("message", "")), g.current_user)
    except ValueError as error: return jsonify(error=str(error)), 400
    return jsonify(message=message.to_dict()) , 201

def change_ticket_status(ticket_id: int):
    ticket = get_ticket(ticket_id, g.current_user)
    if ticket is None: return jsonify(error="Ticket não encontrado."), 404
    if g.current_user.role == "cliente": return jsonify(error="Apenas a equipe pode alterar o status."), 403
    try: update_status(ticket, str((request.get_json(silent=True) or {}).get("status", "")))
    except ValueError as error: return jsonify(error=str(error)), 400
    return jsonify(ticket=ticket.to_dict())
