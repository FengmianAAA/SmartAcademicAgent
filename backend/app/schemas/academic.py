from pydantic import BaseModel


class GradeItem(BaseModel):
    semester: str
    course_code: str
    course_name: str
    course_type: str
    credit: float
    score: float | None
    gpa_point: float | None
    is_passed: bool
    is_retake: bool
    teacher_name: str


class ScheduleItem(BaseModel):
    semester: str
    course_code: str
    course_name: str
    teacher_name: str
    weekday: int | None
    start_section: int | None
    end_section: int | None
    location: str | None
    credit: float


class ProgramRequirementItem(BaseModel):
    requirement_type: str
    is_required: bool
    recommended_semester: str | None
    course_code: str
    course_name: str
    credit: float


class TrainingProgramDetailResponse(BaseModel):
    program_id: int
    major: str
    grade: str
    version: str
    required_total_credits: float
    required_mandatory_credits: float
    required_elective_credits: float
    graduation_requirements: str | None
    requirements: list[ProgramRequirementItem]
