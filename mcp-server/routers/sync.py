"""REST API routes for product progress sync — used by the Web Admin UI."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from database import SessionLocal
from services import sync_service


router = APIRouter(prefix="/api/progress", tags=["progress"])


class ProgressUpdate(BaseModel):
    title: str
    description: str = ""
    status: str = "planning"
    modules: List[str] = []
    keywords: List[str] = []
    author: str


class ConflictCheck(BaseModel):
    title: str
    modules: List[str] = []
    keywords: List[str] = []


@router.get("")
async def get_progress_board(author: str = ""):
    """Get the full progress board."""
    db = SessionLocal()
    try:
        board = sync_service.get_progress_board(db, author=author or None)
    finally:
        db.close()
    total = sum(len(v) for v in board.values())
    return {"board": board, "total_items": total}


@router.post("")
async def update_progress(body: ProgressUpdate):
    """Create or update a progress item."""
    db = SessionLocal()
    try:
        item = sync_service.update_progress(
            db, body.title, body.description, body.status,
            body.modules, body.keywords, body.author
        )
    finally:
        db.close()
    return item


@router.post("/conflicts")
async def check_conflicts(body: ConflictCheck):
    """Check for conflicts with existing progress items."""
    db = SessionLocal()
    try:
        conflicts = sync_service.check_conflicts(db, body.title, body.modules, body.keywords)
    finally:
        db.close()
    return {"conflicts": conflicts, "count": len(conflicts)}


@router.delete("/{progress_id}")
async def delete_progress(progress_id: int):
    """Delete a progress item."""
    db = SessionLocal()
    try:
        success = sync_service.delete_progress(db, progress_id)
    finally:
        db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Progress item not found")
    return {"status": "deleted"}
