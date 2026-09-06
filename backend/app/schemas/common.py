from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):  # noqa: UP046
    success: bool = True
    data: T


class Page(BaseModel, Generic[T]):  # noqa: UP046
    items: list[T]
    total: int
    page: int
    page_size: int


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: list[dict] = Field(default_factory=list)
