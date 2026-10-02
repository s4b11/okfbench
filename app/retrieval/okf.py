"""OKF retrieval: concept pages with YAML frontmatter and multi-hop links."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from app.config import KNOWLEDGE_DIR, get_settings


@dataclass
class Concept:
    id: str
    title: str
    summary: str
    body: str
    links: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    path: str = ""


@dataclass
class RetrievedSource:
    id: str
    title: str
    snippet: str
    score: float
    kind: str  # concept | hop | doc
    hops: int = 0
    path: str = ""


_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


class OKFRetriever:
    def __init__(self, okf_dir: Path | None = None):
        self.okf_dir = okf_dir or (KNOWLEDGE_DIR / "okf")
        self.concepts: dict[str, Concept] = {}
        self._load()

    def _load(self) -> None:
        self.concepts.clear()
        if not self.okf_dir.exists():
            return
        for path in sorted(self.okf_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            meta, body = {}, text
            m = _FRONTMATTER.match(text)
            if m:
                meta = yaml.safe_load(m.group(1)) or {}
                body = m.group(2).strip()
            cid = str(meta.get("id") or path.stem)
            concept = Concept(
                id=cid,
                title=str(meta.get("title") or cid.replace("-", " ").title()),
                summary=str(meta.get("summary") or ""),
                body=body,
                links=[str(x) for x in (meta.get("links") or [])],
                tags=[str(x) for x in (meta.get("tags") or [])],
                path=str(path.relative_to(path.parents[2]) if len(path.parts) > 2 else path),
            )
            self.concepts[cid] = concept

    def reload(self) -> None:
        self._load()

    def _score(self, concept: Concept, tokens: set[str]) -> float:
        if not tokens:
            return 0.0
        blob = " ".join(
            [concept.id.replace("-", " "), concept.title, concept.summary, " ".join(concept.tags), concept.body]
        ).lower()
        words = set(re.findall(r"[a-z0-9]+", blob))
        hit = len(tokens & words)
        title_words = set(re.findall(r"[a-z0-9]+", (concept.id + " " + concept.title).lower()))
        title_hit = len(tokens & title_words)
        summary_bonus = 1.5 if concept.summary and any(t in concept.summary.lower() for t in tokens) else 0.0
        return hit + title_hit * 2.5 + summary_bonus

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedSource]:
        settings = get_settings()
        k = top_k or settings.top_k
        depth = settings.okf_hop_depth
        tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
        stop = {"the", "a", "an", "is", "are", "what", "how", "why", "do", "does", "in", "of", "to", "for", "and", "or"}
        tokens -= stop

        scored: list[tuple[float, Concept]] = []
        for c in self.concepts.values():
            s = self._score(c, tokens)
            if s > 0:
                scored.append((s, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        seeds = scored[: max(k, 3)]

        results: list[RetrievedSource] = []
        seen: set[str] = set()

        for score, c in seeds[:k]:
            seen.add(c.id)
            results.append(
                RetrievedSource(
                    id=c.id,
                    title=c.title,
                    snippet=(c.summary or c.body[:280]).strip(),
                    score=round(score, 3),
                    kind="concept",
                    hops=0,
                    path=c.path,
                )
            )

        frontier = [c.id for _, c in seeds]
        for hop in range(1, depth + 1):
            nxt: list[str] = []
            for cid in frontier:
                concept = self.concepts.get(cid)
                if not concept:
                    continue
                for link in concept.links:
                    if link in seen or link not in self.concepts:
                        continue
                    linked = self.concepts[link]
                    seen.add(link)
                    nxt.append(link)
                    results.append(
                        RetrievedSource(
                            id=linked.id,
                            title=linked.title,
                            snippet=(linked.summary or linked.body[:280]).strip(),
                            score=round(0.5 / hop, 3),
                            kind="hop",
                            hops=hop,
                            path=linked.path,
                        )
                    )
            frontier = nxt
            if len(results) >= k + depth * 3:
                break

        return results[: k + depth * 2]

    def context_block(self, sources: list[RetrievedSource]) -> str:
        parts = []
        for s in sources:
            c = self.concepts.get(s.id)
            if not c:
                continue
            hop = f" (hop={s.hops})" if s.hops else ""
            links = ", ".join(c.links) if c.links else "none"
            parts.append(
                f"### {c.title} [{c.id}]{hop}\n"
                f"Summary: {c.summary}\n"
                f"Links: {links}\n"
                f"{c.body.strip()}\n"
            )
        return "\n".join(parts)
