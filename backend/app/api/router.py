from fastapi import APIRouter
from app.api.routes import projects, questions, system
router = APIRouter(); router.include_router(system.router); router.include_router(projects.router); router.include_router(questions.router)

