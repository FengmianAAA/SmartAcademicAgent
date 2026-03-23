from pydantic import BaseModel, Field


class KnowledgeDocumentBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: str
    content: str = Field(min_length=1)
    source: str | None = None
    is_active: bool = True


class KnowledgeDocumentCreate(KnowledgeDocumentBase):
    pass


class KnowledgeDocumentUpdate(KnowledgeDocumentBase):
    embedding_status: str = "pending"


class KnowledgeDocumentResponse(BaseModel):
    id: int
    title: str
    category: str
    content: str
    source: str | None
    embedding_status: str
    is_active: bool
    created_by: int | None
    created_at: str
    updated_at: str


class KnowledgeSearchResponse(BaseModel):
    id: int
    title: str
    category: str
    snippet: str
    source: str | None
