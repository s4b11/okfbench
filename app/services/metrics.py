"""Helpers for timing and serializing run metrics."""
from __future__ import annotations

import json
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator

from app.retrieval.okf import RetrievedSource


@dataclass
class RunMetrics:
    latency_ms: float = 0.0
    retrieval_ms: float = 0.0
    llm_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    source_count: int = 0
    mode: str = ""
    sources: list[dict[str, Any]] = field(default_factory=list)

    def to_public(self) -> dict[str, Any]:
        return {
            "latency_ms": round(self.latency_ms, 2),
            "retrieval_ms": round(self.retrieval_ms, 2),
            "llm_ms": round(self.llm_ms, 2),
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "source_count": self.source_count,
            "mode": self.mode,
            "sources": self.sources,
        }


def sources_to_dicts(sources: list[RetrievedSource]) -> list[dict[str, Any]]:
    return [
        {
            "id": s.id,
            "title": s.title,
            "snippet": s.snippet,
            "score": s.score,
            "kind": s.kind,
            "hops": s.hops,
            "path": s.path,
        }
        for s in sources
    ]


def sources_json(sources: list[RetrievedSource]) -> str:
    return json.dumps(sources_to_dicts(sources))


@contextmanager
def timer() -> Iterator[list[float]]:
    """Yield a one-element list; filled with elapsed ms on exit."""
    box: list[float] = [0.0]
    start = time.perf_counter()
    try:
        yield box
    finally:
        box[0] = (time.perf_counter() - start) * 1000.0
