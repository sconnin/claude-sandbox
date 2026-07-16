"""Retrieve context chunks from a Chroma collection for each sub-query."""
from chromadb.api.models.Collection import Collection


def retrieve(collection: Collection, subqueries: list[str], n_results: int = 4) -> dict[str, list[str]]:
    """Query the Chroma collection once per sub-query; dedupe returned chunks."""
    results: dict[str, list[str]] = {}
    seen: set[str] = set()
    for sq in subqueries:
        res = collection.query(query_texts=[sq], n_results=n_results)
        docs = res.get("documents", [[]])[0]
        unique_docs = []
        for doc in docs:
            if doc not in seen:
                seen.add(doc)
                unique_docs.append(doc)
        results[sq] = unique_docs
    return results
