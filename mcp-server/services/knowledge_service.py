"""Knowledge base service — ChromaDB document embedding and semantic search."""

from __future__ import annotations

import hashlib
import chromadb
from config import settings


def _get_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(
        path=settings.chroma_persist_dir,
    )


def _get_collection(client: chromadb.ClientAPI):
    return client.get_or_create_collection(
        name="product_knowledge",
        metadata={"hnsw:space": "cosine"},
    )


def chunk_text(text: str, max_chars: int = 1000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks by paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current.strip())
            # Keep overlap from previous chunk
            words = current.split()
            overlap_text = " ".join(words[-overlap // 5 :]) if len(words) > overlap // 5 else ""
            current = overlap_text + "\n\n" + para if overlap_text else para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current.strip())

    return chunks if chunks else [text[:max_chars]]


def add_document(title: str, content: str, doc_type: str = "md") -> int:
    """Chunk, embed and store a document. Returns number of chunks created."""
    client = _get_client()
    collection = _get_collection(client)

    # Generate a stable doc ID prefix from title
    doc_prefix = hashlib.md5(title.encode()).hexdigest()[:8]

    # Remove any existing chunks for this document (re-upload)
    existing = collection.get(where={"doc_title": title})
    if existing and existing["ids"]:
        collection.delete(ids=existing["ids"])

    chunks = chunk_text(content)
    ids = [f"{doc_prefix}_{i}" for i in range(len(chunks))]
    metadatas = [
        {"doc_title": title, "doc_type": doc_type, "chunk_index": i}
        for i in range(len(chunks))
    ]

    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    return len(chunks)


def search(query: str, top_k: int = 5) -> list[dict]:
    """Semantic search over the knowledge base. Returns ranked results."""
    client = _get_client()
    collection = _get_collection(client)

    if collection.count() == 0:
        return []

    results = collection.query(query_texts=[query], n_results=min(top_k, collection.count()))

    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i] if results.get("distances") else None,
        })

    return output


def list_documents() -> list[dict]:
    """List all unique documents in the knowledge base."""
    client = _get_client()
    collection = _get_collection(client)

    if collection.count() == 0:
        return []

    all_items = collection.get(include=["metadatas"])
    doc_map: dict[str, dict] = {}

    for meta in all_items["metadatas"]:
        title = meta.get("doc_title", "Unknown")
        if title not in doc_map:
            doc_map[title] = {
                "title": title,
                "doc_type": meta.get("doc_type", "md"),
                "chunks": 0,
            }
        doc_map[title]["chunks"] += 1

    return list(doc_map.values())


def delete_document(title: str) -> bool:
    """Delete all chunks for a document by title."""
    client = _get_client()
    collection = _get_collection(client)

    existing = collection.get(where={"doc_title": title})
    if existing and existing["ids"]:
        collection.delete(ids=existing["ids"])
        return True
    return False


def get_stats() -> dict:
    """Get knowledge base statistics."""
    client = _get_client()
    collection = _get_collection(client)
    docs = list_documents()
    return {
        "total_chunks": collection.count(),
        "total_documents": len(docs),
        "documents": docs,
    }
