"""Search concept pages and follow their Markdown links."""
import re
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlsplit

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
    kind: str
    hops: int = 0
    path: str = ""


class OKFRetriever:
    def __init__(self, okf_dir: Path | None = None):
        self.okf_dir = (okf_dir or KNOWLEDGE_DIR / "okf").resolve()
        self.concepts: dict[str, Concept] = {}
        for path in sorted(self.okf_dir.rglob("*.md")):
            if path.name in {"index.md", "log.md"}:
                continue
            text = path.read_text(encoding="utf-8")
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
            meta = yaml.safe_load(match[1]) if match else None
            if not isinstance(meta, dict) or not isinstance(meta.get("type"), str) or not meta["type"].strip():
                raise ValueError(f"{path.name}: YAML frontmatter needs a type")
            body = match[2].strip()
            links = []
            for href in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", body):
                url = urlsplit(href)
                if url.scheme or url.netloc or not url.path.endswith(".md"):
                    continue
                target = unquote(url.path)
                target = self.okf_dir / target.lstrip("/") if target.startswith("/") else path.parent / target
                try:
                    links.append(target.resolve().relative_to(self.okf_dir).with_suffix("").as_posix())
                except ValueError:
                    continue
            cid = path.relative_to(self.okf_dir).with_suffix("").as_posix()
            self.concepts[cid] = Concept(
                id=cid,
                title=meta.get("title", path.stem.replace("-", " ").title()),
                summary=meta.get("description", ""),
                body=body,
                links=links,
                tags=meta.get("tags", []),
                path="okf/" + path.relative_to(self.okf_dir).as_posix(),
            )

    def _score(self, concept: Concept, tokens: set[str]) -> float:
        words = set(re.findall(r"[a-z0-9]+", (concept.title + " " + concept.summary + " " + concept.body).lower()))
        title = set(re.findall(r"[a-z0-9]+", concept.title.lower()))
        return len(tokens & words) + 2.5 * len(tokens & title)

    def retrieve(self, question: str, top_k: int | None = None) -> list[RetrievedSource]:
        settings = get_settings()
        k = top_k or settings.top_k
        tokens = set(re.findall(r"[a-z0-9]+", question.lower()))
        tokens -= {"the", "a", "an", "is", "are", "what", "how", "why", "do", "does", "in", "of", "to", "for", "and", "or"}
        ranked = sorted(((self._score(c, tokens), c.id) for c in self.concepts.values()), reverse=True)
        ranked = [(score, cid) for score, cid in ranked if score > 0]
        seed_count = min(2, k) if settings.okf_hop_depth else k
        queue = deque((cid, score, 0) for score, cid in ranked[:seed_count])
        results, seen = [], set()
        while queue and len(results) < k:
            cid, score, hop = queue.popleft()
            if cid in seen or cid not in self.concepts:
                continue
            seen.add(cid)
            concept = self.concepts[cid]
            results.append(RetrievedSource(
                id=cid, title=concept.title, snippet=concept.summary or concept.body[:280],
                score=round(score, 3), kind="hop" if hop else "concept", hops=hop, path=concept.path,
            ))
            if hop < settings.okf_hop_depth:
                queue.extend((link, 0.5 / (hop + 1), hop + 1) for link in concept.links)
        return results

    def context_block(self, sources: list[RetrievedSource]) -> str:
        parts = []
        for source in sources:
            concept = self.concepts[source.id]
            parts.append(f"### {concept.title} [{concept.id}]\n{concept.summary}\n{concept.body}\n")
        return "\n".join(parts)
