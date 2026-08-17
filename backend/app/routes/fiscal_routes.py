from flask import Blueprint

from ..controllers.fiscal_controller import create_new_guide, create_new_obligation, get_guides, get_obligations
from ..services.auth_service import require_auth

fiscal_bp = Blueprint("fiscal", __name__, url_prefix="/api")
fiscal_bp.get("/guides")(require_auth("admin", "colaborador", "cliente")(get_guides))
fiscal_bp.post("/guides")(require_auth("admin", "colaborador")(create_new_guide))
fiscal_bp.get("/fiscal-obligations")(require_auth("admin", "colaborador", "cliente")(get_obligations))
fiscal_bp.post("/fiscal-obligations")(require_auth("admin", "colaborador")(create_new_obligation))
