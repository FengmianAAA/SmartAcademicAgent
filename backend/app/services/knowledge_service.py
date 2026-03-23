from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeDocument
from app.models.user import User
from app.schemas.knowledge import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentResponse,
    KnowledgeDocumentUpdate,
    KnowledgeSearchResponse,
)


def _to_response(item: KnowledgeDocument) -> KnowledgeDocumentResponse:
    return KnowledgeDocumentResponse(
        id=item.id,
        title=item.title,
        category=item.category,
        content=item.content,
        source=item.source,
        embedding_status=item.embedding_status,
        is_active=bool(item.is_active),
        created_by=item.created_by,
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat(),
    )


def list_documents(db: Session) -> list[KnowledgeDocumentResponse]:
    records = db.query(KnowledgeDocument).order_by(KnowledgeDocument.updated_at.desc()).all()
    return [_to_response(item) for item in records]


def create_document(db: Session, payload: KnowledgeDocumentCreate, user: User) -> KnowledgeDocumentResponse:
    item = KnowledgeDocument(
        title=payload.title,
        category=payload.category,
        content=payload.content,
        source=payload.source,
        is_active=1 if payload.is_active else 0,
        embedding_status="pending",
        created_by=user.id,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_response(item)


def update_document(db: Session, document_id: int, payload: KnowledgeDocumentUpdate) -> KnowledgeDocumentResponse | None:
    item = db.get(KnowledgeDocument, document_id)
    if item is None:
        return None

    item.title = payload.title
    item.category = payload.category
    item.content = payload.content
    item.source = payload.source
    item.is_active = 1 if payload.is_active else 0
    item.embedding_status = payload.embedding_status
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_response(item)


def delete_document(db: Session, document_id: int) -> bool:
    item = db.get(KnowledgeDocument, document_id)
    if item is None:
        return False
    db.delete(item)
    db.commit()
    return True


def search_documents(db: Session, query: str, limit: int = 5) -> list[KnowledgeSearchResponse]:
    keyword = f"%{query}%"
    rows = (
        db.query(KnowledgeDocument)
        .filter(KnowledgeDocument.is_active == 1)
        .filter(or_(KnowledgeDocument.title.like(keyword), KnowledgeDocument.content.like(keyword)))
        .order_by(KnowledgeDocument.updated_at.desc())
        .limit(limit)
        .all()
    )
    results: list[KnowledgeSearchResponse] = []
    for item in rows:
        snippet = item.content[:120] + ("..." if len(item.content) > 120 else "")
        results.append(
            KnowledgeSearchResponse(
                id=item.id,
                title=item.title,
                category=item.category,
                snippet=snippet,
                source=item.source,
            )
        )
    return results
