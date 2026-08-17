from flask import Blueprint

from ..controllers.auth_controller import bootstrap, current_user, login, logout
from ..services.auth_service import require_auth


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")
auth_bp.post("/bootstrap")(bootstrap)
auth_bp.post("/login")(login)
auth_bp.post("/logout")(logout)
auth_bp.get("/me")(require_auth()(current_user))
