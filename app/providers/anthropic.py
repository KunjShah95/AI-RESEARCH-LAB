"""Anthropic provider using Vercel AI SDK"""

import json
from typing import AsyncGenerator, Any
from anthropic import AsyncAnthropic
from app.providers.base import BaseProvider, ChatMessage


class AnthropicProvider(BaseProvider):
    """Anthropic provider."""

    name = "anthropic"
    supports_streaming = True
    supports_embeddings = False

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client: AsyncAnthropic | None = None

    def _get_client(self) -> AsyncAnthropic:
        if not self._client:
            self._client = AsyncAnthropic(api_key=self._api_key)
        return self._client

    async def chat_completions(
        self,
        messages: list[ChatMessage],
        model: str = "claude-3-5-sonnet-20241022",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs,
    ) -> dict[str, Any]:
        client = self._get_client()

        system = ""
        anthropic_messages = []
        for msg in messages:
            if msg.role == "system":
                system = msg.content
            else:
                anthropic_messages.append({"role": msg.role, "content": msg.content})

        response = await client.messages.create(
            model=model,
            system=system,
            messages=anthropic_messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        return {
            "id": response.id,
            "model": response.model,
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response.content[0].text if response.content else "",
                    }
                }
            ],
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
            },
        }

    async def chat_completions_stream(
        self,
        messages: list[ChatMessage],
        model: str = "claude-3-5-sonnet-20241022",
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        client = self._get_client()

        system = ""
        anthropic_messages = []
        for msg in messages:
            if msg.role == "system":
                system = msg.content
            else:
                anthropic_messages.append({"role": msg.role, "content": msg.content})

        async with client.messages.stream(
            model=model, system=system, messages=anthropic_messages, **kwargs
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'choices': [{'delta': {'content': text}}]})}\n\n"
        yield "data: [DONE]\n\n"

    async def embeddings(self, input: str | list[str], model: str) -> list[list[float]]:
        raise NotImplementedError("Anthropic does not support embeddings")

    def validate_key(self, api_key: str) -> bool:
        return api_key.startswith("sk-ant-") and len(api_key) > 20

    @property
    def available_models(self) -> list[str]:
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]
