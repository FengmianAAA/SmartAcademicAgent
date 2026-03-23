from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.dashboard import RecommendationItem, StudentOverviewResponse, WarningItem
from app.services.dashboard_service import (
    get_student_overview,
    list_student_recommendations,
    list_student_warnings,
)

router = APIRouter()


@router.get("/overview", response_model=StudentOverviewResponse)
def overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> StudentOverviewResponse:
    return get_student_overview(db, current_user)


@router.get("/warnings", response_model=list[WarningItem])
def warnings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[WarningItem]:
    return list_student_warnings(db, current_user.id)


@router.get("/recommendations", response_model=list[RecommendationItem])
def recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[RecommendationItem]:
    return list_student_recommendations(db, current_user.id)
