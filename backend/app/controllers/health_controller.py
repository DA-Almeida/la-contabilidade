from flask import jsonify

from ..services.health_service import get_health_status


def health_check():
    return jsonify(get_health_status())