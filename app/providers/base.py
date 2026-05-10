"""Base provider class"""

from abc import ABC, abstractmethod
from typing import AsyncIterator


class BaseProvider(ABC):
    _api_key: str = None
    available_models: list[str] = []

    @abstractmethod
    async def chat_completions(self, messages: list[dict], model: str) -> str:
        pass

    async def chat_completions_stream(
        self, messages: list[dict], model: str
    ) -> AsyncIterator[str]:
        yield "not implemented"

    async def embeddings(self, input: str | list[str], model: str) -> list[list[float]]:
        return []
