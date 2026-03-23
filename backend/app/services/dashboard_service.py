from sqlalchemy.orm import Session

from app.models.recommendation import RecommendationRecord
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.models.warning import WarningRecord
from app.schemas.dashboard import RecommendationItem, StudentOverviewResponse, WarningItem


def get_student_overview(db: Session, user: User) -> StudentOverviewResponse:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if profile is None:
        return StudentOverviewResponse(
            user_id=user.id,
            real_name=user.real_name,
            major=user.major,
            grade=user.grade,
            target_career=None,
            earned_credits=0,
            total_credits_required=0,
            mandatory_credits_earned=0,
            elective_credits_earned=0,
            failed_course_count=0,
            gpa=0,
            risk_level="low"
        )

    return StudentOverviewResponse(
        user_id=user.id,
        real_name=user.real_name,
        major=user.major,
        grade=user.grade,
        target_career=profile.target_career,
        earned_credits=float(profile.earned_credits),
        total_credits_required=float(profile.total_credits_required),
        mandatory_credits_earned=float(profile.mandatory_credits_earned),
        elective_credits_earned=float(profile.elective_credits_earned),
        failed_course_count=profile.failed_course_count,
        gpa=float(profile.gpa),
        risk_level=profile.risk_level
    )


def list_student_warnings(db: Session, user_id: int) -> list[WarningItem]:
    records = (
        db.query(WarningRecord)
        .filter(WarningRecord.student_id == user_id)
        .order_by(WarningRecord.triggered_at.desc())
        .limit(10)
        .all()
    )
    return [
        WarningItem(
            id=record.id,
            warning_type=record.warning_type,
            warning_level=record.warning_level,
            reason=record.reason,
            suggestion=record.suggestion,
            status=record.status,
            triggered_at=record.triggered_at.isoformat()
        )
        for record in records
    ]


def list_student_recommendations(db: Session, user_id: int) -> list[RecommendationItem]:
    records = (
        db.query(RecommendationRecord)
        .filter(RecommendationRecord.student_id == user_id)
        .order_by(RecommendationRecord.created_at.desc())
        .limit(10)
        .all()
    )
    return [
        RecommendationItem(
            id=record.id,
            recommendation_type=record.recommendation_type,
            target_direction=record.target_direction,
            reason=record.reason,
            content_json=record.content_json,
            created_at=record.created_at.isoformat()
        )
        for record in records
    ]
