# scripts/demo_agent.py
from app.services.agent_service import AgentService


def main() -> None:
    service = AgentService()
    question = "What is 23 multiplied by 7, plus 15?"
    answer = service.ask(question)
    print(f"Q: {question}")
    print(f"A: {answer}")


if __name__ == "__main__":
    main()