from pydantic import BaseModel, Field


class ChatAskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class ChatAskResponse(BaseModel):
    question: str
    answer: str
    intent: str
    source_json: dict | None
    response_time_ms: int | None
    created_at: str | None = None


class ChatHistoryItem(BaseModel):
    id: int
    question: str
    answer: str
    intent: str | None
    source_json: dict | None
    response_time_ms: int | None
    created_at: str
