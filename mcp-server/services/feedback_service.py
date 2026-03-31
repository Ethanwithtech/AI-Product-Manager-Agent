"""Feedback service — CRUD operations for user feedback with theme analysis."""

from __future__ import annotations

import re
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from models import FeedbackItem


def _extract_themes(text: str) -> List[str]:
    """Extract potential themes from feedback content using keyword frequency."""
    clean = re.sub(r"[#*`\[\]()>-]", " ", text)
    clean = re.sub(r"\s+", " ", clean).lower()

    words = clean.split()
    stop_words = {
        "about", "after", "being", "could", "would", "should", "their",
        "there", "these", "those", "which", "while", "under", "other",
        "before", "between", "through", "during", "without", "within",
        "这个", "那个", "可以", "不能", "已经", "需要", "使用", "功能",
    }
    freq: Dict[str, int] = {}
    for w in words:
        w = re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", w)
        if len(w) > 1 and w not in stop_words:
            freq[w] = freq.get(w, 0) + 1

    sorted_kw = sorted(freq.items(), key=lambda x: -x[1])
    return [kw for kw, count in sorted_kw[:10] if count >= 1]


def create_feedback(
    db: Session,
    title: str,
    content: str,
    source_type: str,
    user_segment: str,
    author: str,
    sentiment_score: int = 0,
    themes: Optional[List[str]] = None,
    impact_level: str = "medium",
) -> dict:
    """Create a new feedback item."""
    auto_themes = themes or _extract_themes(title + " " + content)
    item = FeedbackItem(
        title=title,
        content=content,
        source_type=source_type,
        user_segment=user_segment,
        sentiment_score=max(-2, min(2, sentiment_score)),
        themes=auto_themes,
        impact_level=impact_level,
        author=author,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_dict(item)


def get_feedback(db: Session, feedback_id: int) -> dict | None:
    """Get a single feedback item by ID."""
    item = db.query(FeedbackItem).filter(FeedbackItem.id == feedback_id).first()
    return _to_dict(item) if item else None


def list_feedback(
    db: Session,
    source_type: Optional[str] = None,
    status: Optional[str] = None,
    user_segment: Optional[str] = None,
    author: Optional[str] = None,
) -> List[dict]:
    """List feedback items with optional filters."""
    query = db.query(FeedbackItem).order_by(FeedbackItem.updated_at.desc())
    if source_type:
        query = query.filter(FeedbackItem.source_type == source_type)
    if status:
        query = query.filter(FeedbackItem.status == status)
    if user_segment:
        query = query.filter(FeedbackItem.user_segment == user_segment)
    if author:
        query = query.filter(FeedbackItem.author == author)
    return [_to_dict(item) for item in query.all()]


def update_feedback(
    db: Session,
    feedback_id: int,
    status: Optional[str] = None,
    sentiment_score: Optional[int] = None,
    themes: Optional[List[str]] = None,
    impact_level: Optional[str] = None,
    recommendations: Optional[List[str]] = None,
) -> Optional[dict]:
    """Update a feedback item."""
    item = db.query(FeedbackItem).filter(FeedbackItem.id == feedback_id).first()
    if not item:
        return None
    if status is not None:
        item.status = status
    if sentiment_score is not None:
        item.sentiment_score = max(-2, min(2, sentiment_score))
    if themes is not None:
        item.themes = themes
    if impact_level is not None:
        item.impact_level = impact_level
    if recommendations is not None:
        item.recommendations = recommendations
    db.commit()
    db.refresh(item)
    return _to_dict(item)


def delete_feedback(db: Session, feedback_id: int) -> bool:
    """Delete a feedback item."""
    item = db.query(FeedbackItem).filter(FeedbackItem.id == feedback_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def get_feedback_summary(db: Session) -> dict:
    """Get a summary of all feedback — counts by source, sentiment distribution, top themes."""
    all_items = db.query(FeedbackItem).all()

    by_source: Dict[str, int] = {}
    by_status: Dict[str, int] = {}
    by_segment: Dict[str, int] = {}
    sentiment_dist = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0}
    theme_freq: Dict[str, int] = {}

    for item in all_items:
        by_source[item.source_type] = by_source.get(item.source_type, 0) + 1
        by_status[item.status] = by_status.get(item.status, 0) + 1
        by_segment[item.user_segment] = by_segment.get(item.user_segment, 0) + 1
        sentiment_dist[str(item.sentiment_score)] = sentiment_dist.get(str(item.sentiment_score), 0) + 1
        for theme in (item.themes or []):
            theme_freq[theme] = theme_freq.get(theme, 0) + 1

    top_themes = sorted(theme_freq.items(), key=lambda x: -x[1])[:10]

    return {
        "total": len(all_items),
        "by_source": by_source,
        "by_status": by_status,
        "by_segment": by_segment,
        "sentiment_distribution": sentiment_dist,
        "top_themes": [{"theme": t, "count": c} for t, c in top_themes],
    }


def _to_dict(item: FeedbackItem) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "source_type": item.source_type,
        "content": item.content,
        "user_segment": item.user_segment,
        "sentiment_score": item.sentiment_score,
        "themes": item.themes or [],
        "impact_level": item.impact_level,
        "status": item.status,
        "recommendations": item.recommendations or [],
        "author": item.author,
        "created_at": item.created_at.isoformat() if item.created_at else None,
        "updated_at": item.updated_at.isoformat() if item.updated_at else None,
    }
