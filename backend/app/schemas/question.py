from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.research_question import QuestionStatus


class QuestionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    description: str | None = None
    status: QuestionStatus = QuestionStatus.OPEN


class QuestionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=240)
    description: str | None = None
    status: QuestionStatus | None = None


class QuestionRead(QuestionCreate):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
