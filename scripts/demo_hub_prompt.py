# scripts/demo_hub_prompt.py
from langsmith import Client

from app.config import export_langsmith_env
from app.constants.app_constants import PROMPT_HUB_NAME


def main() -> None:
    export_langsmith_env()
    client = Client()

    prompt = client.pull_prompt(PROMPT_HUB_NAME)
    print(f"Pulled prompt '{PROMPT_HUB_NAME}' from the Hub:")
    print("-" * 60)
    for message in prompt.messages:
        print(f"[{message.__class__.__name__}]")
        template = getattr(getattr(message, "prompt", None), "template", None)
        if template:
            print(template)
    print("-" * 60)


if __name__ == "__main__":
    main()