"""Lexical BM25 retrieval over corpus docs (free-tier friendly vector-like baseline).

Labeled clearly as BM25/lexical, not dense embeddings. Default works offline with no API keys.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from app.config import KNOWLEDGE_DIR, get_settings
from app.retrieval.okf import RetrievedSource


@dataclass
class CorpusDoc:
    id: str
    title: str
    text: str
    path: str
    tokens: list[str]


_TOKEN = re.compile(r"[a-z0-9]+")
_STOP = {
    "the", "a", "an", "is", "are", "was", "were", "be", "to", "of", "and", "or", "in",
    "on", "for", "with", "as", "by", "at", "from", "that", "this", "it", "its",
}


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1]


class BM25Index:
    """Okapi BM25 over an in-memory corpus."""

    def __init__(self, docs: list[CorpusDoc], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.k1 = k1
        self.b = b
        self.N = len(docs)
        self.avgdl = (sum(len(d.tokens) for d in docs) / self.N) if self.N else 0.0
        self.df: Counter[str] = Counter()
        for d in docs:
            for term in set(d.tokens):
                self.df[term] += 1

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def score(self, query_tokens: list[str], doc: CorpusDoc) -> float:
        if not doc.tokens:
            return 0.0
        tf = Counter(doc.tokens)
        dl = len(doc.tokens)
        s = 0.0
        for term in query_tokens:
            f = tf.get(term, 0)
            if f == 0:
                continue
            denom = f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1))
            s += self.idf(term) * (f * (self.k1 + 1)) / denom
        return s


class VectorRAGRetriever:
    """BM25/lexical retriever presented as the vector-RAG baseline for free deploy."""

    label = "BM25 lexical (vector-like baseline)"

    def __init__(self, corpus_dir: Path | None = None):
        self.corpus_dir = corpus_dir or (KNOWLEDGE_DIR / "corpus")
        self.docs: list[CorpusDoc] = []
        self.index: BM25Index | None = None
        self._load()

    def _load(self) -> None:
        self.docs = []
        if self.corpus_dir.exists():
            paths = sorted(self.corpus_dir.glob("*.md")) + sorted(self.corpus_dir.glob("*.txt"))
            for path in paths:
                text = path.read_text(encoding="utf-8")
                title = path.stem.replace("_", " ").replace("-", " ").title()
                lines = text.strip().splitlines()
                if lines and lines[0].startswith("# "):
                    title = lines[0][2:].strip()
                    text = "\n".join(lines[1:]).strip()
                doc = CorpusDoc(
                    id=path.stem,
                    title=title,
                    text=text,
                    path=str(path),
                    tokens=tokenize(title + " " + text),
                )
                self.docs.append(doc)
        self.index = BM25Index(self.docs)

    def reload(self) -> None:
        self._load()

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedSource]:
        k = top_k or get_settings().top_k
        if not self.index or not self.docs:
            return []
        q = tokenize(question)
        ranked = sorted(
            ((self.index.score(q, d), d) for d in self.docs),
            key=lambda x: x[0],
            reverse=True,
        )
        out: list[RetrievedSource] = []
        for score, d in ranked[:k]:
            if score <= 0:
                continue
            snippet = d.text[:320].replace("\n", " ").strip()
            out.append(
                RetrievedSource(
                    id=d.id,
                    title=d.title,
                    snippet=snippet,
                    score=round(score, 3),
                    kind="doc",
                    hops=0,
                    path=d.path,
                )
            )
        return out

    def context_block(self, sources: list[RetrievedSource]) -> str:
        by_id = {d.id: d for d in self.docs}
        parts = []
        for s in sources:
            d = by_id.get(s.id)
            if not d:
                continue
            parts.append(f"### {d.title} [{d.id}]\n{d.text.strip()}\n")
        return "\n".join(parts)
