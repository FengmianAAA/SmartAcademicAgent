from sqlalchemy.orm import Session

from app.models.course import Course, CourseOffering, Enrollment, ProgramCourseRequirement
from app.models.student_profile import StudentProfile
from app.models.training_program import TrainingProgram
from app.schemas.academic import (
    GradeItem,
    ProgramRequirementItem,
    ScheduleItem,
    TrainingProgramDetailResponse,
)


def list_student_grades(db: Session, user_id: int) -> list[GradeItem]:
    rows = (
        db.query(Enrollment, CourseOffering, Course)
        .join(CourseOffering, Enrollment.offering_id == CourseOffering.id)
        .join(Course, CourseOffering.course_id == Course.id)
        .filter(Enrollment.student_id == user_id)
        .order_by(Enrollment.semester.desc(), Course.course_code.asc())
        .all()
    )
    return [
        GradeItem(
            semester=enrollment.semester,
            course_code=course.course_code,
            course_name=course.course_name,
            course_type=course.course_type,
            credit=float(course.credit),
            score=float(enrollment.score) if enrollment.score is not None else None,
            gpa_point=float(enrollment.gpa_point) if enrollment.gpa_point is not None else None,
            is_passed=bool(enrollment.is_passed),
            is_retake=bool(enrollment.is_retake),
            teacher_name=offering.teacher_name,
        )
        for enrollment, offering, course in rows
    ]


def list_student_schedule(db: Session, user_id: int, semester: str | None = None) -> list[ScheduleItem]:
    query = (
        db.query(Enrollment, CourseOffering, Course)
        .join(CourseOffering, Enrollment.offering_id == CourseOffering.id)
        .join(Course, CourseOffering.course_id == Course.id)
        .filter(Enrollment.student_id == user_id)
    )
    if semester:
        query = query.filter(Enrollment.semester == semester)
    rows = query.order_by(Enrollment.semester.desc(), CourseOffering.weekday.asc(), CourseOffering.start_section.asc()).all()
    return [
        ScheduleItem(
            semester=enrollment.semester,
            course_code=course.course_code,
            course_name=course.course_name,
            teacher_name=offering.teacher_name,
            weekday=offering.weekday,
            start_section=offering.start_section,
            end_section=offering.end_section,
            location=offering.location,
            credit=float(course.credit),
        )
        for enrollment, offering, course in rows
    ]


def get_training_program_detail(db: Session, user_id: int) -> TrainingProgramDetailResponse | None:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    if profile is None:
        return None

    program = db.get(TrainingProgram, profile.training_program_id)
    if program is None:
        return None

    rows = (
        db.query(ProgramCourseRequirement, Course)
        .join(Course, ProgramCourseRequirement.course_id == Course.id)
        .filter(ProgramCourseRequirement.training_program_id == program.id)
        .order_by(ProgramCourseRequirement.requirement_type.asc(), ProgramCourseRequirement.recommended_semester.asc(), Course.course_code.asc())
        .all()
    )
    requirements = [
        ProgramRequirementItem(
            requirement_type=req.requirement_type,
            is_required=bool(req.is_required),
            recommended_semester=req.recommended_semester,
            course_code=course.course_code,
            course_name=course.course_name,
            credit=float(course.credit),
        )
        for req, course in rows
    ]
    return TrainingProgramDetailResponse(
        program_id=program.id,
        major=program.major,
        grade=program.grade,
        version=program.version,
        required_total_credits=float(program.required_total_credits),
        required_mandatory_credits=float(program.required_mandatory_credits),
        required_elective_credits=float(program.required_elective_credits),
        graduation_requirements=program.graduation_requirements,
        requirements=requirements,
    )
