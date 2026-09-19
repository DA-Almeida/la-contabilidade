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
def team_dashboard():
    return send_from_directory(PROJECT_ROOT, "portal/team/dashboard.html")


@public_bp.get("/portal/equipe/clientes")
@require_portal_access("admin", "colaborador")
def team_customers():
    return send_from_directory(PROJECT_ROOT, "portal/team/customers.html")


@public_bp.get("/portal/equipe/colaboradores")
@require_portal_access("admin", "colaborador")
def team_employees():
    return send_from_directory(PROJECT_ROOT, "portal/team/employees.html")


@public_bp.get("/portal/equipe/tarefas")
@require_portal_access("admin", "colaborador")
def team_tasks():
    return send_from_directory(PROJECT_ROOT, "portal/team/tasks.html")


@public_bp.get("/portal/equipe/atribuicoes")
@require_portal_access("admin", "colaborador")
def team_assignments():
    return send_from_directory(PROJECT_ROOT, "portal/team/assignments.html")


@public_bp.get("/portal/equipe/tickets")
@require_portal_access("admin", "colaborador")
def team_tickets():
    return send_from_directory(PROJECT_ROOT, "portal/team/tickets.html")


@public_bp.get("/portal/equipe/guias")
@require_portal_access("admin", "colaborador")
def team_guides():
    return send_from_directory(PROJECT_ROOT, "portal/team/guides.html")


@public_bp.get("/portal/equipe/obrigacoes")
@require_portal_access("admin", "colaborador")
def team_obligations():
    return send_from_directory(PROJECT_ROOT, "portal/team/obligations.html")


@public_bp.get("/portal/equipe/usuarios")
@require_portal_access("admin")
def team_users():
    return send_from_directory(PROJECT_ROOT, "portal/team/users.html")


@public_bp.get("/portal/cliente")
@require_portal_access("cliente")
def client_portal():
    return send_from_directory(PROJECT_ROOT, "portal-cliente.html")


@public_bp.get("/acesso/<path:filename>")
@public_bp.get("/portal/<path:filename>")
@public_bp.get("/<path:filename>")
def public_assets(filename: str):
    allowed_assets = {
        "style.css", "site.js", "leacont.jpeg", "portal.css", "portal.js", 
        "portal-admin.js", "portal-client.js", "portal/shared/layout.html",
        "portal/shared/sidebar.html", "portal/shared/navbar.html",
        "portal/team/dashboard.html", "portal/team/customers.html",
        "portal/team/employees.html", "portal/team/tasks.html",
        "portal/team/assignments.html", "portal/team/tickets.html",
        "portal/team/guides.html", "portal/team/obligations.html",
        "portal/team/users.html", "portal/team/modules.js",
    }
    if filename not in allowed_assets:
        return {"error": "Rota não encontrada."}, 404
    return send_from_directory(PROJECT_ROOT, filename)

