"""Load .txt documents from a directory and upsert them into a Chroma collection."""
import os

from rag.chunking import chunk_text
from rag.config import DEFAULT_COLLECTION, DEFAULT_DB_PATH, DEFAULT_DOCS_DIR
from rag.store import get_collection


def load_documents(docs_dir: str) -> tuple[list[str], list[str], list[dict]]:
    """Read every .txt file in docs_dir and chunk it into ids/docs/metadatas."""
    ids, docs, metadatas = [], [], []
    for fname in sorted(os.listdir(docs_dir)):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(docs_dir, fname)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        for i, chunk in enumerate(chunk_text(text)):
            ids.append(f"{fname}::{i}")
            docs.append(chunk)
            metadatas.append({"source": fname, "chunk": i})
    return ids, docs, metadatas


def ingest(docs_dir: str = DEFAULT_DOCS_DIR, db_path: str = DEFAULT_DB_PATH,
           collection_name: str = DEFAULT_COLLECTION) -> int:
    """Chunk and upsert all .txt files in docs_dir. Returns the number of chunks ingested."""
    if not os.path.isdir(docs_dir):
        raise FileNotFoundError(f"docs directory '{docs_dir}' does not exist.")

    ids, docs, metadatas = load_documents(docs_dir)
    if not docs:
        return 0

    collection = get_collection(db_path, collection_name)
    collection.upsert(ids=ids, documents=docs, metadatas=metadatas)
    return len(docs)
