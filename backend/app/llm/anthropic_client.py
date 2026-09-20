import asyncio
import json
from typing import Any, Type, List
from pydantic import BaseModel
from anthropic import AsyncAnthropic
from app.llm.provider import LLMProvider
from app.core.config import settings

try:
    client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
except:
    client = None

class AnthropicProvider(LLMProvider):
    async def complete(self, messages: list[dict], response_model: Type[BaseModel]) -> BaseModel:
        if not client:
            raise Exception("Anthropic client not configured")
        
        system = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                anthropic_messages.append(msg)
                
        tool = {
            "name": "output_structured_data",
            "description": "Output the required data",
            "input_schema": response_model.model_json_schema()
        }
        
        response = await client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=4096,
            system=system,
            messages=anthropic_messages,
            tools=[tool],
            tool_choice={"type": "tool", "name": "output_structured_data"}
        )
        
        for content in response.content:
            if content.type == "tool_use":
                return response_model(**content.input)
        
        raise Exception("No tool use found in response")

    async def embed(self, texts: list[str]) -> list[list[float]]:
        # Fallback to OpenAI
        from app.llm.openai_client import OpenAIProvider
        openai_provider = OpenAIProvider()
        return await openai_provider.embed(texts)
