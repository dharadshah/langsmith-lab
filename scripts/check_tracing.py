# scripts/check_tracing.py
import os

from app.config import export_langsmith_env

export_langsmith_env()

print("LANGSMITH_TRACING =", os.environ.get("LANGSMITH_TRACING"))
print("LANGSMITH_PROJECT =", os.environ.get("LANGSMITH_PROJECT"))
key = os.environ.get("LANGSMITH_API_KEY", "")
print("LANGSMITH_API_KEY =", (key[:12] + "...") if key else "MISSING")

from langsmith import Client

client = Client()
print("Connected. Recent projects visible to this key:")
for project in client.list_projects(limit=5):
    print(" -", project.name)