# scripts/demo_agent.py
from langchain_core.tracers.langchain import wait_for_all_tracers

from app.services.agent_service import AgentService


def main() -> None:
    service = AgentService()
    question = "What is   23 multiplied by 7,   plus 15?"
    answer = service.handle_question(
        question,
        langsmith_extra={"metadata": {"source": "demo_script", "user": "dhara"}},
    )
    print(f"Q: {question.strip()}")
    print(f"A: {answer}")
    wait_for_all_tracers()


if __name__ == "__main__":
    main()