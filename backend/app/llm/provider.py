from abc import ABC, abstractmethod
from typing import Any, Type, List
from pydantic import BaseModel

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, messages: list[dict], response_model: Type[BaseModel]) -> BaseModel:
        pass
        
    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        pass

def get_llm_provider() -> LLMProvider:
    from app.core.config import settings
    if settings.LLM_PROVIDER == 'openai':
        from app.llm.openai_client import OpenAIProvider
        return OpenAIProvider()
    elif settings.LLM_PROVIDER == 'anthropic':
        from app.llm.anthropic_client import AnthropicProvider
        return AnthropicProvider()
    elif settings.LLM_PROVIDER == 'mock':
        from app.llm.mock_client import MockProvider
        return MockProvider()
    raise ValueError(f'Unknown LLM provider: {settings.LLM_PROVIDER}')
