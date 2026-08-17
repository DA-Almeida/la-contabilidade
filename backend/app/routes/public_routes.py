from pathlib import Path

from flask import Blueprint, send_from_directory

from ..services.auth_service import require_portal_access


PROJECT_ROOT = Path(__file__).resolve().parents[3]
public_bp = Blueprint("public", __name__)


@public_bp.get("/")
def home():
    return send_from_directory(PROJECT_ROOT, "index.html")


@public_bp.get("/acesso/equipe")
def team_access():
    return send_from_directory(PROJECT_ROOT, "portal-admin.html")


@public_bp.get("/acesso/cliente")
def client_access():
    return send_from_directory(PROJECT_ROOT, "portal-cliente.html")


@public_bp.get("/portal/equipe")
@require_portal_access("admin", "colaborador")
def team_portal():
    return send_from_directory(PROJECT_ROOT, "portal-admin.html")


@public_bp.get("/portal/cliente")
@require_portal_access("cliente")
def client_portal():
    return send_from_directory(PROJECT_ROOT, "portal-cliente.html")


@public_bp.get("/<path:filename>")
def public_assets(filename: str):
    allowed_assets = {
        "style.css", "site.js", "leacont.jpeg", "portal.css", "portal.js",
    }
    if filename not in allowed_assets:
        return {"error": "Rota não encontrada."}, 404
    return send_from_directory(PROJECT_ROOT, filename)
