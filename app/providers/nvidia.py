"""NVIDIA NIM provider (custom adapter)"""

import json
from typing import AsyncGenerator, Any
import httpx
from app.providers.base import BaseProvider, ChatMessage


class NVIDIAProvider(BaseProvider):
    """NVIDIA NIM provider."""

    name = "nvidia"
    supports_streaming = True
    supports_embeddings = True

    BASE_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client: httpx.AsyncClient | None = None

    def _get_client(self) -> httpx.AsyncClient:
        if not self._client:
            self._client = httpx.AsyncClient(
                headers={"Authorization": f"Bearer {self._api_key}"},
                base_url=self.BASE_URL,
                timeout=60.0,
            )
        return self._client

    async def chat_completions(
        self,
        messages: list[ChatMessage],
        model: str = "meta/llama-3.1-70b-instruct",
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
        self,
        messages: list[ChatMessage],
        model: str = "meta/llama-3.1-70b-instruct",
        **kwargs,
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

    async def embeddings(
        self, input: str | list[str], model: str = "nvidia/nvolveqa_40k"
    ) -> list[list[float]]:
        client = self._get_client()

        inputs = input if isinstance(input, list) else [input]

        response = await client.post(
            "/embeddings", json={"input": inputs, "model": model}
        )
        response.raise_for_status()
        data = response.json()
        return [e["embedding"] for e in data["data"]]

    def validate_key(self, api_key: str) -> bool:
        return len(api_key) > 10

    @property
    def available_models(self) -> list[str]:
        return [
            "meta/llama-3.1-70b-instruct",
            "meta/llama-3.1-8b-instruct",
            "nvidia/nvolveqa_40k",
            "mistralai/mixtral-8x7b-instruct-v0.1",
        ]
