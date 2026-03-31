"""Requirement service — CRUD operations for product requirements with keyword extraction."""

from __future__ import annotations

import re
from sqlalchemy.orm import Session
from models import Requirement


def _extract_keywords(text: str) -> list[str]:
    """Extract keywords from requirement content using simple heuristics."""
    # Remove markdown formatting
    clean = re.sub(r"[#*`\[\]()>-]", " ", text)
    clean = re.sub(r"\s+", " ", clean).lower()

    # Extract words that appear in headings or are emphasized
    words = clean.split()
    # Simple frequency-based extraction: words >4 chars that appear 2+ times
    freq: dict[str, int] = {}
    stop_words = {
        "about", "after", "being", "could", "would", "should", "their",
        "there", "these", "those", "which", "while", "under", "other",
        "before", "between", "through", "during", "without", "within",
    }
    for w in words:
        w = re.sub(r"[^a-z0-9]", "", w)
        if len(w) > 4 and w not in stop_words:
            freq[w] = freq.get(w, 0) + 1

    # Return top keywords by frequency
    sorted_kw = sorted(freq.items(), key=lambda x: -x[1])
    return [kw for kw, _ in sorted_kw[:15]]


def create_requirement(
    db: Session, title: str, content: str, modules: list[str], author: str
) -> dict:
    """Create a new requirement document."""
    keywords = _extract_keywords(title + " " + content)
    req = Requirement(
        title=title,
        content=content,
        modules=modules,
        keywords=keywords,
        author=author,
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return _to_dict(req)


def get_requirement(db: Session, req_id: int) -> dict | None:
    """Get a single requirement by ID."""
    req = db.query(Requirement).filter(Requirement.id == req_id).first()
    return _to_dict(req) if req else None


def list_requirements(
    db: Session, status: str | None = None, author: str | None = None
) -> list[dict]:
    """List requirements with optional filters."""
    query = db.query(Requirement).order_by(Requirement.updated_at.desc())
    if status:
        query = query.filter(Requirement.status == status)
    if author:
        query = query.filter(Requirement.author == author)
    return [_to_dict(r) for r in query.all()]


def update_requirement(
    db: Session,
    req_id: int,
    title: str | None = None,
    content: str | None = None,
    status: str | None = None,
    modules: list[str] | None = None,
) -> dict | None:
    """Update a requirement. Returns None if not found."""
    req = db.query(Requirement).filter(Requirement.id == req_id).first()
    if not req:
        return None

    if title is not None:
        req.title = title
    if content is not None:
        req.content = content
        req.keywords = _extract_keywords(req.title + " " + content)
    if status is not None:
        req.status = status
    if modules is not None:
        req.modules = modules

    db.commit()
    db.refresh(req)
    return _to_dict(req)


def delete_requirement(db: Session, req_id: int) -> bool:
    """Delete a requirement by ID."""
    req = db.query(Requirement).filter(Requirement.id == req_id).first()
    if not req:
        return False
    db.delete(req)
    db.commit()
    return True


def _to_dict(req: Requirement) -> dict:
    return {
        "id": req.id,
        "title": req.title,
        "content": req.content,
        "status": req.status,
        "modules": req.modules or [],
        "keywords": req.keywords or [],
        "author": req.author,
        "created_at": req.created_at.isoformat() if req.created_at else None,
        "updated_at": req.updated_at.isoformat() if req.updated_at else None,
    }
