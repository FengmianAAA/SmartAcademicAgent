from sqlalchemy import DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class WarningRule(Base):
    __tablename__ = "warning_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rule_name: Mapped[str] = mapped_column(nullable=False)
    warning_type: Mapped[str] = mapped_column(
        Enum(
            "credit_shortage",
            "failed_courses",
            "mandatory_missing",
            "graduation_risk",
            "retake_risk",
            name="warning_type"
        ),
        nullable=False
    )
    warning_level: Mapped[str] = mapped_column(
        Enum("low", "medium", "high", name="warning_level"),
        nullable=False
    )
    rule_expression: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[int] = mapped_column(nullable=False, default=1)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    warning_records = relationship("WarningRecord", back_populates="rule")


class WarningRecord(Base):
    __tablename__ = "warning_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rule_id: Mapped[int | None] = mapped_column(ForeignKey("warning_rules.id"))
    warning_type: Mapped[str] = mapped_column(
        Enum(
            "credit_shortage",
            "failed_courses",
            "mandatory_missing",
            "graduation_risk",
            "retake_risk",
            name="warning_type_record"
        ),
        nullable=False
    )
    warning_level: Mapped[str] = mapped_column(
        Enum("low", "medium", "high", name="warning_level_record"),
        nullable=False
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    suggestion: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        Enum("new", "viewed", "resolved", name="warning_status"),
        nullable=False,
        default="new"
    )
    triggered_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    student = relationship("User", back_populates="warning_records")
    rule = relationship("WarningRule", back_populates="warning_records")
