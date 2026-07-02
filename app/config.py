# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    langsmith_tracing: bool = True
    langsmith_api_key: str
    langsmith_project: str = "langsmith-lab"
    groq_api_key: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()