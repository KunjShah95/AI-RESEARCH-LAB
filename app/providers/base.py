"""Base provider class"""

from abc import ABC, abstractmethod
from typing import AsyncIterator
from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""
    role: str
    content: str


class BaseProvider(ABC):
    _api_key: str = None
    available_models: list[str] = []

    @abstractmethod
    async def chat_completions(self, messages: list[ChatMessage], model: str) -> dict:
        pass

    async def chat_completions_stream(
        self, messages: list[ChatMessage], model: str
    ) -> AsyncIterator[str]:
        yield "data: [DONE]\n\n"

    async def embeddings(self, input: str | list[str], model: str) -> list[list[float]]:
        return []
