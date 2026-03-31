"""Product progress sync service — progress board and conflict detection."""

from __future__ import annotations

from sqlalchemy.orm import Session
from models import ProductProgress


def update_progress(
    db: Session,
    title: str,
    description: str,
    status: str,
    modules: list[str],
    keywords: list[str],
    author: str,
) -> dict:
    """Create or update a progress item. If title+author match, update existing."""
    existing = (
        db.query(ProductProgress)
        .filter(ProductProgress.title == title, ProductProgress.author == author)
        .first()
    )

    if existing:
        existing.description = description
        existing.status = status
        existing.modules = modules
        existing.keywords = keywords
        db.commit()
        db.refresh(existing)
        return _to_dict(existing)

    item = ProductProgress(
        title=title,
        description=description,
        status=status,
        modules=modules,
        keywords=keywords,
        author=author,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_dict(item)


def get_progress_board(db: Session, author: str | None = None) -> dict:
    """Get the full progress board, grouped by status columns."""
    query = db.query(ProductProgress).order_by(ProductProgress.updated_at.desc())
    if author:
        query = query.filter(ProductProgress.author == author)

    items = query.all()

    board = {
        "planning": [],
        "in_progress": [],
        "review": [],
        "done": [],
    }

    for item in items:
        status_key = item.status if item.status in board else "planning"
        board[status_key].append(_to_dict(item))

    return board


def check_conflicts(
    db: Session, title: str, modules: list[str], keywords: list[str]
) -> list[dict]:
    """Detect conflicts between a proposed item and existing progress items."""
    all_items = (
        db.query(ProductProgress)
        .filter(ProductProgress.status.in_(["planning", "in_progress", "review"]))
        .all()
    )

    conflicts = []
    modules_set = set(m.lower() for m in modules)
    keywords_set = set(k.lower() for k in keywords)

    for item in all_items:
        if item.title.lower() == title.lower():
            continue  # Don't conflict with self

        item_modules = set(m.lower() for m in (item.modules or []))
        item_keywords = set(k.lower() for k in (item.keywords or []))

        # Check module overlap
        module_overlap = modules_set & item_modules
        if module_overlap:
            conflicts.append({
                "type": "module_overlap",
                "your_item": title,
                "existing_item": f"{item.title} ({item.author})",
                "existing_status": item.status,
                "overlap_modules": list(module_overlap),
                "recommendation": (
                    f"Coordinate with {item.author} — both items modify "
                    f"{', '.join(module_overlap)}. Their item is currently "
                    f"in '{item.status}' status."
                ),
            })
            continue  # Don't double-report

        # Check keyword overlap (threshold: 3+ shared keywords)
        keyword_overlap = keywords_set & item_keywords
        if len(keyword_overlap) >= 3:
            conflicts.append({
                "type": "keyword_overlap",
                "your_item": title,
                "existing_item": f"{item.title} ({item.author})",
                "existing_status": item.status,
                "overlap_keywords": list(keyword_overlap),
                "recommendation": (
                    f"Possible overlap with {item.author}'s work — "
                    f"shared keywords: {', '.join(list(keyword_overlap)[:5])}. "
                    f"Consider checking if these features interact."
                ),
            })

    return conflicts


def delete_progress(db: Session, progress_id: int) -> bool:
    """Delete a progress item."""
    item = db.query(ProductProgress).filter(ProductProgress.id == progress_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def _to_dict(item: ProductProgress) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "status": item.status,
        "modules": item.modules or [],
        "keywords": item.keywords or [],
        "author": item.author,
        "created_at": item.created_at.isoformat() if item.created_at else None,
        "updated_at": item.updated_at.isoformat() if item.updated_at else None,
    }
