from pydantic import BaseModel


class StudentOverviewResponse(BaseModel):
    user_id: int
    real_name: str
    major: str | None
    grade: str | None
    target_career: str | None
    earned_credits: float
    total_credits_required: float
    mandatory_credits_earned: float
    elective_credits_earned: float
    failed_course_count: int
    gpa: float
    risk_level: str


class WarningItem(BaseModel):
    id: int
    warning_type: str
    warning_level: str
    reason: str
    suggestion: str | None
    status: str
    triggered_at: str


class RecommendationItem(BaseModel):
    id: int
    recommendation_type: str
    target_direction: str | None
    reason: str | None
    content_json: dict
    created_at: str
