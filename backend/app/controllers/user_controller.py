from flask import jsonify, request

from ..services.user_service import create_user, list_users


def create_new_user():
    try:
        user = create_user(request.get_json(silent=True) or {})
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(user=user.to_dict()), 201


def get_users():
    return jsonify(users=[user.to_dict() for user in list_users()])
