from uuid import UUID
from fastapi import APIRouter, Depends, Response
from app.api.dependencies import get_question_service
from app.schemas.common import SuccessResponse
from app.schemas.question import QuestionRead, QuestionUpdate
from app.services.question import QuestionService
router = APIRouter(prefix="/questions", tags=["questions"])
@router.get("/{question_id}", response_model=SuccessResponse[QuestionRead])
async def get_question(question_id: UUID, service: QuestionService = Depends(get_question_service)): return {"data": await service.get(question_id)}
@router.patch("/{question_id}", response_model=SuccessResponse[QuestionRead])
async def update_question(question_id: UUID, data: QuestionUpdate, service: QuestionService = Depends(get_question_service)): return {"data": await service.update(question_id, data)}
@router.delete("/{question_id}", status_code=204)
async def delete_question(question_id: UUID, service: QuestionService = Depends(get_question_service)): await service.delete(question_id); return Response(status_code=204)

