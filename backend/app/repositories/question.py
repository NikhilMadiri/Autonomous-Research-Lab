from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.research_question import ResearchQuestion
class QuestionRepository:
    def __init__(self, db: AsyncSession): self.db = db
    async def list(self, project_id: UUID, page: int, page_size: int):
        base = select(ResearchQuestion).where(ResearchQuestion.project_id == project_id, ResearchQuestion.deleted_at.is_(None))
        items = list((await self.db.scalars(base.order_by(ResearchQuestion.created_at.desc()).offset((page - 1) * page_size).limit(page_size))).all())
        total = await self.db.scalar(select(func.count()).select_from(ResearchQuestion).where(ResearchQuestion.project_id == project_id, ResearchQuestion.deleted_at.is_(None)))
        return items, int(total or 0)
    async def get(self, question_id: UUID):
        return await self.db.scalar(select(ResearchQuestion).where(ResearchQuestion.id == question_id, ResearchQuestion.deleted_at.is_(None)))
    async def add(self, question: ResearchQuestion):
        self.db.add(question); await self.db.commit(); await self.db.refresh(question); return question

