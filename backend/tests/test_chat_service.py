import asyncio

import pytest

from app.models import ChatRequest
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.types import LLMResult, RetrievedChunk


class DummyRetriever(RetrievalService):
    def __init__(self, chunks: list[RetrievedChunk]):
        super().__init__(max_chunks=len(chunks))
        self._chunks = chunks

    async def fetch_relevant_chunks(self, query: str, top_k: int):  # type: ignore[override]
        _ = query
        return self._chunks[:top_k]


class DummyLLM(LLMService):
    def __init__(self):
        super().__init__(model_name="dummy")

    async def generate(self, prompt: str, context_chunks, stream: bool):  # type: ignore[override]
        _ = stream
        text = f"PROMPT:{prompt}|CONTEXT:{len(list(context_chunks))}"
        return LLMResult(text=text, sources=[chunk.source for chunk in context_chunks])


@pytest.mark.asyncio
async def test_chat_service_generates_response_with_sources():
    retriever = DummyRetriever(
        [
            RetrievedChunk(content="Chunk 1", source="file1.txt", score=0.9),
            RetrievedChunk(content="Chunk 2", source="file2.txt", score=0.8),
        ]
    )
    llm = DummyLLM()
    service = ChatService(retriever=retriever, llm_service=llm)

    result = await service.generate_response(ChatRequest(prompt="Hello", top_k=1))

    assert "PROMPT:Hello" in result.response
    assert result.sources == ["file1.txt"]


@pytest.mark.asyncio
async def test_chat_service_rejects_empty_prompt():
    retriever = DummyRetriever([])
    llm = DummyLLM()
    service = ChatService(retriever=retriever, llm_service=llm)

    with pytest.raises(ValueError):
        await service.generate_response(ChatRequest(prompt=" "))
