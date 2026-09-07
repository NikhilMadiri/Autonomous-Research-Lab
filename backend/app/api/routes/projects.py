from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response

from app.api.dependencies import get_project_service, get_question_service
from app.schemas.common import Page, SuccessResponse
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.question import QuestionCreate, QuestionRead
from app.services.project import ProjectService
from app.services.question import QuestionService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=SuccessResponse[Page[ProjectRead]])
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    sort: str = "created_at",
    service: ProjectService = Depends(get_project_service),  # noqa: B008
):
    items, total = await service.list(page, page_size, search, sort)
    return {
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    }


@router.post("", response_model=SuccessResponse[ProjectRead], status_code=201)
async def create_project(
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),  # noqa: B008
):
    return {"data": await service.create(data)}


@router.get("/{project_id}", response_model=SuccessResponse[ProjectRead])
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),  # noqa: B008
):
    return {"data": await service.get(project_id)}


@router.patch("/{project_id}", response_model=SuccessResponse[ProjectRead])
async def update_project(
    project_id: UUID,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),  # noqa: B008
):
    return {"data": await service.update(project_id, data)}


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),  # noqa: B008
):
    await service.delete(project_id)
    return Response(status_code=204)


@router.get("/{project_id}/questions", response_model=SuccessResponse[Page[QuestionRead]])
async def list_questions(
    project_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
    sort: str = "created_at",
    service: QuestionService = Depends(get_question_service),  # noqa: B008
):
    items, total = await service.list(project_id, page, page_size, search, status, sort)
    return {
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    }


@router.post(
    "/{project_id}/questions",
    response_model=SuccessResponse[QuestionRead],
    status_code=201,
)
async def create_question(
    project_id: UUID,
    data: QuestionCreate,
    service: QuestionService = Depends(get_question_service),  # noqa: B008
):
    return {"data": await service.create(project_id, data)}
