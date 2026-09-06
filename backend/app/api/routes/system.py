from fastapi import APIRouter
from app.core.config import settings
router = APIRouter(tags=["system"])
@router.get("/health")
async def health(): return {"success": True, "data": {"status": "ok"}}
@router.get("/version")
async def version(): return {"success": True, "data": {"name": settings.app_name, "version": settings.app_version, "environment": settings.app_env}}

