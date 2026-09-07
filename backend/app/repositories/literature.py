from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.literature import Literature


class LiteratureRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(
        self,
        question_id: UUID,
        page: int,
        page_size: int,
        search: str | None,
        sort: str,
    ):
        query = select(Literature).where(
            Literature.question_id == question_id,
            Literature.deleted_at.is_(None),
        )
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                or_(
                    Literature.title.ilike(search_filter),
                    Literature.authors.ilike(search_filter),
                    Literature.journal.ilike(search_filter),
                )
            )

        sort_column = {
            "title": Literature.title,
            "year": Literature.year,
            "created_at": Literature.created_at,
        }.get(sort, Literature.created_at)
        query = query.order_by(sort_column.desc()).offset((page - 1) * page_size).limit(page_size)
        items = list((await self.db.scalars(query)).all())

        count_query = (
            select(func.count())
            .select_from(Literature)
            .where(
                Literature.question_id == question_id,
                Literature.deleted_at.is_(None),
            )
        )
        if search:
            count_query = count_query.where(
                or_(
                    Literature.title.ilike(search_filter),
                    Literature.authors.ilike(search_filter),
                    Literature.journal.ilike(search_filter),
                )
            )
        total = await self.db.scalar(count_query)
        return items, int(total or 0)

    async def get(self, literature_id: UUID):
        return await self.db.scalar(
            select(Literature).where(
                Literature.id == literature_id,
                Literature.deleted_at.is_(None),
            )
        )

    async def create(self, literature: Literature):
        self.db.add(literature)
        await self.db.commit()
        await self.db.refresh(literature)
        return literature

    async def update(self, literature: Literature):
        await self.db.commit()
        await self.db.refresh(literature)
        return literature

    async def delete(self, literature: Literature):
        await self.db.commit()
