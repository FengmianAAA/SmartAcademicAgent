from fastapi import APIRouter

from app.api.v1.endpoints import academic, admin, assistant, auth, dashboard, health, knowledge

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(academic.router, prefix="/academic", tags=["academic"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
