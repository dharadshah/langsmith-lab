# app/config.py
import os

from pydantic_settings import BaseSettings

def export_langsmith_env() -> None:
    """Push LangSmith settings into the process environment for LangChain tracing."""
    os.environ.setdefault("LANGSMITH_TRACING", str(settings.langsmith_tracing).lower())
    os.environ.setdefault("LANGSMITH_API_KEY", settings.langsmith_api_key)
    os.environ.setdefault("LANGSMITH_PROJECT", settings.langsmith_project)

class Settings(BaseSettings):
    langsmith_tracing: bool = True
    langsmith_api_key: str
    langsmith_project: str = "langsmith-lab"
    groq_api_key: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()