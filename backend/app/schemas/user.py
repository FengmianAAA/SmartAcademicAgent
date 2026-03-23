from pydantic import BaseModel


class CurrentUserResponse(BaseModel):
    id: int
    username: str
    role: str
    real_name: str
    student_no: str | None
    teacher_no: str | None
    college: str | None
    major: str | None
    grade: str | None
    class_name: str | None
