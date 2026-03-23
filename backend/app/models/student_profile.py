from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    training_program_id: Mapped[int] = mapped_column(
        ForeignKey("training_programs.id"),
        nullable=False
    )
    target_career: Mapped[str | None] = mapped_column(String(100))
    total_credits_required: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False, default=0)
    earned_credits: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False, default=0)
    mandatory_credits_earned: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False, default=0)
    elective_credits_earned: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False, default=0)
    failed_course_count: Mapped[int] = mapped_column(nullable=False, default=0)
    gpa: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False, default=0)
    risk_level: Mapped[str] = mapped_column(
        Enum("low", "medium", "high", name="risk_level"),
        nullable=False,
        default="low"
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="student_profile")
    training_program = relationship("TrainingProgram", back_populates="student_profiles")
