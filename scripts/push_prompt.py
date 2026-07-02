# scripts/push_prompt.py
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

from app.config import export_langsmith_env
from app.constants.prompts import QA_AGENT_SYSTEM_PROMPT

PROMPT_HUB_NAME = "langsmith-lab-qa-system"


def main() -> None:
    export_langsmith_env()
    client = Client()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", QA_AGENT_SYSTEM_PROMPT),
            ("placeholder", "{messages}"),
        ]
    )

    url = client.push_prompt(PROMPT_HUB_NAME, object=prompt)
    print(f"Pushed prompt '{PROMPT_HUB_NAME}'.")
    print(f"View/edit it at: {url}")


if __name__ == "__main__":
    main()