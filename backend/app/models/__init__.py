from app.models.chat import ChatRecord
from app.models.course import Course, CourseOffering, Enrollment, ProgramCourseRequirement
from app.models.knowledge import KnowledgeDocument
from app.models.recommendation import MicroMajor, RecommendationRecord
from app.models.student_profile import StudentProfile
from app.models.training_program import TrainingProgram
from app.models.user import User
from app.models.warning import WarningRecord, WarningRule

__all__ = [
    "ChatRecord",
    "Course",
    "CourseOffering",
    "Enrollment",
    "KnowledgeDocument",
    "MicroMajor",
    "ProgramCourseRequirement",
    "RecommendationRecord",
    "StudentProfile",
    "TrainingProgram",
    "User",
    "WarningRecord",
    "WarningRule",
]
