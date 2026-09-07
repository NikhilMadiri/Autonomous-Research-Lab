from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.research_question import ResearchQuestion


class QuestionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        project_id: UUID,
        page: int,
        page_size: int,
        search=None,
        status=None,
        sort="created_at",
    ):
        base = select(ResearchQuestion).where(
            ResearchQuestion.project_id == project_id,
            ResearchQuestion.deleted_at.is_(None),
        )
        if search:
            base = base.where(ResearchQuestion.title.ilike(f"%{search}%"))
        if status:
            base = base.where(ResearchQuestion.status == status)
        sort_column = {
            "title": ResearchQuestion.title,
            "status": ResearchQuestion.status,
            "created_at": ResearchQuestion.created_at,
        }.get(sort, ResearchQuestion.created_at)
        query = (
            base.order_by(sort_column.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        items = list((await self.db.scalars(query)).all())
        count_query = select(func.count()).select_from(ResearchQuestion).where(
            ResearchQuestion.project_id == project_id,
            ResearchQuestion.deleted_at.is_(None),
        )
        if search:
            count_query = count_query.where(ResearchQuestion.title.ilike(f"%{search}%"))
        if status:
            count_query = count_query.where(ResearchQuestion.status == status)
        total = await self.db.scalar(count_query)
        return items, int(total or 0)

    async def get(self, question_id: UUID):
        return await self.db.scalar(
            select(ResearchQuestion).where(
                ResearchQuestion.id == question_id,
                ResearchQuestion.deleted_at.is_(None),
            )
        )

    async def add(self, question: ResearchQuestion):
        self.db.add(question)
        await self.db.commit()
        await self.db.refresh(question)
        return question
