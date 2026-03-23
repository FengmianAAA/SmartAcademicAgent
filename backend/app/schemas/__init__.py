from app.schemas.academic import GradeItem, ProgramRequirementItem, ScheduleItem, TrainingProgramDetailResponse
from app.schemas.admin import (
    AdminOverviewResponse,
    WarningRecordResponse,
    WarningRecordUpdate,
    WarningRuleCreate,
    WarningRuleResponse,
    WarningRuleUpdate,
)
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.chat import ChatAskRequest, ChatAskResponse, ChatHistoryItem
from app.schemas.dashboard import RecommendationItem, StudentOverviewResponse, WarningItem
from app.schemas.knowledge import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentResponse,
    KnowledgeDocumentUpdate,
    KnowledgeSearchResponse,
)
from app.schemas.user import CurrentUserResponse

__all__ = [
    "AdminOverviewResponse",
    "ChatAskRequest",
    "ChatAskResponse",
    "ChatHistoryItem",
    "CurrentUserResponse",
    "GradeItem",
    "KnowledgeDocumentCreate",
    "KnowledgeDocumentResponse",
    "KnowledgeDocumentUpdate",
    "KnowledgeSearchResponse",
    "LoginRequest",
    "ProgramRequirementItem",
    "RecommendationItem",
    "ScheduleItem",
    "StudentOverviewResponse",
    "TokenResponse",
    "TrainingProgramDetailResponse",
    "WarningItem",
    "WarningRecordResponse",
    "WarningRecordUpdate",
    "WarningRuleCreate",
    "WarningRuleResponse",
    "WarningRuleUpdate",
]
