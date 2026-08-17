from datetime import UTC, datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, g, jsonify, redirect, request

from ..extensions import db
from ..models import User

VALID_ROLES = {"admin", "colaborador", "cliente"}


def create_access_token(user: User) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(hours=current_app.config["JWT_EXPIRATION_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def get_authenticated_user() -> User | None:
    authorization = request.headers.get("Authorization", "")
    token = authorization.removeprefix("Bearer ") if authorization.startswith("Bearer ") else request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return db.session.get(User, int(payload["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        return None


def require_auth(*roles: str):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = get_authenticated_user()
            if user is None:
                return jsonify(error="Token de acesso inválido ou expirado."), 401
            if roles and user.role not in roles:
                return jsonify(error="Você não tem permissão para esta ação."), 403
            g.current_user = user
            return view(*args, **kwargs)

        return wrapped

    return decorator


def require_portal_access(*roles: str):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = get_authenticated_user()
            if user is None or user.role not in roles:
                login_path = "/acesso/cliente" if roles == ("cliente",) else "/acesso/equipe"
                return redirect(login_path)
            g.current_user = user
            return view(*args, **kwargs)

        return wrapped

    return decorator


def bootstrap_admin(data: dict) -> User:
    if User.query.first() is not None:
        raise ValueError("A configuração inicial já foi concluída.")
    role = "admin"
    user = User(name=data["name"].strip(), email=data["email"].strip().lower(), role=role)
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email: str, password: str) -> User | None:
    user = User.query.filter_by(email=email.strip().lower()).first()
    return user if user and user.check_password(password) else None
