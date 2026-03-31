"""REST API routes for template/rule management — used by the Web Admin UI."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
from database import SessionLocal
from services import template_service
from services.file_parser import parse_file, is_supported


router = APIRouter(prefix="/api/templates", tags=["templates"])


class TemplateCreate(BaseModel):
    name: str
    category: str = "requirement"
    content: str


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None


@router.get("")
async def list_templates(category: str = "all"):
    """List all templates, optionally filtered by category."""
    db = SessionLocal()
    try:
        templates = template_service.get_templates(db, category=category)
    finally:
        db.close()
    return {"templates": templates, "count": len(templates)}


@router.get("/{tpl_id}")
async def get_template(tpl_id: int):
    """Get a single template by ID."""
    db = SessionLocal()
    try:
        tpl = template_service.get_template(db, tpl_id)
    finally:
        db.close()
    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")
    return tpl


@router.post("")
async def create_template(body: TemplateCreate):
    """Create a new template from JSON body."""
    db = SessionLocal()
    try:
        tpl = template_service.create_template(db, body.name, body.category, body.content)
    finally:
        db.close()
    return tpl


@router.post("/upload")
async def upload_template(
    file: UploadFile = File(...),
    name: str = Form(None),
    category: str = Form("requirement"),
):
    """Create a template by uploading a file (.md, .txt, .docx).

    The file content is parsed and stored as the template content.
    """
    filename = file.filename or "untitled.txt"

    if not is_supported(filename):
        raise HTTPException(
            status_code=400,
            detail="不支持的文件格式。支持: .md, .txt, .docx, .pdf, .html",
        )

    raw = await file.read()

    try:
        text = parse_file(raw, filename)
    except (RuntimeError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not text.strip():
        raise HTTPException(status_code=400, detail="文件内容为空，无法解析出文本")

    # Use filename as template name if not provided
    template_name = name or filename.rsplit(".", 1)[0]

    # Validate category
    valid_categories = {"requirement", "rule", "checklist"}
    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail=f"无效的分类。可选: {', '.join(valid_categories)}",
        )

    db = SessionLocal()
    try:
        tpl = template_service.create_template(db, template_name, category, text)
    finally:
        db.close()

    return tpl


@router.put("/{tpl_id}")
async def update_template(tpl_id: int, body: TemplateUpdate):
    """Update an existing template."""
    db = SessionLocal()
    try:
        tpl = template_service.update_template(
            db, tpl_id,
            name=body.name,
            category=body.category,
            content=body.content,
        )
    finally:
        db.close()
    if not tpl:
        raise HTTPException(status_code=404, detail="Template not found")
    return tpl


@router.delete("/{tpl_id}")
async def delete_template(tpl_id: int):
    """Delete a template."""
    db = SessionLocal()
    try:
        success = template_service.delete_template(db, tpl_id)
    finally:
        db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"status": "deleted"}
