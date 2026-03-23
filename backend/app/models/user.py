from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("student", "teacher", "admin", name="user_role"),
        nullable=False
    )
    real_name: Mapped[str] = mapped_column(String(50), nullable=False)
    student_no: Mapped[str | None] = mapped_column(String(30), unique=True)
    teacher_no: Mapped[str | None] = mapped_column(String(30), unique=True)
    college: Mapped[str | None] = mapped_column(String(100))
    major: Mapped[str | None] = mapped_column(String(100))
    grade: Mapped[str | None] = mapped_column(String(20))
    class_name: Mapped[str | None] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[int] = mapped_column(nullable=False, default=1)
    last_login_at: Mapped[DateTime | None] = mapped_column(DateTime)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    student_profile = relationship("StudentProfile", back_populates="user", uselist=False)
    warning_records = relationship("WarningRecord", back_populates="student")
    recommendation_records = relationship("RecommendationRecord", back_populates="student")
    chat_records = relationship("ChatRecord", back_populates="user")
