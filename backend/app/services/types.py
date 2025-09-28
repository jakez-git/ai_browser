from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass(slots=True)
class RetrievedChunk:
    content: str
    source: str
    score: float


@dataclass(slots=True)
class LLMResult:
    text: str
    sources: list[str] = field(default_factory=list)
    raw_chunks: Sequence[RetrievedChunk] | None = None
