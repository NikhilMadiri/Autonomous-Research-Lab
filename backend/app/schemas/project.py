from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.project import ProjectStatus


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str | None = None
    status: ProjectStatus = ProjectStatus.DRAFT


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectRead(ProjectCreate):
    id: UUID
    owner_id: UUID | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
