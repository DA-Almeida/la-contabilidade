from flask import Blueprint

from ..controllers.ticket_controller import change_ticket_status, create_new_ticket, create_ticket_message, get_ticket_detail, get_tickets
from ..services.auth_service import require_auth

ticket_bp = Blueprint("tickets", __name__, url_prefix="/api/tickets")
ticket_bp.get("")(require_auth("admin", "colaborador", "cliente")(get_tickets))
ticket_bp.post("")(require_auth("admin", "colaborador", "cliente")(create_new_ticket))
ticket_bp.get("/<int:ticket_id>")(require_auth("admin", "colaborador", "cliente")(get_ticket_detail))
ticket_bp.post("/<int:ticket_id>/messages")(require_auth("admin", "colaborador", "cliente")(create_ticket_message))
ticket_bp.patch("/<int:ticket_id>/status")(require_auth("admin", "colaborador")(change_ticket_status))
