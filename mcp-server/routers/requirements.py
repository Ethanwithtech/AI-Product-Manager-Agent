"""REST API routes for requirement management — used by the Web Admin UI."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
from services import requirement_service


router = APIRouter(prefix="/api/requirements", tags=["requirements"])


class RequirementCreate(BaseModel):
    title: str
    content: str
    modules: List[str] = []
    author: str


class RequirementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    modules: Optional[List[str]] = None


@router.get("")
async def list_requirements(status: str = "", author: str = ""):
    """List all requirements with optional filters."""
    db = SessionLocal()
    try:
        reqs = requirement_service.list_requirements(
            db, status=status or None, author=author or None
        )
    finally:
        db.close()
    return {"requirements": reqs, "count": len(reqs)}


@router.get("/{req_id}")
async def get_requirement(req_id: int):
    """Get a single requirement by ID."""
    db = SessionLocal()
    try:
        req = requirement_service.get_requirement(db, req_id)
    finally:
        db.close()
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return req


@router.post("")
async def create_requirement(body: RequirementCreate):
    """Create a new requirement."""
    db = SessionLocal()
    try:
        req = requirement_service.create_requirement(
            db, body.title, body.content, body.modules, body.author
        )
    finally:
        db.close()
    return req


@router.put("/{req_id}")
async def update_requirement(req_id: int, body: RequirementUpdate):
    """Update an existing requirement."""
    db = SessionLocal()
    try:
        req = requirement_service.update_requirement(
            db, req_id,
            title=body.title,
            content=body.content,
            status=body.status,
            modules=body.modules,
        )
    finally:
        db.close()
    if not req:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return req


@router.delete("/{req_id}")
async def delete_requirement(req_id: int):
    """Delete a requirement."""
    db = SessionLocal()
    try:
        success = requirement_service.delete_requirement(db, req_id)
    finally:
        db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return {"status": "deleted"}
