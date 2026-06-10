from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

from ingest_and_chunk import DOCUMENTS_DIR, build_chunks, load_txt_files


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5
CHROMA_DIR = Path(__file__).resolve().parent / "chroma_store"
COLLECTION_NAME = "unofficial_guide_chunks"


def load_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def build_vector_store() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    documents = load_txt_files(DOCUMENTS_DIR)
    chunks = build_chunks(documents)

    if not chunks:
        return collection

    model = load_embedding_model()

    chunk_texts = [chunk.text for chunk in chunks]
    embeddings = model.encode(chunk_texts, normalize_embeddings=True).tolist()

    ids = [
        f"{chunk.metadata['filename']}::{chunk.metadata['document_index']}::{chunk.metadata['chunk_index']}"
        for chunk in chunks
    ]
    metadatas = [chunk.metadata for chunk in chunks]

    collection.upsert(ids=ids, documents=chunk_texts, metadatas=metadatas, embeddings=embeddings)
    return collection


def retrieve(query: str, top_k: int = TOP_K) -> list[dict[str, Any]]:
    model = load_embedding_model()
    collection = build_vector_store()
    query_embedding = model.encode([query], normalize_embeddings=True).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    items: list[dict[str, Any]] = []
    for index, document in enumerate(results["documents"][0]):
        items.append(
            {
                "rank": index + 1,
                "text": document,
                "metadata": results["metadatas"][0][index],
                "distance": results["distances"][0][index],
            }
        )

    return items


def print_retrieval_results(query: str, top_k: int = TOP_K) -> None:
    results = retrieve(query, top_k=top_k)

    print(f"\nQuery: {query}")
    if not results:
        print("No results returned.")
        return

    for item in results:
        print(f"\nRank {item['rank']} | distance: {item['distance']:.4f}")
        print(f"Source: {item['metadata'].get('filename')} | chunk {item['metadata'].get('chunk_index')}")
        print(item["text"])


def main() -> None:
    build_vector_store()

    test_queries = [
        "What do students say about Professor Smith's grading style?",
        "How difficult is the Introduction to Programming course according to students?",
        "Which professors are most frequently recommended for introductory computer science courses?",
    ]

    for query in test_queries:
        print_retrieval_results(query, top_k=TOP_K)


if __name__ == "__main__":
    main()