from app.services.academic_service import (
    get_training_program_detail,
    list_student_grades,
    list_student_schedule,
)
from app.services.assistant_service import ask_academic_assistant, list_chat_history
from app.services.auth_service import login_with_password
from app.services.dashboard_service import (
    get_student_overview,
    list_student_recommendations,
    list_student_warnings,
)
from app.services.knowledge_service import (
    create_document,
    delete_document,
    list_documents,
    search_documents,
    update_document,
)

__all__ = [
    "ask_academic_assistant",
    "create_document",
    "delete_document",
    "get_student_overview",
    "get_training_program_detail",
    "list_chat_history",
    "list_documents",
    "list_student_grades",
    "list_student_recommendations",
    "list_student_schedule",
    "list_student_warnings",
    "login_with_password",
    "search_documents",
    "update_document",
]
