from sqlalchemy import DateTime, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class MicroMajor(Base):
    __tablename__ = "micro_majors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    direction: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    required_credits: Mapped[float] = mapped_column(nullable=False, default=0)
    eligibility_rules: Mapped[str | None] = mapped_column(Text)
    status: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    recommendation_records = relationship(
        "RecommendationRecord",
        back_populates="related_micro_major"
    )


class RecommendationRecord(Base):
    __tablename__ = "recommendation_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    recommendation_type: Mapped[str] = mapped_column(
        Enum("course", "micro_major", "skill_path", name="recommendation_type"),
        nullable=False
    )
    target_direction: Mapped[str | None] = mapped_column(String(100))
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    related_micro_major_id: Mapped[int | None] = mapped_column(ForeignKey("micro_majors.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    student = relationship("User", back_populates="recommendation_records")
    related_micro_major = relationship("MicroMajor", back_populates="recommendation_records")
