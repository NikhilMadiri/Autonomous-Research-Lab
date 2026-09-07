from datetime import UTC, datetime

from app.core.exceptions import NotFoundException
from app.models.research_question import ResearchQuestion
from app.repositories.question import QuestionRepository


class QuestionService:
    def __init__(self, repo: QuestionRepository):
        self.repo = repo

    async def list(self, project_id, page, page_size, search=None, status=None, sort="created_at"):
        return await self.repo.list(project_id, page, page_size, search, status, sort)

    async def get(self, question_id):
        item = await self.repo.get(question_id)
        if not item:
            raise NotFoundException("Research question not found")
        return item

    async def create(self, project_id, data):
        return await self.repo.add(ResearchQuestion(project_id=project_id, **data.model_dump()))

    async def update(self, question_id, data):
        item = await self.get(question_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)
        item.updated_at = datetime.now(UTC)
        await self.repo.db.commit()
        await self.repo.db.refresh(item)
        return item

    async def delete(self, question_id):
        item = await self.get(question_id)
        item.deleted_at = datetime.now(UTC)
        await self.repo.db.commit()
