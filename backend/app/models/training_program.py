from sqlalchemy import DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class TrainingProgram(Base):
    __tablename__ = "training_programs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    major: Mapped[str] = mapped_column(String(100), nullable=False)
    grade: Mapped[str] = mapped_column(String(20), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    required_total_credits: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False)
    required_mandatory_credits: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False)
    required_elective_credits: Mapped[float] = mapped_column(Numeric(5, 1), nullable=False)
    graduation_requirements: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    student_profiles = relationship("StudentProfile", back_populates="training_program")
