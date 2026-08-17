from flask import Blueprint

from ..controllers.lead_controller import create_public_lead, get_leads
from ..services.auth_service import require_auth


lead_bp = Blueprint("leads", __name__, url_prefix="/api/leads")
lead_bp.post("")(create_public_lead)
lead_bp.get("")(require_auth("admin", "colaborador")(get_leads))
