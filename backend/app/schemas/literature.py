from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.models.literature import LiteratureStatus


def validate_literature_year(value: int | None) -> int | None:
    if value is None:
        return value

    current_year = datetime.now().year
    if value > current_year:
        raise ValueError("Year must not exceed the current year")
    return value


class LiteratureCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    authors: str | None = Field(default=None, max_length=1000)
    year: int | None = Field(default=None, ge=1900)
    journal: str | None = Field(default=None, max_length=500)
    doi: str | None = Field(default=None, max_length=255)
    url: HttpUrl | None = None
    abstract: str | None = None
    notes: str | None = None
    citation: str | None = None
    status: LiteratureStatus = LiteratureStatus.NOT_REVIEWED

    _validate_year = field_validator("year")(validate_literature_year)


class LiteratureUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    authors: str | None = Field(default=None, max_length=1000)
    year: int | None = Field(default=None, ge=1900)
    journal: str | None = Field(default=None, max_length=500)
    doi: str | None = Field(default=None, max_length=255)
    url: HttpUrl | None = None
    abstract: str | None = None
    notes: str | None = None
    citation: str | None = None
    status: LiteratureStatus | None = None

    _validate_year = field_validator("year")(validate_literature_year)


class LiteratureRead(LiteratureCreate):
    id: UUID
    question_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
