import pytest
import asyncio
from shared.llm_client import LLMClient

@pytest.mark.asyncio
async def test_analyze_text():
    client = LLMClient()
    result = await client.analyze_text("Hello, world!", context="test")
    assert isinstance(result, str)
    assert len(result) > 0