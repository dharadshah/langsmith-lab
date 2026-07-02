# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import export_langsmith_env
from app.routers import qa


@asynccontextmanager
async def lifespan(app: FastAPI):
    export_langsmith_env()
    yield


app = FastAPI(title="langsmith-lab", lifespan=lifespan)
app.include_router(qa.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}