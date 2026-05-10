"""Main FastAPI application"""

from fastapi import FastAPI
from app.api import chat, models, embeddings, keys, usage, providers
from app.providers.init import init_providers

app = FastAPI(title="AI Gateway", version="1.0.0")

# Initialize providers on startup
init_providers()

app.include_router(chat.router)
app.include_router(models.router)
app.include_router(embeddings.router)
app.include_router(keys.router)
app.include_router(usage.router)
app.include_router(providers.router)


@app.get("/health")
def health():
    return {"status": "ok"}
