"""Synthesize a final answer from retrieved context across all sub-queries."""
from openai import OpenAI

from rag.config import MODEL


def synthesize(client: OpenAI, query: str, subqueries: list[str],
                retrieved: dict[str, list[str]]) -> str:
    """Combine retrieved context across all sub-queries into a final answer."""
    context_blocks = []
    for sq in subqueries:
        chunks = retrieved.get(sq, [])
        if not chunks:
            continue
        joined = "\n---\n".join(chunks)
        context_blocks.append(f"Sub-question: {sq}\nRetrieved context:\n{joined}")

    context_text = "\n\n".join(context_blocks) if context_blocks else "(no relevant context retrieved)"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer the user's original question using only the retrieved "
                    "context provided below. If the context is insufficient to fully "
                    "answer, say so explicitly rather than guessing."
                ),
            },
            {
                "role": "user",
                "content": f"Original question: {query}\n\n{context_text}",
            },
        ],
    )
    return response.choices[0].message.content
