from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ..core.config import get_settings
from .types import LLMResult, RetrievedChunk


@dataclass
class LLMService:
    """Wrap interaction with the underlying LLM runtime."""

    model_name: str

    async def generate(
        self,
        prompt: str,
        context_chunks: Sequence[RetrievedChunk],
        stream: bool,
    ) -> LLMResult:
        # Placeholder implementation; will call local runtime via API/CLI.
        _ = stream  # Will be used when streaming is implemented

        context_text = "\n\n".join(chunk.content for chunk in context_chunks)
        formatted_prompt = f"{prompt}\n\nContext:\n{context_text}" if context_text else prompt

        # TODO: integrate with llama.cpp or other runtime.
        generated_text = f"[LLM OUTPUT PLACEHOLDER]\nPrompt: {formatted_prompt}"
        sources = [chunk.source for chunk in context_chunks]

        return LLMResult(text=generated_text, sources=sources, raw_chunks=context_chunks)

    @classmethod
    def from_settings(cls) -> "LLMService":
        settings = get_settings()
        return cls(model_name="local-gguf-placeholder" if settings.environment == "development" else "local-production")
