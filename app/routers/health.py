"""Health and meta endpoints."""
from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "llm": "stub" if settings.use_stub_llm else "live",
        "db": "sqlite" if settings.is_sqlite else "postgres",
    }
