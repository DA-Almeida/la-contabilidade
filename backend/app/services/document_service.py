from werkzeug.datastructures import FileStorage

from ..extensions import db
from ..models import Document, User

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "xml", "xlsx"}


def create_document(file: FileStorage, owner: User, uploaded_by: User, category: str = "Outros") -> Document:
    if not file or not file.filename:
        raise ValueError("Selecione um arquivo para enviar.")
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Formato não permitido. Envie PDF, JPG, PNG, XML ou XLSX.")
    content = file.read()
    if not content:
        raise ValueError("O arquivo enviado está vazio.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("O arquivo excede o limite de 10 MB.")
    document = Document(
        owner_id=owner.id,
        uploaded_by_id=uploaded_by.id,
        original_filename=file.filename[:255],
        content_type=file.mimetype or "application/octet-stream",
        size_bytes=len(content),
        category=(category or "Outros")[:50],
        direction="enviado" if uploaded_by.id == owner.id else "recebido",
        content=content,
    )
    db.session.add(document)
    db.session.commit()
    return document


def list_documents(user: User) -> list[Document]:
    query = Document.query.order_by(Document.created_at.desc())
    if user.role == "cliente":
        query = query.filter_by(owner_id=user.id)
    return query.all()


def get_document_for_user(document_id: int, user: User) -> Document | None:
    document = db.session.get(Document, document_id)
    if document is None or (user.role == "cliente" and document.owner_id != user.id):
        return None
    return document
