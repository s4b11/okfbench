"""Hybrid retrieval: merge OKF concepts and BM25 corpus hits."""
from __future__ import annotations
from itertools import zip_longest

from app.config import get_settings
from app.retrieval.okf import OKFRetriever, RetrievedSource
from app.retrieval.bm25 import BM25Retriever


class HybridRetriever:
    def __init__(self, okf: OKFRetriever, bm25: BM25Retriever):
        self.okf = okf
        self.bm25 = bm25

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedSource]:
        k = top_k or get_settings().top_k
        okf_hits = self.okf.retrieve(question, top_k=k)
        bm25_hits = self.bm25.retrieve(question, top_k=k)
        merged = []
        for pair in zip_longest(okf_hits, bm25_hits):
            merged.extend(hit for hit in pair if hit is not None)
        return merged[:k]

    def context_block(self, sources: list[RetrievedSource]) -> str:
        okf_sources = [s for s in sources if s.kind in ("concept", "hop")]
        doc_sources = [s for s in sources if s.kind == "doc"]
        parts = []
        if okf_sources:
            parts.append("## OKF concepts\n" + self.okf.context_block(okf_sources))
        if doc_sources:
            parts.append("## Corpus documents\n" + self.bm25.context_block(doc_sources))
        return "\n\n".join(parts)
