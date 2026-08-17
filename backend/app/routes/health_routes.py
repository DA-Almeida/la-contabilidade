from flask import Blueprint

from ..controllers import health_check


health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_route():
    return health_check()