from ..extensions import db
from ..models import User
from .auth_service import VALID_ROLES


def create_user(data: dict) -> User:
    required_fields = ("name", "email", "password", "role")
    missing = [field for field in required_fields if not str(data.get(field, "")).strip()]
    if missing:
        raise ValueError("Campos obrigatórios: " + ", ".join(missing) + ".")
    if data["role"] not in VALID_ROLES:
        raise ValueError("Perfil inválido.")
    if len(data["password"]) < 8:
        raise ValueError("A senha deve ter ao menos 8 caracteres.")
    email = data["email"].strip().lower()
    if User.query.filter_by(email=email).first():
        raise ValueError("Já existe um usuário com este e-mail.")

    user = User(name=data["name"].strip(), email=email, role=data["role"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user


def list_users() -> list[User]:
    return User.query.order_by(User.name).all()
