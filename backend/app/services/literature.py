from datetime import UTC, datetime
from uuid import UUID

from app.core.exceptions import NotFoundException
from app.models.literature import Literature
from app.repositories.literature import LiteratureRepository
from app.repositories.question import QuestionRepository


class LiteratureService:
    def __init__(
        self,
        repo: LiteratureRepository,
        question_repo: QuestionRepository,
    ):
        self.repo = repo
        self.question_repo = question_repo

    async def _get_question(self, project_id: UUID, question_id: UUID):
        question = await self.question_repo.get(question_id)
        if not question or question.project_id != project_id:
            raise NotFoundException("Research question not found")
        return question

    async def list(
        self,
        project_id: UUID,
        question_id: UUID,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
    ):
        await self._get_question(project_id, question_id)
        return await self.repo.list(question_id, page, page_size, search, sort)

    async def get(self, literature_id: UUID):
        literature = await self.repo.get(literature_id)
        if not literature:
            raise NotFoundException("Literature not found")
        return literature

    async def create(
        self,
        project_id: UUID,
        question_id: UUID,
        data,
    ):
        await self._get_question(project_id, question_id)
        values = data.model_dump()
        if values["url"] is not None:
            values["url"] = str(values["url"])
        return await self.repo.create(Literature(question_id=question_id, **values))

    async def update(self, literature_id: UUID, data):
        literature = await self.get(literature_id)
        values = data.model_dump(exclude_unset=True)
        if values.get("url") is not None:
            values["url"] = str(values["url"])
        for key, value in values.items():
            setattr(literature, key, value)
        literature.updated_at = datetime.now(UTC)
        return await self.repo.update(literature)

    async def delete(self, literature_id: UUID):
        literature = await self.get(literature_id)
        literature.deleted_at = datetime.now(UTC)
        await self.repo.delete(literature)
