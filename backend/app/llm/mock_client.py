from typing import Any, Type, List
from pydantic import BaseModel
from app.llm.provider import LLMProvider

class MockProvider(LLMProvider):
    async def complete(self, messages: list[dict], response_model: Type[BaseModel]) -> BaseModel:
        schema = response_model.model_json_schema()
        # Very basic mock, this should generally be replaced by actual tests
        return response_model()

    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.1] * 1536 for _ in texts]
