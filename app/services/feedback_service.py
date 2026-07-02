# app/services/feedback_service.py
from langsmith import Client

from app.config import export_langsmith_env
from app.constants.app_constants import (
    FeedbackKey,
    HELPFUL_SCORE,
    UNHELPFUL_SCORE,
)


class FeedbackService:
    """Writes user feedback to LangSmith for a given run."""

    def __init__(self) -> None:
        export_langsmith_env()
        self._client = Client()

    def record(self, run_id: str, helpful: bool, comment: str | None = None) -> None:
        score = HELPFUL_SCORE if helpful else UNHELPFUL_SCORE
        self._client.create_feedback(
            run_id=run_id,
            key=FeedbackKey.USER_SCORE,
            score=score,
            comment=comment,
        )