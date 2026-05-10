"""Mistral AI provider (custom adapter)"""

import json
from typing import AsyncGenerator, Any
import httpx
from app.providers.base import BaseProvider, ChatMessage


class MistralProvider(BaseProvider):
    """Mistral AI provider."""

    name = "mistral"
    supports_streaming = True
    supports_embeddings = False

    BASE_URL = "https://api.mistral.ai/v1"

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if not self._client:
            self._client = httpx.AsyncClient(
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                base_url=self.BASE_URL,
                timeout=60.0,
            )
        return self._client

    async def chat_completions(
        self,
        messages: list[ChatMessage],
        model: str = "mistral-large-latest",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs,
    ) -> dict[str, Any]:
        client = self._get_client()

        response = await client.post(
            "/chat/completions",
            json={
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs,
            },
        )
        response.raise_for_status()
        return response.json()

    async def chat_completions_stream(
        self, messages: list[ChatMessage], model: str = "mistral-large-latest", **kwargs
    ) -> AsyncGenerator[str, None]:
        client = self._get_client()

        async with client.stream(
            "POST",
            "/chat/completions",
            json={
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "stream": True,
                **kwargs,
            },
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    yield line + "\n\n"
        yield "data: [DONE]\n\n"

    async def embeddings(self, input: str | list[str], model: str) -> list[list[float]]:
        raise NotImplementedError("Use NVIDIA for Mistral embeddings")

    def validate_key(self, api_key: str) -> bool:
        return api_key.startswith("sk-") and len(api_key) > 20

    @property
    def available_models(self) -> list[str]:
        return [
            "mistral-large-latest",
            "mistral-medium-latest",
            "mistral-small-latest",
            "codestral-latest",
        ]
