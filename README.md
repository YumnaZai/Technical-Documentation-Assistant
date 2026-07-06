# Technical Documentation Assistant

A RAG-based (Retrieval-Augmented Generation) chat assistant that answers questions about internal technical documentation — API references, architecture docs, wikis, and READMEs — with cited, grounded answers instead of manual searching.

## What It Does

Ask a question like *"How does authentication work?"* and the system retrieves the most relevant chunks across multiple source documents, then generates an answer using only that retrieved content, citing which files the information came from.

## Tech Stack

| Layer | Tools |
|---|---|
| Orchestration | LangChain |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector store | ChromaDB |
| Generation | OpenAI `gpt-4.1-mini` |
| Backend API | FastAPI |
| Frontend | React (Vite) |

## How It Works

1. **Indexing (one-time)** — Documents in `data/raw_docs/` are split into chunks, converted into embeddings, and stored in a local vector database.
2. **Querying (per request)** — A user's question is embedded the same way, matched against stored chunks via similarity search, filtered by a relevance threshold, and diversified across source files. The retrieved chunks are passed to the LLM, which generates a grounded, cited answer.

## Project Structure

```
├── data/raw_docs/          # Source documentation, organized by category
├── src/                    # Core RAG pipeline (ingest, embed, retrieve, generate)
├── scripts/build_index.py  # Run to (re)build the vector index
├── storage/vector_db/      # Persisted vector index
├── backend_api.py          # FastAPI wrapper exposing the pipeline over HTTP
├── frontend/                # React chat interface
└── app.py                   # CLI entry point
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_key_here
```

## Usage

**Build the index** (run once, or whenever docs change):
```bash
python scripts/build_index.py
```

**CLI mode:**
```bash
python app.py
```

**Web UI mode** (two terminals):
```bash
uvicorn backend_api:app --reload --port 8000
```
```bash
cd frontend && npm run dev
```

## Key Configuration (`src/config.py`)

| Variable | Purpose |
|---|---|
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | Controls how documents are split into retrievable pieces |
| `TOP_K` | Number of chunks retrieved per question |
| `score_threshold` | Minimum relevance score for a chunk to be included |

## Status

Functional prototype — tested against multi-document retrieval, cross-source reasoning, precision, and grounded refusal (no hallucination on out-of-scope questions). Next steps: formal evaluation metrics, expanded document set.
