from __future__ import annotations

import html
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CHUNK_SIZE = 200
CHUNK_OVERLAP = 50
DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"

TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


@dataclass(frozen=True)
class Document:
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class Chunk:
    text: str
    metadata: dict[str, object]


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = TAG_RE.sub(" ", text)
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()


def load_txt_files(documents_dir: Path) -> list[Document]:
    documents: list[Document] = []

    for path in sorted(documents_dir.rglob("*.txt")):
        raw_text = path.read_text(encoding="utf-8", errors="ignore")
        cleaned_text = clean_text(raw_text)
        documents.append(
            Document(
                text=cleaned_text,
                metadata={
                    "filename": path.name,
                    "source_path": str(path),
                },
            )
        )

    return documents


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be 0 or greater")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    if not text:
        return []

    sentences = [sentence.strip() for sentence in SENTENCE_RE.split(text) if sentence.strip()]
    if not sentences:
        return []

    chunks: list[str] = []
    current_sentences: list[str] = []

    def emit_chunk(sentences_to_join: list[str]) -> str:
        return " ".join(sentences_to_join).strip()

    for sentence in sentences:
        candidate_sentences = current_sentences + [sentence]
        candidate_chunk = emit_chunk(candidate_sentences)

        if current_sentences and len(candidate_chunk) > chunk_size:
            chunk = emit_chunk(current_sentences)
            if chunk:
                chunks.append(chunk)

            overlap_text = chunk[-overlap:].strip()
            current_sentences = [overlap_text] if overlap_text else []

            candidate_sentences = current_sentences + [sentence]
            candidate_chunk = emit_chunk(candidate_sentences)

        current_sentences = candidate_sentences

    final_chunk = emit_chunk(current_sentences)
    if final_chunk:
        chunks.append(final_chunk)

    return [chunk for chunk in chunks if chunk]


def build_chunks(documents: Iterable[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []

    for document_index, document in enumerate(documents):
        for chunk_index, chunk_text_value in enumerate(chunk_text(document.text)):
            chunks.append(
                Chunk(
                    text=chunk_text_value,
                    metadata={
                        **document.metadata,
                        "document_index": document_index,
                        "chunk_index": chunk_index,
                        "chunk_size": CHUNK_SIZE,
                        "chunk_overlap": CHUNK_OVERLAP,
                    },
                )
            )

    return chunks


def print_chunk_preview(chunks: list[Chunk], sample_size: int = 5) -> None:
    if not chunks:
        print("No chunks were created.")
        return

    sample = random.sample(chunks, k=min(sample_size, len(chunks)))

    print("\nFive random chunks for inspection:")
    for index, chunk in enumerate(sample, start=1):
        print(f"\n--- Chunk {index} ---")
        print(f"Metadata: {chunk.metadata}")
        print(chunk.text)


def main() -> None:
    documents = load_txt_files(DOCUMENTS_DIR)
    chunks = build_chunks(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")
    print_chunk_preview(chunks)


if __name__ == "__main__":
    main()