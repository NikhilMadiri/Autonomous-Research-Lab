from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.repositories.project import ProjectRepository
from app.repositories.question import QuestionRepository
from app.services.project import ProjectService
from app.services.question import QuestionService
def get_project_service(db: AsyncSession = Depends(get_db)): return ProjectService(ProjectRepository(db))
def get_question_service(db: AsyncSession = Depends(get_db)): return QuestionService(QuestionRepository(db))

