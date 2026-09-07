from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response

from app.api.dependencies import get_literature_service
from app.schemas.common import Page, SuccessResponse
from app.schemas.literature import LiteratureCreate, LiteratureRead, LiteratureUpdate
from app.services.literature import LiteratureService

router = APIRouter(tags=["literature"])


@router.get(
    "/projects/{project_id}/questions/{question_id}/literature",
    response_model=SuccessResponse[Page[LiteratureRead]],
)
async def list_literature(
    project_id: UUID,
    question_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    sort: Literal["title", "year", "created_at"] = "created_at",
    service: LiteratureService = Depends(get_literature_service),  # noqa: B008
):
    items, total = await service.list(
        project_id,
        question_id,
        page,
        page_size,
        search,
        sort,
    )
    return {
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    }


@router.post(
    "/projects/{project_id}/questions/{question_id}/literature",
    response_model=SuccessResponse[LiteratureRead],
    status_code=201,
)
async def create_literature(
    project_id: UUID,
    question_id: UUID,
    data: LiteratureCreate,
    service: LiteratureService = Depends(get_literature_service),  # noqa: B008
):
    literature = await service.create(project_id, question_id, data)
    return {"data": literature}


@router.get(
    "/literature/{literature_id}",
    response_model=SuccessResponse[LiteratureRead],
)
async def get_literature(
    literature_id: UUID,
    service: LiteratureService = Depends(get_literature_service),  # noqa: B008
):
    return {"data": await service.get(literature_id)}


@router.patch(
    "/literature/{literature_id}",
    response_model=SuccessResponse[LiteratureRead],
)
async def update_literature(
    literature_id: UUID,
    data: LiteratureUpdate,
    service: LiteratureService = Depends(get_literature_service),  # noqa: B008
):
    return {"data": await service.update(literature_id, data)}


@router.delete("/literature/{literature_id}", status_code=204)
async def delete_literature(
    literature_id: UUID,
    service: LiteratureService = Depends(get_literature_service),  # noqa: B008
):
    await service.delete(literature_id)
    return Response(status_code=204)
