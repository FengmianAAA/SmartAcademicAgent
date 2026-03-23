from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.academic import GradeItem, ScheduleItem, TrainingProgramDetailResponse
from app.services.academic_service import (
    get_training_program_detail,
    list_student_grades,
    list_student_schedule,
)

router = APIRouter()


@router.get("/grades", response_model=list[GradeItem])
def grades(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[GradeItem]:
    return list_student_grades(db, current_user.id)


@router.get("/schedule", response_model=list[ScheduleItem])
def schedule(
    semester: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[ScheduleItem]:
    return list_student_schedule(db, current_user.id, semester)


@router.get("/training-program", response_model=TrainingProgramDetailResponse)
def training_program(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TrainingProgramDetailResponse:
    detail = get_training_program_detail(db, current_user.id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Training program not found")
    return detail
