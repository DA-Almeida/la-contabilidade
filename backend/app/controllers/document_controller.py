from io import BytesIO

from flask import g, jsonify, request, send_file

from ..models import User
from ..services.document_service import create_document, get_document_for_user, list_documents


def upload_document():
    owner = g.current_user
    if g.current_user.role != "cliente":
        owner_id = request.form.get("owner_id", type=int)
        owner = User.query.filter_by(id=owner_id, role="cliente").first() if owner_id else None
        if owner is None:
            return jsonify(error="Informe um cliente válido para o documento."), 400
    try:
        document = create_document(request.files.get("file"), owner, g.current_user, request.form.get("category", "Outros"))
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(document=document.to_dict()), 201


def get_documents():
    return jsonify(documents=[document.to_dict() for document in list_documents(g.current_user)])


def download_document(document_id: int):
    document = get_document_for_user(document_id, g.current_user)
    if document is None:
        return jsonify(error="Documento não encontrado."), 404
    return send_file(
        BytesIO(document.content),
        mimetype=document.content_type,
        as_attachment=True,
        download_name=document.original_filename,
    )
