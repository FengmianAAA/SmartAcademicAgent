from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.session import Base, engine
from app.models import (
    ChatRecord,
    Course,
    CourseOffering,
    Enrollment,
    MicroMajor,
    ProgramCourseRequirement,
    RecommendationRecord,
    StudentProfile,
    TrainingProgram,
    User,
    WarningRecord,
    WarningRule,
)

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="智慧教务系统与智能体平台后端服务"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "smart academic backend is running"}
