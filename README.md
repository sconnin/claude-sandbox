# claude-code
Temporary repository to experiment with Claude Code.

## Agentic RAG (query decomposition + Chroma)

A very basic agentic RAG pipeline: an OpenAI model (`gpt-5-mini`) decomposes
a complex question into sub-questions, each sub-question retrieves context
from a local Chroma collection, and the model synthesizes a final answer from
the combined context.

### Setup

```bash
pip install -r requirements.txt
```

Authenticate with OpenAI by setting `OPENAI_API_KEY` in `.env` (already
gitignored), or via:
- `export OPENAI_API_KEY=...`

### Ingest documents

Put `.txt` files in a directory (default `./data`), then run:

```bash
python ingest.py ./data
```

This chunks each file and upserts it into a persistent Chroma collection at
`./chroma_db` (using Chroma's built-in local embedding model — no embedding
API key required).

### Ask a question

```bash
python rag_agent.py "your complex, multi-part question"
```

Or run without an argument to be prompted interactively. The script prints
the decomposed sub-questions, then the final synthesized answer.

### Files

- `ingest.py` — CLI: chunks and loads `.txt` files into Chroma
- `rag_agent.py` — CLI: decompose → retrieve → synthesize pipeline
- `rag/` — package containing the pipeline logic:
  - `config.py` — shared defaults (paths, model, chunk size)
  - `chunking.py` — text chunking
  - `store.py` — Chroma client/collection access
  - `ingestion.py` — file loading and upsert logic
  - `decompose.py` — query decomposition
  - `retrieval.py` — per-sub-query Chroma retrieval
  - `synthesis.py` — final answer synthesis
  - `pipeline.py` — orchestrates decompose → retrieve → synthesize
- `requirements.txt` — `openai` + `chromadb`
- `.env` — local secrets (e.g. `OPENAI_API_KEY`), gitignored

