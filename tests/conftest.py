# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.qa import get_agent_service, get_feedback_service


import os
os.environ["LANGSMITH_TRACING"] = "false"

class FakeAgentService:
    """Stand-in for AgentService that returns a canned answer, no LLM calls."""

    def __init__(self, answer: str = "Mocked answer: 42.") -> None:
        self._answer = answer
        self.received_question: str | None = None

    def handle_question(self, question: str, **kwargs) -> str:
        self.received_question = question
        return self._answer


@pytest.fixture
def fake_service() -> FakeAgentService:
    return FakeAgentService()


@pytest.fixture
def client(fake_service, fake_feedback_service):
    app.dependency_overrides[get_agent_service] = lambda: fake_service
    app.dependency_overrides[get_feedback_service] = lambda: fake_feedback_service
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

class FakeFeedbackService:
    """Records calls in memory instead of writing to LangSmith."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def record(self, run_id: str, helpful: bool, comment: str | None = None) -> None:
        self.calls.append({"run_id": run_id, "helpful": helpful, "comment": comment})


@pytest.fixture
def fake_feedback_service() -> FakeFeedbackService:
    return FakeFeedbackService()