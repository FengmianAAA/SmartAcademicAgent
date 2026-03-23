from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.chat import ChatAskRequest, ChatAskResponse, ChatHistoryItem
from app.services.assistant_service import ask_academic_assistant, list_chat_history

router = APIRouter()


@router.get("/history", response_model=list[ChatHistoryItem])
def history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[ChatHistoryItem]:
    return list_chat_history(db, current_user.id)


@router.post("/ask", response_model=ChatAskResponse)
def ask(
    payload: ChatAskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ChatAskResponse:
    return ask_academic_assistant(db, current_user, payload.question)
