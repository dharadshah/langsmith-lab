# app/routers/qa.py
import uuid

from fastapi import APIRouter, HTTPException

from app.schemas.qa import AskRequest, AskResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/qa", tags=["qa"])

_service = AgentService()


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest) -> AskResponse:
    run_id = str(uuid.uuid4())
    try:
        answer = _service.handle_question(
            payload.question,
            langsmith_extra={
                "run_id": run_id,
                "metadata": {"source": "api", "endpoint": "/qa/ask"},
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AskResponse(answer=answer, run_id=run_id)