from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False)
    course_type: Mapped[str] = mapped_column(
        Enum("mandatory", "elective", "public", "practice", "micro_major", name="course_type"),
        nullable=False
    )
    credit: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False)
    hours: Mapped[int] = mapped_column(nullable=False, default=0)
    assessment_method: Mapped[str | None] = mapped_column(String(50))
    college: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    offerings = relationship("CourseOffering", back_populates="course")
    requirements = relationship("ProgramCourseRequirement", back_populates="course")


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    semester: Mapped[str] = mapped_column(String(20), nullable=False)
    teacher_name: Mapped[str] = mapped_column(String(50), nullable=False)
    weekday: Mapped[int | None]
    start_section: Mapped[int | None]
    end_section: Mapped[int | None]
    location: Mapped[str | None] = mapped_column(String(100))
    capacity: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    course = relationship("Course", back_populates="offerings")
    enrollments = relationship("Enrollment", back_populates="offering")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    offering_id: Mapped[int] = mapped_column(ForeignKey("course_offerings.id"), nullable=False)
    semester: Mapped[str] = mapped_column(String(20), nullable=False)
    score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    gpa_point: Mapped[float | None] = mapped_column(Numeric(3, 2))
    is_passed: Mapped[int] = mapped_column(nullable=False, default=0)
    is_retake: Mapped[int] = mapped_column(nullable=False, default=0)
    remark: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    offering = relationship("CourseOffering", back_populates="enrollments")


class ProgramCourseRequirement(Base):
    __tablename__ = "program_course_requirements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    training_program_id: Mapped[int] = mapped_column(ForeignKey("training_programs.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    requirement_type: Mapped[str] = mapped_column(
        Enum("mandatory", "elective", "public", "practice", name="requirement_type"),
        nullable=False
    )
    min_credit: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False, default=0)
    recommended_semester: Mapped[str | None] = mapped_column(String(20))
    is_required: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    course = relationship("Course", back_populates="requirements")
