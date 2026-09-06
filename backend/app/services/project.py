from datetime import datetime, timezone
from uuid import UUID
from app.core.exceptions import NotFoundException
from app.models.project import Project
from app.repositories.project import ProjectRepository
class ProjectService:
    def __init__(self, repo: ProjectRepository): self.repo = repo
    async def list(self, page, page_size, search, sort): return await self.repo.list(page, page_size, search, sort)
    async def get(self, project_id: UUID):
        item = await self.repo.get(project_id)
        if not item: raise NotFoundException("Project not found")
        return item
    async def create(self, data): return await self.repo.add(Project(**data.model_dump()))
    async def update(self, project_id, data):
        item = await self.get(project_id)
        for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
        item.updated_at = datetime.now(timezone.utc); await self.repo.db.commit(); await self.repo.db.refresh(item); return item
    async def delete(self, project_id):
        item = await self.get(project_id); item.deleted_at = datetime.now(timezone.utc); await self.repo.db.commit()

