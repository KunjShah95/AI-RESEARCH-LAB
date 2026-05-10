"""OpenAI provider using Vercel AI SDK"""

import json
from typing import AsyncGenerator, Any
from openai import AsyncOpenAI
from app.providers.base import BaseProvider, ChatMessage


class OpenAIProvider(BaseProvider):
    """OpenAI provider."""

    name = "openai"
    supports_streaming = True
    supports_embeddings = True

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        if not self._client:
            self._client = AsyncOpenAI(api_key=self._api_key)
        return self._client

    async def chat_completions(
        self,
        messages: list[ChatMessage],
        model: str = "gpt-4o",
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
        self, messages: list[ChatMessage], model: str = "gpt-4o", **kwargs
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

    async def embeddings(
        self, input: str | list[str], model: str = "text-embedding-3-small"
    ) -> list[list[float]]:
        client = self._get_client()
        response = await client.embeddings.create(
            model=model, input=input if isinstance(input, list) else [input]
        )
        return [e.embedding for e in response.data]

    def validate_key(self, api_key: str) -> bool:
        return api_key.startswith("sk-") and len(api_key) > 20

    @property
    def available_models(self) -> list[str]:
        return [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
            "o1",
            "o1-mini",
            "o1-preview",
            "text-embedding-3-small",
            "text-embedding-3-large",
        ]
