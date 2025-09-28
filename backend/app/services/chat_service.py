from __future__ import annotations

from dataclasses import dataclass

from ..models import ChatRequest, ChatResponse
from .llm_service import LLMService
from .retrieval_service import RetrievalService


@dataclass
class ChatService:
    """Coordinates retrieval and LLM completion to answer user queries."""

    retriever: RetrievalService
    llm_service: LLMService

    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        if not request.prompt.strip():
            raise ValueError("Prompt must not be empty.")

        retrieved_chunks = await self.retriever.fetch_relevant_chunks(
            query=request.prompt,
            top_k=request.top_k or 5,
        )

        llm_output = await self.llm_service.generate(
            prompt=request.prompt,
            context_chunks=retrieved_chunks,
            stream=request.stream,
        )

        return ChatResponse(response=llm_output.text, sources=llm_output.sources)


def get_chat_service() -> ChatService:
    return ChatService(
        retriever=RetrievalService.from_settings(),
        llm_service=LLMService.from_settings(),
    )
