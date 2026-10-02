"""Hybrid retrieval: merge OKF concepts and BM25 corpus hits."""
from __future__ import annotations

from app.config import get_settings
from app.retrieval.okf import OKFRetriever, RetrievedSource
from app.retrieval.vector_rag import VectorRAGRetriever


class HybridRetriever:
    def __init__(self, okf: OKFRetriever, vector: VectorRAGRetriever):
        self.okf = okf
        self.vector = vector

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedSource]:
        k = top_k or get_settings().top_k
        okf_hits = self.okf.retrieve(question, top_k=max(2, k // 2 + 1))
        vec_hits = self.vector.retrieve(question, top_k=max(2, k // 2 + 1))

        merged: list[RetrievedSource] = []
        seen: set[str] = set()
        for a, b in zip(okf_hits, vec_hits):
            for hit in (a, b):
                key = f"{hit.kind}:{hit.id}"
                if key in seen:
                    continue
                seen.add(key)
                merged.append(hit)
        for bucket in (okf_hits, vec_hits):
            for hit in bucket:
                key = f"{hit.kind}:{hit.id}"
                if key in seen:
                    continue
                seen.add(key)
                merged.append(hit)
        return merged[: k + 2]

    def context_block(self, sources: list[RetrievedSource]) -> str:
        okf_sources = [s for s in sources if s.kind in ("concept", "hop")]
        doc_sources = [s for s in sources if s.kind == "doc"]
        parts = []
        if okf_sources:
            parts.append("## OKF concepts\n" + self.okf.context_block(okf_sources))
        if doc_sources:
            parts.append("## Corpus passages\n" + self.vector.context_block(doc_sources))
        return "\n\n".join(parts)
