"""Groq provider using Vercel AI SDK"""

import json
from typing import AsyncGenerator, Any
from openai import AsyncOpenAI
from app.providers.base import BaseProvider, ChatMessage


class GroqProvider(BaseProvider):
    """Groq provider."""

    name = "groq"
    supports_streaming = True
    supports_embeddings = False

    BASE_URL = "https://api.groq.com/openai/v1"

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        if not self._client:
            self._client = AsyncOpenAI(api_key=self._api_key, base_url=self.BASE_URL)
        return self._client

    async def chat_completions(
        self,
        messages: list[ChatMessage],
        model: str = "llama-3.1-70b-versatile",
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        client = self._get_client()
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return response.model_dump()

    async def chat_completions_stream(
        self,
        messages: list[ChatMessage],
        model: str = "llama-3.1-70b-versatile",
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        client = self._get_client()
        stream = await client.chat.completions.create(
            model=model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            stream=True,
            **kwargs,
        )
        async for chunk in stream:
            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                yield f"data: {json.dumps(chunk.choices[0].delta.model_dump())}\n\n"
        yield "data: [DONE]\n\n"

    async def embeddings(self, input: str | list[str], model: str) -> list[list[float]]:
        raise NotImplementedError("Groq does not support embeddings")

    def validate_key(self, api_key: str) -> bool:
        return len(api_key) > 20

    @property
    def available_models(self) -> list[str]:
        return [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3-70b-versatile",
            "llama-3-8b-versatile",
            "mixtral-8x7b-32768",
            "gemma-7b-it",
        ]
