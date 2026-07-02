# app/services/evaluators.py
import json

from langchain_groq import ChatGroq

from app.config import settings
from app.constants.app_constants import MODEL_NAME
from app.constants.prompts import JUDGE_RELEVANCE_PROMPT


def correctness(outputs: dict, reference_outputs: dict) -> dict:
    """Heuristic: does the agent's answer contain the expected numeric value?"""
    answer = str(outputs.get("answer", ""))
    expected = str(reference_outputs.get("expected_value", ""))
    score = 1.0 if expected and expected in answer else 0.0
    return {"key": "correctness", "score": score}

def relevance(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    """LLM-as-judge: is the answer relevant and correct for the question?"""
    judge = ChatGroq(model=MODEL_NAME, temperature=0.0, api_key=settings.groq_api_key)

    prompt = JUDGE_RELEVANCE_PROMPT.format(
        question=inputs.get("question", ""),
        answer=outputs.get("answer", ""),
        reference=reference_outputs.get("reference_answer", ""),
    )
    response = judge.invoke(prompt)

    try:
        parsed = json.loads(response.content)
        score = float(parsed.get("score", 0.0))
        reasoning = parsed.get("reasoning", "")
    except (json.JSONDecodeError, ValueError, TypeError):
        score = 0.0
        reasoning = "Could not parse judge response."

    return {"key": "relevance", "score": score, "comment": reasoning}