# OKFBench Chat

Open-source demo chatbot that compares **OKF concept retrieval** (structured concepts + multi-hop links) with a **BM25 lexical / vector-like corpus RAG** baseline, plus a **hybrid** mode.

**Domain:** Fictional Infant Guard newborn-care demo set at K Brother Children's Hospital. Knowledge is original demo writing for open-source retrieval comparison.

**Stack:** FastAPI, SQLAlchemy, PostgreSQL or SQLite, Tailwind CDN UI, optional Groq LLM (primary; OpenAI secondary)

> Not medical advice. Not a university report. Do not commit private project reports or verbatim extracts. Demo knowledge is a portfolio showcase written as fictional portfolio content, not a clinical source of truth.

## Why this demo

| Mode | What it retrieves | Good for |
|------|-------------------|----------|
| **OKF** | Concept `.md` files with YAML `id`, `summary`, `links`, `tags` then multi-hop link expansion | Multi-hop questions ("how nutrition connects to alerts") |
| **Vector-like (BM25)** | Longer unstructured docs in `knowledge/corpus/` | Fuzzy keyword overlap over narrative text |
| **Hybrid** | Interleaved OKF + BM25 hits | Side-by-side grounding in one answer |

Dense embeddings (sentence-transformers) and MCP tooling are **deferred** so the app stays light enough for a free Render web service. See [Future work](#future-work).

## Quick start (local)

```bash
cd chatbot
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open http://127.0.0.1:8000

- **No API keys required** for UI browsing, retrieval, and deterministic stub answers.
- Set `GROQ_API_KEY` in `.env` for live generative answers; Groq is the primary LLM path.
- `OPENAI_API_KEY` is optional and used as a secondary path only when no Groq key is set.

### Postgres locally (optional)

```bash
# .env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/okfbench
```

## API

| Method | Path | Notes |
|--------|------|-------|
| GET | `/` | Chat UI |
| GET | `/health` | Liveness + llm/db mode |
| POST | `/api/chat` | `{ "question", "mode": "vector\|okf\|hybrid", "session_id?" }` |
| GET | `/api/runs` | Recent metrics (`limit`, optional `mode`, `session_id`) |
| POST | `/api/reload-knowledge` | Reload OKF + corpus from disk |

Each chat run stores latency, retrieval time, LLM time, token counts (when the provider returns them), and retrieved sources in the database.

## Project layout

```
chatbot/
  app/
    main.py
    config.py
    db.py
    models.py
    routers/          # health, chat
    retrieval/        # okf, vector_rag (BM25), hybrid
    services/         # llm, metrics
  knowledge/
    okf/              # Infant Guard concept pages
    corpus/           # parallel unstructured docs
  eval/sample_questions.json
  templates/index.html
  static/
  requirements.txt
  render.yaml
  .env.example
```

## Deploy on Render (free)

1. Push this repo to GitHub.
2. On Render, create a **PostgreSQL** database (free plan).
3. Create a **Web Service** from the repo (or use Blueprint with `render.yaml`).
4. Build: `pip install -r requirements.txt`
5. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Set env vars:
   - `DATABASE_URL` from the Render Postgres connection string. If Render gives `postgres://`, change the scheme to `postgresql+psycopg://` for SQLAlchemy + psycopg3.
   - Optional: `GROQ_API_KEY` (primary LLM), `LLM_MODEL=openai/gpt-oss-20b`
7. Deploy. Open the service URL.

`render.yaml` is a starting Blueprint; free plans and connection string formats can change, so verify in the Render dashboard.

## How OKF vs BM25 works here

**OKF (Open Knowledge Fragments style):** each concept is a short markdown page with frontmatter:

```yaml
---
id: ai-nutrition-planning
title: AI-Powered Nutrition Planning
summary: ...
links:
  - nutrition-plan-module
  - alerts-notifications
tags:
  - ai
  - nutrition
---
```

Retrieval token-overlaps the question against concept text, ranks seed concepts, then walks `links` up to `OKF_HOP_DEPTH` (default 2). Hopped concepts are labeled in the UI.

**BM25 corpus RAG:** `knowledge/corpus/*.md` holds longer narrative mirrors of the same facts. Okapi BM25 ranks passages. This is intentionally a **lexical / vector-like baseline**, not dense embedding search, so free hosting stays feasible without heavyweight model downloads.

**Hybrid:** merges top OKF and BM25 hits for one context block.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | SQLite file under project root | Postgres or SQLite URL |
| `GROQ_API_KEY` | empty | Primary live LLM via Groq |
| `OPENAI_API_KEY` | empty | Optional secondary LLM path, used when Groq is unavailable |
| `LLM_MODEL` | `openai/gpt-oss-20b` | Groq chat model id |
| `LLM_STUB` | false | Force deterministic stub answers |
| `TOP_K` | 5 | Retrieval depth |
| `OKF_HOP_DEPTH` | 2 | OKF link expansion |
| `APP_NAME` | OKFBench Chat | UI title |
| `CORS_ORIGINS` | `*` | Comma-separated origins |

## Sample knowledge

~24 Infant Guard OKF concepts covering overview, modules, AI nutrition (doctor approval), malnutrition risk thresholds, vaccination to age 5, three-tier architecture, dashboards, security, and roadmap. Twelve corpus documents expand the same facts as unstructured prose for BM25 comparison. Content is written as fictional demo content; do not treat it as clinical guidance.

Try questions in `eval/sample_questions.json` (also loaded in the UI).

## Future work

- Optional dense embeddings (sentence-transformers or API embeddings) behind an env flag
- MCP tools for knowledge browsing / eval harnesses
- Side-by-side dual-pane UI that fires OKF and BM25 in parallel for one question
- Export run metrics to CSV for blog / portfolio writeups

## License

MIT. See [LICENSE](LICENSE).
