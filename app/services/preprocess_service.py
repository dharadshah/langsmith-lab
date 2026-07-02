# app/services/preprocess_service.py
import re

from langsmith import traceable

from app.constants.app_constants import MAX_QUESTION_LENGTH
from app.constants.messages import EMPTY_QUESTION, QUESTION_TOO_LONG


@traceable(run_type="tool", name="preprocess_question")
def preprocess_question(question: str) -> str:
    """Clean and validate an incoming question before it reaches the agent."""
    cleaned = re.sub(r"\s+", " ", question).strip()

    if not cleaned:
        raise ValueError(EMPTY_QUESTION)
    if len(cleaned) > MAX_QUESTION_LENGTH:
        raise ValueError(QUESTION_TOO_LONG.format(max_length=MAX_QUESTION_LENGTH))

    return cleaned