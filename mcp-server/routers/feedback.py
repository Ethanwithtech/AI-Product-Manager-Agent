"""REST API routes for feedback management — used by the Web Admin UI."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
from services import feedback_service


router = APIRouter(prefix="/api/feedback", tags=["feedback"])


class FeedbackCreate(BaseModel):
    title: str
    content: str
    source_type: str = "general"
    user_segment: str = "unknown"
    author: str
    sentiment_score: int = 0
    themes: Optional[List[str]] = None
    impact_level: str = "medium"


class FeedbackUpdate(BaseModel):
    status: Optional[str] = None
    sentiment_score: Optional[int] = None
    themes: Optional[List[str]] = None
    impact_level: Optional[str] = None
    recommendations: Optional[List[str]] = None


@router.get("")
async def list_feedback(
    source_type: str = "",
    status: str = "",
    user_segment: str = "",
    author: str = "",
):
    """List feedback items with optional filters."""
    db = SessionLocal()
    try:
        items = feedback_service.list_feedback(
            db,
            source_type=source_type or None,
            status=status or None,
            user_segment=user_segment or None,
            author=author or None,
        )
    finally:
        db.close()
    return {"feedback": items, "count": len(items)}


@router.get("/summary")
async def get_summary():
    """Get a summary of all feedback data."""
    db = SessionLocal()
    try:
        summary = feedback_service.get_feedback_summary(db)
    finally:
        db.close()
    return summary


@router.get("/{feedback_id}")
async def get_feedback(feedback_id: int):
    """Get a single feedback item by ID."""
    db = SessionLocal()
    try:
        item = feedback_service.get_feedback(db, feedback_id)
    finally:
        db.close()
    if not item:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return item


@router.post("")
async def create_feedback(body: FeedbackCreate):
    """Create a new feedback item."""
    db = SessionLocal()
    try:
        item = feedback_service.create_feedback(
            db,
            title=body.title,
            content=body.content,
            source_type=body.source_type,
            user_segment=body.user_segment,
            author=body.author,
            sentiment_score=body.sentiment_score,
            themes=body.themes,
            impact_level=body.impact_level,
        )
    finally:
        db.close()
    return item


@router.put("/{feedback_id}")
async def update_feedback(feedback_id: int, body: FeedbackUpdate):
    """Update a feedback item."""
    db = SessionLocal()
    try:
        item = feedback_service.update_feedback(
            db,
            feedback_id,
            status=body.status,
            sentiment_score=body.sentiment_score,
            themes=body.themes,
            impact_level=body.impact_level,
            recommendations=body.recommendations,
        )
    finally:
        db.close()
    if not item:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return item


@router.delete("/{feedback_id}")
async def delete_feedback(feedback_id: int):
    """Delete a feedback item."""
    db = SessionLocal()
    try:
        success = feedback_service.delete_feedback(db, feedback_id)
    finally:
        db.close()
    if not success:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"status": "deleted"}
