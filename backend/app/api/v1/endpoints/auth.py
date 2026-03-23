from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import CurrentUserResponse
from app.services.auth_service import login_with_password

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    return login_with_password(db, payload.username, payload.password)


@router.get("/me", response_model=CurrentUserResponse)
def me(current_user: User = Depends(get_current_user)) -> CurrentUserResponse:
    return CurrentUserResponse(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role,
        real_name=current_user.real_name,
        student_no=current_user.student_no,
        teacher_no=current_user.teacher_no,
        college=current_user.college,
        major=current_user.major,
        grade=current_user.grade,
        class_name=current_user.class_name
    )
