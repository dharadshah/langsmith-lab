# scripts/run_evaluation.py
from langsmith import Client, evaluate

from app.config import export_langsmith_env
from app.constants.eval_data import DATASET_NAME
from app.services.agent_service import AgentService
from app.services.evaluators import correctness, relevance


def main() -> None:
    export_langsmith_env()
    service = AgentService()

    def target(inputs: dict) -> dict:
        answer = service.handle_question(inputs["question"])
        return {"answer": answer}

    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[correctness, relevance],
        experiment_prefix="qa-baseline",
    )

    print("Evaluation complete. View results in the LangSmith UI.")
    print(results)


if __name__ == "__main__":
    main()