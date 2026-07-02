# app/constants/eval_data.py

DATASET_NAME = "langsmith-lab-qa"
DATASET_DESCRIPTION = "Arithmetic and factual Q&A pairs for evaluating the agent."

# Each example: the question, the expected final numeric answer (as a string
# fragment we expect to see in the response), and a reference answer for the judge.
EVAL_EXAMPLES = [
    {
        "question": "What is 23 multiplied by 7, plus 15?",
        "expected_value": "176",
        "reference_answer": "The result is 176.",
    },
    {
        "question": "What is 45 divided by 9, then times 6?",
        "expected_value": "30",
        "reference_answer": "The result is 30.",
    },
    {
        "question": "What is 19 times 3?",
        "expected_value": "57",
        "reference_answer": "The result is 57.",
    },
    {
        "question": "What is 100 minus 37, then divided by 9?",
        "expected_value": "7",
        "reference_answer": "The result is 7.",
    },
    {
        "question": "What is 2 to the power of 10?",
        "expected_value": "1024",
        "reference_answer": "The result is 1024.",
    },
    {
        "question": "What is 144 divided by 12?",
        "expected_value": "12",
        "reference_answer": "The result is 12.",
    },
    {
        "question": "What is 8 times 9, minus 20?",
        "expected_value": "52",
        "reference_answer": "The result is 52.",
    },
    {
        "question": "What is 250 plus 375?",
        "expected_value": "625",
        "reference_answer": "The result is 625.",
    },
]