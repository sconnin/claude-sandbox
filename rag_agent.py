"""CLI: agentic RAG query over a Chroma collection (decompose -> retrieve -> synthesize)."""
import argparse
import sys

from rag.config import DEFAULT_COLLECTION, DEFAULT_DB_PATH
from rag.pipeline import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic RAG query over a Chroma collection.")
    parser.add_argument("query", nargs="?", help="The question to ask")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    args = parser.parse_args()

    query = args.query
    if not query:
        if sys.stdin.isatty():
            query = input("Enter your question: ").strip()
        else:
            query = sys.stdin.read().strip()

    if not query:
        print("No query provided.")
        sys.exit(1)

    answer = run(query, args.db_path, args.collection)
    print(answer)


if __name__ == "__main__":
    main()
