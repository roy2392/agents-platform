"""Health check endpoint."""
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "azure_ai_foundry": bool(settings.azure_ai_foundry_project_connection_string),
            "azure_openai": bool(settings.azure_openai_endpoint),
            "cosmos_db": bool(settings.cosmos_db_endpoint),
            "content_safety": bool(settings.azure_content_safety_endpoint),
        },
    }
