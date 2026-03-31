from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from database import Base


class Requirement(Base):
    """Product requirement / PRD document."""

    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False, index=True)
    content = Column(Text, nullable=False)  # Markdown PRD content
    status = Column(String(32), default="draft")  # draft | review | approved | archived
    modules = Column(JSON, default=list)  # ["checkout", "payments"]
    keywords = Column(JSON, default=list)  # auto-extracted keywords
    author = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProductProgress(Base):
    """Product progress board item — tracks what each PM is working on."""

    __tablename__ = "product_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False, index=True)
    description = Column(Text, default="")
    status = Column(String(32), default="planning")  # planning | in_progress | review | done
    modules = Column(JSON, default=list)
    keywords = Column(JSON, default=list)
    author = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Template(Base):
    """Reusable templates and team rules."""

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False, unique=True)
    category = Column(String(64), default="requirement")  # requirement | rule | checklist
    content = Column(Text, nullable=False)  # Markdown template content
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class KnowledgeDocument(Base):
    """Metadata for documents stored in the vector database."""

    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    doc_type = Column(String(16), default="md")  # md | txt | pdf
    chunks = Column(Integer, default=0)  # number of chunks in ChromaDB
    content_preview = Column(Text, default="")  # first 500 chars for display
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FeedbackItem(Base):
    """User feedback item — bids, reviews, tickets, interviews, surveys."""

    __tablename__ = "feedback_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False, index=True)
    source_type = Column(String(32), default="general")  # bid | review | ticket | interview | survey | general
    content = Column(Text, nullable=False)  # Raw feedback content
    user_segment = Column(String(64), default="unknown")  # enterprise | core | new | churned | unknown
    sentiment_score = Column(Integer, default=0)  # -2 to +2
    themes = Column(JSON, default=list)  # ["数据导出", "操作效率"]
    impact_level = Column(String(16), default="medium")  # low | medium | high | critical
    status = Column(String(32), default="new")  # new | analyzing | analyzed | actioned | archived
    recommendations = Column(JSON, default=list)  # AI-generated recommendations
    author = Column(String(128), nullable=False)  # PM who collected this
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
