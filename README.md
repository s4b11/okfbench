# OKFBench Chat

A small demo for exploring how knowledge structure changes retrieval.

[Live demo](https://okfbench-chat.onrender.com/) · [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)

| Mode | What it does |
| --- | --- |
| OKF | Finds relevant concept pages, then follows their Markdown links. |
| BM25 | Ranks corpus documents by keyword relevance. |
| Hybrid | Alternates OKF and BM25 results. |

All modes use the same source limit and answer model. The app shows retrieved evidence, retrieval and generation time, and provider-reported token usage. Timings exclude database writes and browser rendering.

**Dense embeddings are not implemented.** OKF is a knowledge format, while RAG is a retrieval-and-generation pipeline. OKF content can also be used with vector search. This project explores those ideas; it does not establish an accuracy or performance winner.

The dataset describes **Infant Guard**, a fictional newborn-care product. It is sample documentation, not an implemented medical system. The concept and corpus versions cover the same domain but are not fact-identical.

## Run locally

Python 3.12+:

```bash
python -m venv .venv
```

Activate the environment (`.venv\Scripts\Activate.ps1` on Windows, `source .venv/bin/activate` on macOS/Linux), then:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. SQLite and an offline retrieval preview work without API keys.

For generated answers, copy `.env.example` to `.env` and set `GROQ_API_KEY` or `OPENAI_API_KEY`. Groq is used when both are set. `LLM_MODEL` is an optional override; defaults are `openai/gpt-oss-20b` for Groq and `gpt-4o-mini` for OpenAI. `LLM_STUB=true` forces the offline preview, which reports zero LLM tokens.

## Try a comparison

Ask **“How does an approved nutrition plan reach parents?”** in each mode. Inspect the citations and retrieved sources before comparing the timings. Scores are local to each retriever and are not confidence estimates. The app sends each question independently; it does not use earlier messages as context.

`TOP_K` limits the total sources per run (default 5). The OKF path starts with up to two keyword-ranked concepts and follows links up to `OKF_HOP_DEPTH` (default 2), stopping at that source limit. Hybrid alternates the two result lists; it is not a learned reranker.

## Files

- `app/retrieval/`: OKF traversal, BM25, and hybrid.
- `app/routers/chat.py`: chat requests and session run history.
- `app/services/llm.py`: Groq/OpenAI calls and offline preview.
- `knowledge/`: 24 concept pages and 12 corpus documents.
- `static/`, `templates/`: plain JavaScript, CSS, and HTML.
- `tests/`: retrieval and API regression checks.

The concept bundle uses YAML `type`, `title`, and `description`, plus Markdown links. Its IDs come from file paths. The small loader handles this bundle's local links; it is not a general OKF validation tool. See the [OKF specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md).

## API

- `GET /health`: app and provider configuration status.
- `POST /api/chat`: `{ "question": "...", "mode": "okf" }`; modes are `okf`, `bm25`, and `hybrid`.
- `GET /api/runs?session_id=...`: recent runs for that session.

The chat response contains a random session ID. The browser saves it locally; **New session** starts fresh but does not delete database records. Session IDs are bearer identifiers, not user accounts. API details are at `/docs`. The former `vector` mode is now named `bm25`.

## Check and deploy

```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

`render.yaml` deploys the app with Postgres. Set the provider key in Render, and use the database connection URL supplied by Render. SQLite remains the local default. Restart the app after editing knowledge files.

MIT licensed. Created by [Sabii](https://sabithsb.fermyon.app/).
