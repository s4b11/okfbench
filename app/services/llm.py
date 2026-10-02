"""LLM client: Groq (primary) or OpenAI (secondary), with deterministic stub fallback."""
from __future__ import annotations

from dataclasses import dataclass

from app.config import get_settings


@dataclass
class LLMResult:
    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    provider: str = "stub"


SYSTEM_PROMPT = (
    "You are OKFBench Chat, a careful demo assistant. Answer using ONLY the provided "
    "context. If the context is incomplete, say what is missing. Be concise. "
    "Cite concept or doc ids in brackets like [concept-id] when you use them. "
    "Do not invent product features that are not in the context. "
    "This is a portfolio demo about Infant Guard software documentation, not clinical advice."
)


def _stub_answer(question: str, context: str, mode: str) -> LLMResult:
    preview = context.strip()
    if not preview:
        text = (
            f"(stub mode) No retrieval context for mode={mode}. "
            f"Question was: {question}"
        )
        return LLMResult(text=text, provider="stub")
    lines = [ln.strip() for ln in preview.splitlines() if ln.strip()]
    bullets = []
    for ln in lines:
        if ln.startswith("### ") or ln.startswith("## "):
            bullets.append(ln.lstrip("# ").strip())
        if len(bullets) >= 4:
            break
    if not bullets:
        bullets = lines[:3]
    joined = "; ".join(bullets[:4])
    text = (
        f"(stub mode, no API key) Based on {mode} retrieval, relevant material includes: "
        f"{joined}. Set GROQ_API_KEY for a full generative answer. Question: {question}"
    )
    approx = max(1, len(question.split()) + len(context.split()) // 4)
    return LLMResult(
        text=text,
        prompt_tokens=approx,
        completion_tokens=len(text.split()),
        provider="stub",
    )


def _chat_openai_compatible(base_url: str, api_key: str, model: str, question: str, context: str) -> LLMResult:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Mode context follows.\n\n{context}\n\nQuestion: {question}",
        },
    ]
    resp = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    choice = resp.choices[0].message.content or ""
    usage = getattr(resp, "usage", None)
    pt = int(getattr(usage, "prompt_tokens", 0) or 0)
    ct = int(getattr(usage, "completion_tokens", 0) or 0)
    return LLMResult(text=choice.strip(), prompt_tokens=pt, completion_tokens=ct, provider=model)


def generate_answer(question: str, context: str, mode: str) -> LLMResult:
    settings = get_settings()
    if settings.use_stub_llm:
        return _stub_answer(question, context, mode)

    if settings.groq_api_key:
        return _chat_openai_compatible(
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.groq_api_key,
            model=settings.llm_model or "openai/gpt-oss-20b",
            question=question,
            context=context,
        )

    if settings.openai_api_key:
        return _chat_openai_compatible(
            base_url="https://api.openai.com/v1",
            api_key=settings.openai_api_key,
            model=settings.llm_model or "gpt-4o-mini",
            question=question,
            context=context,
        )

    return _stub_answer(question, context, mode)
