# scripts/create_dataset.py
from langsmith import Client

from app.config import export_langsmith_env
from app.constants.eval_data import (
    DATASET_NAME,
    DATASET_DESCRIPTION,
    EVAL_EXAMPLES,
)


def main() -> None:
    export_langsmith_env()
    client = Client()

    if client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset '{DATASET_NAME}' already exists. Skipping creation.")
        return

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=DATASET_DESCRIPTION,
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"question": ex["question"]},
                "outputs": {
                    "expected_value": ex["expected_value"],
                    "reference_answer": ex["reference_answer"],
                },
            }
            for ex in EVAL_EXAMPLES
        ],
    )
    print(f"Created dataset '{DATASET_NAME}' with {len(EVAL_EXAMPLES)} examples.")


if __name__ == "__main__":
    main()