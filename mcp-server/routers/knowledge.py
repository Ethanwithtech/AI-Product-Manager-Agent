"""REST API routes for knowledge base management — used by the Web Admin UI."""

from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services import knowledge_service
from services.file_parser import parse_file, get_doc_type, is_supported
from database import SessionLocal
from models import KnowledgeDocument

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.get("")
async def list_documents():
    """List all documents in the knowledge base."""
    stats = knowledge_service.get_stats()
    # Enrich with SQLite metadata
    db = SessionLocal()
    try:
        db_docs = db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()
        docs_with_meta = []
        for doc in db_docs:
            docs_with_meta.append({
                "id": doc.id,
                "title": doc.title,
                "doc_type": doc.doc_type,
                "chunks": doc.chunks,
                "content_preview": doc.content_preview,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
            })
    finally:
        db.close()
    return {"documents": docs_with_meta, "stats": stats}


@router.post("")
async def upload_document(
    title: str = Form(...),
    doc_type: str = Form(None),
    content: str = Form(None),
    file: UploadFile = File(None),
):
    """Upload a document to the knowledge base.

    Supports: .md, .txt, .pdf, .docx, .html
    Either provide 'content' (raw text) or 'file' (uploaded file).
    """
    if file:
        filename = file.filename or "untitled.txt"

        # Validate file type
        if not is_supported(filename):
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式。支持: .md, .txt, .pdf, .docx, .html",
            )

        raw = await file.read()

        # Parse file content based on extension
        try:
            text = parse_file(raw, filename)
        except (RuntimeError, ValueError) as e:
            raise HTTPException(status_code=400, detail=str(e))

        if not title or title == "Untitled":
            title = filename

        # Auto-detect doc_type from file extension if not provided
        if not doc_type:
            doc_type = get_doc_type(filename)
    elif content:
        text = content
        if not doc_type:
            doc_type = "md"
    else:
        raise HTTPException(status_code=400, detail="Provide either 'content' or 'file'")

    if not text.strip():
        raise HTTPException(status_code=400, detail="文件内容为空，无法解析出文本")

    chunks = knowledge_service.add_document(title, text, doc_type)

    db = SessionLocal()
    try:
        doc = KnowledgeDocument(
            title=title,
            doc_type=doc_type,
            chunks=chunks,
            content_preview=text[:500],
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        doc_id = doc.id
    finally:
        db.close()

    return {"id": doc_id, "title": title, "doc_type": doc_type, "chunks": chunks}


@router.delete("/{doc_id}")
async def delete_document(doc_id: int):
    """Delete a document from the knowledge base."""
    db = SessionLocal()
    try:
        doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == doc_id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        knowledge_service.delete_document(doc.title)
        db.delete(doc)
        db.commit()
    finally:
        db.close()
    return {"status": "deleted"}


@router.post("/search")
async def search_documents(query: str = Form(...), top_k: int = Form(5)):
    """Test semantic search on the knowledge base."""
    results = knowledge_service.search(query, top_k=top_k)
    return {"query": query, "results": results}
