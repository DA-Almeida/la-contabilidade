from flask import Blueprint

from ..controllers.document_controller import download_document, get_documents, upload_document
from ..services.auth_service import require_auth


document_bp = Blueprint("documents", __name__, url_prefix="/api/documents")
document_bp.get("")(require_auth("admin", "colaborador", "cliente")(get_documents))
document_bp.post("")(require_auth("admin", "colaborador", "cliente")(upload_document))
document_bp.get("/<int:document_id>/download")(require_auth("admin", "colaborador", "cliente")(download_document))
