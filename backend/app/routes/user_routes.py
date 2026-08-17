from flask import Blueprint

from ..controllers.user_controller import create_new_user, get_users
from ..services.auth_service import require_auth


user_bp = Blueprint("users", __name__, url_prefix="/api/users")
user_bp.get("")(require_auth("admin")(get_users))
user_bp.post("")(require_auth("admin")(create_new_user))
