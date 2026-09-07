from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.repositories.literature import LiteratureRepository
from app.repositories.project import ProjectRepository
from app.repositories.question import QuestionRepository
from app.services.literature import LiteratureService
from app.services.project import ProjectService
from app.services.question import QuestionService


def get_project_service(
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    return ProjectService(ProjectRepository(db))


def get_question_service(
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    return QuestionService(QuestionRepository(db))


def get_literature_service(
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    return LiteratureService(
        LiteratureRepository(db),
        QuestionRepository(db),
    )
