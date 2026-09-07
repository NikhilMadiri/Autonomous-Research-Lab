from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, page: int, page_size: int, search: str | None, sort: str):
        query = select(Project).where(Project.deleted_at.is_(None))
        if search:
            query = query.where(Project.name.ilike(f"%{search}%"))
        sort_column = getattr(Project, sort, Project.created_at)
        query = query.order_by(sort_column.desc()).offset((page - 1) * page_size).limit(page_size)
        items = list((await self.db.scalars(query)).all())
        count_query = select(func.count()).select_from(Project).where(Project.deleted_at.is_(None))
        if search:
            count_query = count_query.where(Project.name.ilike(f"%{search}%"))
        total = await self.db.scalar(count_query)
        return items, int(total or 0)

    async def get(self, project_id: UUID):
        return await self.db.scalar(
            select(Project).where(
                Project.id == project_id,
                Project.deleted_at.is_(None),
            )
        )

    async def add(self, project: Project):
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project
