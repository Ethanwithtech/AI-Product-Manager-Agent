"""MCP Tool definitions — 12 tools for PM Team Hub.

These tools are exposed via the MCP protocol and callable from CodeBuddy.
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import json

from database import SessionLocal
from services import knowledge_service, requirement_service, sync_service, template_service

server = Server("pm-team-hub")


# ─────────────────────────── Knowledge Base Tools ───────────────────────────


@server.tool()
async def search_knowledge(query: str, top_k: int = 5) -> list[TextContent]:
    """Search the product knowledge base for relevant document chunks.

    Use this before writing requirements, making product decisions, or
    generating UI code — to ground your work in actual product context.

    Args:
        query: Natural language question (e.g., "how does our checkout flow work?")
        top_k: Maximum number of results to return (default: 5)
    """
    results = knowledge_service.search(query, top_k=top_k)
    if not results:
        return [TextContent(type="text", text=json.dumps({
            "results": [],
            "message": "No relevant documents found. Consider uploading product docs to the knowledge base."
        }))]
    return [TextContent(type="text", text=json.dumps({"results": results}, default=str))]


@server.tool()
async def add_knowledge_document(title: str, content: str, doc_type: str = "md") -> list[TextContent]:
    """Upload a document to the product knowledge base.

    The document will be chunked and embedded for semantic search.
    Supported types: md (markdown), txt (plain text).

    Args:
        title: Descriptive document title (e.g., "Checkout Flow Architecture")
        content: Full document content
        doc_type: Document type — "md" or "txt"
    """
    chunks = knowledge_service.add_document(title, content, doc_type)
    # Also record metadata in SQLite
    db = SessionLocal()
    try:
        from models import KnowledgeDocument
        doc = KnowledgeDocument(
            title=title,
            doc_type=doc_type,
            chunks=chunks,
            content_preview=content[:500],
        )
        db.add(doc)
        db.commit()
    finally:
        db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "title": title,
        "chunks_created": chunks,
        "message": f"Document '{title}' uploaded successfully with {chunks} chunks."
    }))]


@server.tool()
async def list_knowledge_documents() -> list[TextContent]:
    """List all documents in the knowledge base with metadata."""
    stats = knowledge_service.get_stats()
    return [TextContent(type="text", text=json.dumps(stats, default=str))]


@server.tool()
async def delete_knowledge_document(title: str) -> list[TextContent]:
    """Delete a document from the knowledge base by title.

    Args:
        title: Exact title of the document to delete
    """
    success = knowledge_service.delete_document(title)
    if success:
        # Also remove from SQLite metadata
        db = SessionLocal()
        try:
            from models import KnowledgeDocument
            db.query(KnowledgeDocument).filter(KnowledgeDocument.title == title).delete()
            db.commit()
        finally:
            db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success" if success else "not_found",
        "message": f"Document '{title}' deleted." if success else f"Document '{title}' not found."
    }))]


# ─────────────────────────── Requirement Tools ───────────────────────────


@server.tool()
async def create_requirement(
    title: str, content: str, modules: list[str], author: str
) -> list[TextContent]:
    """Create and store a requirement document (PRD) in the shared repository.

    Also automatically checks for conflicts with other PMs' work.

    Args:
        title: Requirement title (e.g., "Smart Notification System")
        content: Full PRD content in Markdown format
        modules: Product modules this requirement affects (e.g., ["notifications", "user-preferences"])
        author: PM name who created this requirement
    """
    db = SessionLocal()
    try:
        req = requirement_service.create_requirement(db, title, content, modules, author)
        conflicts = sync_service.check_conflicts(db, title, modules, req.get("keywords", []))
    finally:
        db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "requirement": req,
        "conflicts": conflicts,
        "message": (
            f"Requirement '{title}' created (ID: {req['id']}). "
            + (f"⚠️ {len(conflicts)} potential conflict(s) detected." if conflicts else "No conflicts detected.")
        )
    }, default=str))]


@server.tool()
async def get_requirement(requirement_id: int) -> list[TextContent]:
    """Get a single requirement document by ID.

    Args:
        requirement_id: The numeric ID of the requirement
    """
    db = SessionLocal()
    try:
        req = requirement_service.get_requirement(db, requirement_id)
    finally:
        db.close()

    if not req:
        return [TextContent(type="text", text=json.dumps({
            "status": "not_found",
            "message": f"Requirement ID {requirement_id} not found."
        }))]

    return [TextContent(type="text", text=json.dumps({"status": "success", "requirement": req}, default=str))]


@server.tool()
async def list_requirements(status: str = "", author: str = "") -> list[TextContent]:
    """List requirement documents with optional filters.

    Args:
        status: Filter by status — "draft", "review", "approved", "archived" (empty = all)
        author: Filter by author name (empty = all)
    """
    db = SessionLocal()
    try:
        reqs = requirement_service.list_requirements(
            db,
            status=status or None,
            author=author or None,
        )
    finally:
        db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "count": len(reqs),
        "requirements": reqs,
    }, default=str))]


@server.tool()
async def update_requirement(
    requirement_id: int,
    title: str = "",
    content: str = "",
    status: str = "",
    modules: str = "",
) -> list[TextContent]:
    """Update an existing requirement document.

    Args:
        requirement_id: The ID of the requirement to update
        title: New title (empty = no change)
        content: New content (empty = no change)
        status: New status (empty = no change)
        modules: Comma-separated module names (empty = no change)
    """
    db = SessionLocal()
    try:
        modules_list = [m.strip() for m in modules.split(",") if m.strip()] if modules else None
        req = requirement_service.update_requirement(
            db,
            requirement_id,
            title=title or None,
            content=content or None,
            status=status or None,
            modules=modules_list,
        )
    finally:
        db.close()

    if not req:
        return [TextContent(type="text", text=json.dumps({
            "status": "not_found",
            "message": f"Requirement ID {requirement_id} not found."
        }))]

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "requirement": req,
        "message": f"Requirement '{req['title']}' updated."
    }, default=str))]


# ─────────────────────────── Progress Sync Tools ───────────────────────────


@server.tool()
async def update_progress(
    title: str,
    description: str,
    status: str,
    modules: list[str],
    keywords: list[str],
    author: str,
) -> list[TextContent]:
    """Update the product progress board with your current work item.

    If a matching title+author exists, it updates the existing entry.
    Otherwise creates a new one.

    Args:
        title: Work item title (e.g., "Smart Notifications v2")
        description: Brief description of the work
        status: Current status — "planning", "in_progress", "review", or "done"
        modules: Product modules involved (e.g., ["notifications", "settings"])
        keywords: Relevant keywords for conflict detection
        author: Your PM name
    """
    db = SessionLocal()
    try:
        item = sync_service.update_progress(db, title, description, status, modules, keywords, author)
    finally:
        db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "progress_item": item,
        "message": f"Progress updated: '{title}' is now in '{status}' status."
    }, default=str))]


@server.tool()
async def get_progress_board(author: str = "") -> list[TextContent]:
    """Get the full product progress board showing all PMs' work.

    Returns items grouped by status: planning, in_progress, review, done.

    Args:
        author: Filter by PM name (empty = show all PMs)
    """
    db = SessionLocal()
    try:
        board = sync_service.get_progress_board(db, author=author or None)
    finally:
        db.close()

    total = sum(len(v) for v in board.values())
    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "total_items": total,
        "board": board,
    }, default=str))]


@server.tool()
async def check_conflicts(
    title: str, modules: list[str], keywords: list[str]
) -> list[TextContent]:
    """Check for potential conflicts between your work and other PMs' items.

    Detects module overlaps and keyword overlaps with items in
    planning/in_progress/review status.

    Args:
        title: Your work item title
        modules: Product modules your work affects
        keywords: Keywords related to your work
    """
    db = SessionLocal()
    try:
        conflicts = sync_service.check_conflicts(db, title, modules, keywords)
    finally:
        db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "conflicts_found": len(conflicts),
        "conflicts": conflicts,
        "message": (
            f"Found {len(conflicts)} potential conflict(s)."
            if conflicts else "No conflicts detected — you're clear to proceed."
        )
    }, default=str))]


# ─────────────────────────── Template Tools ───────────────────────────


@server.tool()
async def get_templates(category: str = "all") -> list[TextContent]:
    """Get requirement templates and team rules.

    Args:
        category: Filter by category — "requirement", "rule", "checklist" (or "all")
    """
    db = SessionLocal()
    try:
        templates = template_service.get_templates(db, category=category)
    finally:
        db.close()

    return [TextContent(type="text", text=json.dumps({
        "status": "success",
        "count": len(templates),
        "templates": templates,
    }, default=str))]
