from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from embed_and_retrieve import TOP_K, retrieve


load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
NO_ANSWER_TEXT = "I don't have enough information on that."


@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")
    return Groq(api_key=api_key)


def format_context(retrieved_chunks: list[dict[str, Any]]) -> str:
    sections: list[str] = []
    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        sections.append(
            "\n".join(
                [
                    f"Source: {metadata.get('filename')}",
                    f"Chunk index: {metadata.get('chunk_index')}",
                    f"Distance: {chunk['distance']:.4f}",
                    f"Text: {chunk['text']}",
                ]
            )
        )
    return "\n\n---\n\n".join(sections)


def build_messages(question: str, retrieved_chunks: list[dict[str, Any]]) -> list[dict[str, str]]:
    context = format_context(retrieved_chunks)

    system_prompt = (
        "You are answering questions about student reviews of professors and courses at "
        "the University of Wisconsin-Stevens Point. Use only the information in the "
        "provided context. Do not use outside knowledge. If the context does not contain "
        "enough information to answer the question, reply with exactly: "
        f"{NO_ANSWER_TEXT}"
    )

    user_prompt = (
        f"Question: {question}\n\n"
        "Context:\n"
        f"{context}\n\n"
        "Write a concise answer using only the context above. Do not mention that you are an AI. "
        "Do not invent details."
    )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def generate_answer(question: str, retrieved_chunks: list[dict[str, Any]]) -> str:
    if not retrieved_chunks:
        return NO_ANSWER_TEXT

    client = get_groq_client()
    messages = build_messages(question, retrieved_chunks)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=400,
    )

    answer = response.choices[0].message.content or ""
    answer = answer.strip()
    return answer or NO_ANSWER_TEXT


def build_source_list(retrieved_chunks: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    sources: list[str] = []

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        source = (
            f"{metadata.get('filename')} | chunk {metadata.get('chunk_index')} | "
            f"distance {chunk['distance']:.4f}"
        )
        if source not in seen:
            seen.add(source)
            sources.append(source)

    return sources


def ask(question: str, top_k: int = TOP_K) -> dict[str, Any]:
    retrieved_chunks = retrieve(question, top_k=top_k)
    answer = generate_answer(question, retrieved_chunks)
    sources = build_source_list(retrieved_chunks)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved_chunks,
    }


def test_queries() -> None:
    queries = [
        "What do students say about Professor Smith's grading style?",
        "How difficult is the Introduction to Programming course according to students?",
        "What complaints do students most often have about course registration?",
        "What is the mascot of the University of Wisconsin-Stevens Point?",
    ]

    for query in queries:
        result = ask(query)
        print(f"\nQ: {query}")
        print(f"A: {result['answer']}")
        print("Sources:")
        for source in result["sources"]:
            print(f"- {source}")


if __name__ == "__main__":
    test_queries()