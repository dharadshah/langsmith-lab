# app/schemas/qa.py
from pydantic import BaseModel, Field

from app.constants.app_constants import MAX_QUESTION_LENGTH


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_QUESTION_LENGTH)


class AskResponse(BaseModel):
    answer: str
    run_id: str