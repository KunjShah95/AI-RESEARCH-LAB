"""Google Gemini provider using Vercel AI SDK"""

import json
import uuid
from typing import AsyncGenerator, Any
from google.genai import AsyncClient
from app.providers.base import BaseProvider, ChatMessage


class GoogleProvider(BaseProvider):
    """Google Gemini provider."""

    name = "google"
    supports_streaming = True
    supports_embeddings = True

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client: AsyncClient | None = None

    def _get_client(self) -> AsyncClient:
        if not self._client:
            self._client = AsyncClient(api_key=self._api_key)
        return self._client

    async def chat_completions(
        self,
        messages: list[ChatMessage],
        model: str = "gemini-2.0-flash-exp",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs,
    ) -> dict[str, Any]:
        client = self._get_client()

        contents = []
        for msg in messages:
            if msg.role == "system":
                continue
            contents.append({"role": msg.role, "parts": [{"text": msg.content}]})

        response = await client.models.generate_content(
            model=model,
            contents=contents,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                **kwargs,
            },
        )

        return {
            "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
            "model": model,
            "choices": [{"message": {"role": "model", "content": response.text}}],
        }

    async def chat_completions_stream(
        self, messages: list[ChatMessage], model: str = "gemini-2.0-flash-exp", **kwargs
    ) -> AsyncGenerator[str, None]:
        client = self._get_client()

        contents = []
        for msg in messages:
            if msg.role == "system":
                continue
            contents.append({"role": msg.role, "parts": [{"text": msg.content}]})

        async with client.models.generate_content(
            model=model, contents=contents, stream=True, **kwargs
        ) as stream:
            async for chunk in stream:
                if chunk.text:
                    yield f"data: {json.dumps({'choices': [{'delta': {'content': chunk.text}}]})}\n\n"
        yield "data: [DONE]\n\n"

    async def embeddings(
        self, input: str | list[str], model: str = "text-embedding-004"
    ) -> list[list[float]]:
        client = self._get_client()

        inputs = input if isinstance(input, list) else [input]

        response = await client.models.embed_content(
            model=model, content=inputs, task_type="SEMANTIC_SIMILARITY"
        )

        return [e.values for e in response.embeddings]

    def validate_key(self, api_key: str) -> bool:
        return len(api_key) > 20

    @property
    def available_models(self) -> list[str]:
        return [
            "gemini-2.0-flash-exp",
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
        ]
