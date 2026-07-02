# app/routers/qa.py
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.qa import AskRequest, AskResponse
from app.services.agent_service import AgentService
from app.schemas.qa import (
    AskRequest,
    AskResponse,
    FeedbackRequest,
    FeedbackResponse,
)
from app.services.feedback_service import FeedbackService
from app.constants.messages import FEEDBACK_RECORDED, FEEDBACK_FAILED

router = APIRouter(prefix="/qa", tags=["qa"])

_service: AgentService | None = None


def get_agent_service() -> AgentService:
    """Provide a singleton AgentService. Overridable in tests."""
    global _service
    if _service is None:
        _service = AgentService()
    return _service

_feedback_service: FeedbackService | None = None


def get_feedback_service() -> FeedbackService:
    """Provide a singleton FeedbackService. Overridable in tests."""
    global _feedback_service
    if _feedback_service is None:
        _feedback_service = FeedbackService()
    return _feedback_service

@router.post("/ask", response_model=AskResponse)
def ask_question(
    payload: AskRequest,
    service: AgentService = Depends(get_agent_service),
) -> AskResponse:
    run_id = str(uuid.uuid4())
    try:
        answer = service.handle_question(
            payload.question,
            langsmith_extra={
                "run_id": run_id,
                "metadata": {"source": "api", "endpoint": "/qa/ask"},
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AskResponse(answer=answer, run_id=run_id)

@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(
    payload: FeedbackRequest,
    service: FeedbackService = Depends(get_feedback_service),
) -> FeedbackResponse:
    try:
        service.record(
            run_id=payload.run_id,
            helpful=payload.helpful,
            comment=payload.comment,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=FEEDBACK_FAILED.format(run_id=payload.run_id),
        ) from exc

    return FeedbackResponse(message=FEEDBACK_RECORDED)