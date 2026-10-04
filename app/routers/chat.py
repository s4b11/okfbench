"""Chat and session history."""
import json
import time
import uuid
from dataclasses import asdict
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from openai import APIError
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ChatRun
from app.retrieval.bm25 import BM25Retriever
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.okf import OKFRetriever
from app.services.llm import generate_answer

router = APIRouter(prefix="/api", tags=["chat"])
Mode = Literal["okf", "bm25", "hybrid"]
SESSION_ID = r"^[a-f0-9]{32}$"

okf = OKFRetriever()
bm25 = BM25Retriever()
retrievers = {
    "okf": (okf, "OKF linked concepts"),
    "bm25": (bm25, "BM25 keyword search"),
    "hybrid": (HybridRetriever(okf, bm25), "Hybrid: OKF + BM25"),
}


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    mode: Mode = "okf"
    session_id: str | None = Field(None, pattern=SESSION_ID)


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "question is required")

    started = time.perf_counter()
    retriever, label = retrievers[req.mode]
    sources = retriever.retrieve(question)
    context = retriever.context_block(sources)
    retrieved = time.perf_counter()
    try:
        llm = generate_answer(question, context, req.mode)
    except APIError as exc:
        raise HTTPException(502, "The answer service is unavailable. Please try again.") from exc
    finished = time.perf_counter()

    metrics = {
        "mode": req.mode,
        "latency_ms": round((finished - started) * 1000, 2),
        "retrieval_ms": round((retrieved - started) * 1000, 2),
        "llm_ms": round((finished - retrieved) * 1000, 2),
        "prompt_tokens": llm.prompt_tokens,
        "completion_tokens": llm.completion_tokens,
        "source_count": len(sources),
    }
    public_sources = [asdict(source) for source in sources]
    session_id = req.session_id or uuid.uuid4().hex
    row = ChatRun(
        session_id=session_id, question=question, answer=llm.text,
        sources_json=json.dumps(public_sources), **metrics,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {
        "answer": llm.text, "session_id": session_id, "run_id": row.id,
        "mode": req.mode, "metrics": metrics, "sources": public_sources,
        "retrieval_label": label, "llm_provider": llm.provider,
    }


@router.get("/runs")
def list_runs(
    session_id: str = Query(..., pattern=SESSION_ID),
    limit: int = Query(20, ge=1, le=100),
    mode: Mode | None = None,
    db: Session = Depends(get_db),
):
    query = select(ChatRun).where(ChatRun.session_id == session_id).order_by(ChatRun.id.desc()).limit(limit)
    if mode:
        query = query.where(ChatRun.mode == mode)
    rows = db.scalars(query).all()
    return {"runs": [
        {
            "id": row.id,
            "session_id": row.session_id,
            "mode": row.mode,
            "question": row.question,
            "latency_ms": row.latency_ms,
            "retrieval_ms": row.retrieval_ms,
            "llm_ms": row.llm_ms,
            "prompt_tokens": row.prompt_tokens,
            "completion_tokens": row.completion_tokens,
            "source_count": row.source_count,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]}
