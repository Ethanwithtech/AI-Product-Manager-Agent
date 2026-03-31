"""Template service — CRUD operations for requirement templates and team rules."""

from __future__ import annotations

from sqlalchemy.orm import Session
from models import Template


def create_template(
    db: Session, name: str, category: str, content: str
) -> dict:
    """Create a new template."""
    tpl = Template(name=name, category=category, content=content)
    db.add(tpl)
    db.commit()
    db.refresh(tpl)
    return _to_dict(tpl)


def get_template(db: Session, template_id: int) -> dict | None:
    """Get a single template by ID."""
    tpl = db.query(Template).filter(Template.id == template_id).first()
    return _to_dict(tpl) if tpl else None


def get_templates(db: Session, category: str = "all") -> list[dict]:
    """List templates, optionally filtered by category."""
    query = db.query(Template).order_by(Template.updated_at.desc())
    if category != "all":
        query = query.filter(Template.category == category)
    return [_to_dict(t) for t in query.all()]


def update_template(
    db: Session,
    template_id: int,
    name: str | None = None,
    category: str | None = None,
    content: str | None = None,
) -> dict | None:
    """Update a template. Returns None if not found."""
    tpl = db.query(Template).filter(Template.id == template_id).first()
    if not tpl:
        return None
    if name is not None:
        tpl.name = name
    if category is not None:
        tpl.category = category
    if content is not None:
        tpl.content = content
    db.commit()
    db.refresh(tpl)
    return _to_dict(tpl)


def delete_template(db: Session, template_id: int) -> bool:
    """Delete a template."""
    tpl = db.query(Template).filter(Template.id == template_id).first()
    if not tpl:
        return False
    db.delete(tpl)
    db.commit()
    return True


def _to_dict(tpl: Template) -> dict:
    return {
        "id": tpl.id,
        "name": tpl.name,
        "category": tpl.category,
        "content": tpl.content,
        "created_at": tpl.created_at.isoformat() if tpl.created_at else None,
        "updated_at": tpl.updated_at.isoformat() if tpl.updated_at else None,
    }
