"""Chat and run-history API."""
from __future__ import annotations

import uuid
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ChatRun
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.okf import OKFRetriever
from app.retrieval.vector_rag import VectorRAGRetriever
from app.services.llm import generate_answer
from app.services.metrics import RunMetrics, sources_json, sources_to_dicts, timer

router = APIRouter(prefix="/api", tags=["chat"])

Mode = Literal["vector", "okf", "hybrid"]

_okf = OKFRetriever()
_vector = VectorRAGRetriever()
_hybrid = HybridRetriever(_okf, _vector)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    mode: Mode = "okf"
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    run_id: int
    mode: str
    metrics: dict[str, Any]
    sources: list[dict[str, Any]]
    retrieval_label: str
    llm_provider: str


def _context_for(mode: Mode, question: str):
    with timer() as t:
        if mode == "okf":
            sources = _okf.retrieve(question)
            context = _okf.context_block(sources)
            label = "OKF concept graph (multi-hop links)"
        elif mode == "vector":
            sources = _vector.retrieve(question)
            context = _vector.context_block(sources)
            label = _vector.label
        else:
            sources = _hybrid.retrieve(question)
            context = _hybrid.context_block(sources)
            label = "Hybrid: OKF + BM25"
    return sources, context, label, t[0]


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    session_id = (req.session_id or "").strip() or uuid.uuid4().hex
    metrics = RunMetrics(mode=req.mode)

    with timer() as total:
        sources, context, label, retrieval_ms = _context_for(req.mode, question)
        metrics.retrieval_ms = retrieval_ms
        metrics.sources = sources_to_dicts(sources)
        metrics.source_count = len(sources)

        with timer() as llm_t:
            llm = generate_answer(question, context, req.mode)
        metrics.llm_ms = llm_t[0]
        metrics.prompt_tokens = llm.prompt_tokens
        metrics.completion_tokens = llm.completion_tokens

    metrics.latency_ms = total[0]

    row = ChatRun(
        session_id=session_id,
        mode=req.mode,
        question=question,
        answer=llm.text,
        sources_json=sources_json(sources),
        latency_ms=metrics.latency_ms,
        retrieval_ms=metrics.retrieval_ms,
        llm_ms=metrics.llm_ms,
        prompt_tokens=metrics.prompt_tokens,
        completion_tokens=metrics.completion_tokens,
        source_count=metrics.source_count,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return ChatResponse(
        answer=llm.text,
        session_id=session_id,
        run_id=row.id,
        mode=req.mode,
        metrics=metrics.to_public(),
        sources=metrics.sources,
        retrieval_label=label,
        llm_provider=llm.provider,
    )


@router.get("/runs")
def list_runs(
    limit: int = Query(20, ge=1, le=100),
    mode: Mode | None = None,
    session_id: str | None = None,
    db: Session = Depends(get_db),
):
    q = select(ChatRun).order_by(ChatRun.id.desc()).limit(limit)
    if mode:
        q = q.where(ChatRun.mode == mode)
    if session_id:
        q = q.where(ChatRun.session_id == session_id)
    rows = db.scalars(q).all()
    return {
        "runs": [
            {
                "id": r.id,
                "session_id": r.session_id,
                "mode": r.mode,
                "question": r.question,
                "answer": r.answer[:400],
                "latency_ms": r.latency_ms,
                "retrieval_ms": r.retrieval_ms,
                "llm_ms": r.llm_ms,
                "prompt_tokens": r.prompt_tokens,
                "completion_tokens": r.completion_tokens,
                "source_count": r.source_count,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]
    }


@router.post("/reload-knowledge")
def reload_knowledge():
    """Reload OKF and corpus from disk (useful in local demos)."""
    _okf.reload()
    _vector.reload()
    return {
        "okf_concepts": len(_okf.concepts),
        "corpus_docs": len(_vector.docs),
    }
