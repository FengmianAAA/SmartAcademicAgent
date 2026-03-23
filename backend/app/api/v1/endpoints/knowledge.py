from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_current_user, get_db
from app.models.user import User
from app.schemas.knowledge import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentResponse,
    KnowledgeDocumentUpdate,
    KnowledgeSearchResponse,
)
from app.services.knowledge_service import (
    create_document,
    delete_document,
    list_documents,
    search_documents,
    update_document,
)

router = APIRouter()


@router.get("/documents", response_model=list[KnowledgeDocumentResponse])
def documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[KnowledgeDocumentResponse]:
    return list_documents(db)


@router.post("/documents", response_model=KnowledgeDocumentResponse, status_code=status.HTTP_201_CREATED)
def create(
    payload: KnowledgeDocumentCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
) -> KnowledgeDocumentResponse:
    return create_document(db, payload, current_user)


@router.put("/documents/{document_id}", response_model=KnowledgeDocumentResponse)
def update(
    document_id: int,
    payload: KnowledgeDocumentUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
) -> KnowledgeDocumentResponse:
    result = update_document(db, document_id, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return result


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(
    document_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
) -> None:
    ok = delete_document(db, document_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Document not found")


@router.get("/search", response_model=list[KnowledgeSearchResponse])
def search(
    q: str = Query(min_length=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[KnowledgeSearchResponse]:
    return search_documents(db, q)
