from flask import jsonify, request

from ..services.auth_service import authenticate, bootstrap_admin, create_access_token


def bootstrap():
    data = request.get_json(silent=True) or {}
    if not all(str(data.get(key, "")).strip() for key in ("name", "email", "password")):
        return jsonify(error="Nome, e-mail e senha são obrigatórios."), 400
    if len(data["password"]) < 8:
        return jsonify(error="A senha deve ter ao menos 8 caracteres."), 400
    try:
        user = bootstrap_admin(data)
    except ValueError as error:
        return jsonify(error=str(error)), 409
    response = jsonify(user=user.to_dict())
    response.set_cookie("access_token", create_access_token(user), httponly=True, samesite="Lax")
    return response, 201


def login():
    data = request.get_json(silent=True) or {}
    user = authenticate(str(data.get("email", "")), str(data.get("password", "")))
    if user is None:
        return jsonify(error="E-mail ou senha inválidos."), 401
    response = jsonify(user=user.to_dict())
    response.set_cookie("access_token", create_access_token(user), httponly=True, samesite="Lax")
    return response


def logout():
    response = jsonify(message="Sessão encerrada.")
    response.delete_cookie("access_token")
    return response


def current_user():
    from flask import g

    return jsonify(user=g.current_user.to_dict())
