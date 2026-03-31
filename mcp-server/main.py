"""PM Team Hub — MCP Server + REST API for shared product data.

This is the main entry point. It serves two protocols:
1. MCP protocol (SSE) at /mcp — for CodeBuddy MCP Client connections (requires mcp package)
2. REST API at /api/* — for the Web Admin management interface
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the mcp-server directory is on the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import settings
from database import init_db
from routers import knowledge, requirements, sync, templates, feedback

# ─────────────────────────── Optional MCP Support ───────────────────────────

MCP_AVAILABLE = False
try:
    from mcp.server.fastmcp import FastMCP
    import mcp_tools  # noqa: F401
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  MCP SDK not installed — MCP protocol endpoints disabled.")
    print("   REST API will still work. Install with: pip install 'mcp[cli]>=1.3.0'")


# ─────────────────────────── FastAPI Application ───────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events."""
    # Create data directory if needed
    os.makedirs("data", exist_ok=True)
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)

    # Initialize database tables
    init_db()
    print(f"✅ PM Team Hub started on {settings.host}:{settings.port}")
    if MCP_AVAILABLE:
        print(f"   MCP endpoint: http://{settings.host}:{settings.port}/mcp")
    print(f"   REST API:     http://{settings.host}:{settings.port}/api")
    print(f"   API Docs:     http://{settings.host}:{settings.port}/docs")
    print(f"   Skills dir:   {settings.skills_dir}")
    yield
    print("👋 PM Team Hub shutting down")


app = FastAPI(
    title="PM Team Hub",
    description="MCP Server + REST API for PM team collaboration — knowledge base, requirements, progress sync, templates.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for development (small team internal tool)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────── Mount REST API Routes ───────────────────────────

app.include_router(knowledge.router)
app.include_router(requirements.router)
app.include_router(sync.router)
app.include_router(templates.router)
app.include_router(feedback.router)


# ─────────────────────────── Mount MCP SSE Endpoint (optional) ───────────────

if MCP_AVAILABLE:
    mcp_app = FastMCP("pm-team-hub")
    from mcp_tools import server as mcp_server


@app.get("/mcp/sse")
async def mcp_sse_info():
    """Info endpoint for MCP SSE discovery."""
    return {
        "name": "pm-team-hub",
        "version": "1.0.0",
        "mcp_available": MCP_AVAILABLE,
        "description": "PM Team Hub — shared knowledge base, requirements, progress sync, and templates.",
        "tools": [
            "search_knowledge", "add_knowledge_document", "list_knowledge_documents",
            "delete_knowledge_document", "create_requirement", "get_requirement",
            "list_requirements", "update_requirement", "update_progress",
            "get_progress_board", "check_conflicts", "get_templates",
        ]
    }


# ─────────────────────────── Health Check ───────────────────────────

@app.get("/")
async def root():
    return {
        "name": "PM Team Hub",
        "version": "1.0.0",
        "status": "running",
        "mcp_available": MCP_AVAILABLE,
        "endpoints": {
            "mcp": "/mcp/sse",
            "api": "/api",
            "docs": "/docs",
        }
    }


@app.get("/api")
async def api_root():
    return {
        "knowledge": "/api/knowledge",
        "requirements": "/api/requirements",
        "progress": "/api/progress",
        "templates": "/api/templates",
        "feedback": "/api/feedback",
    }


# ─────────────────────────── Seed Demo Data ───────────────────────────

def seed_demo_data():
    """Seed database with demo data for development preview."""
    from database import SessionLocal
    from models import Requirement, ProductProgress, Template, FeedbackItem

    db = SessionLocal()
    try:
        # Only seed if database is empty
        if db.query(Requirement).count() > 0:
            return

        # Demo requirements
        demo_reqs = [
            Requirement(
                title="智能通知系统 V2",
                content="# 智能通知系统 V2\n\n## 背景\n用户反馈当前通知系统过于频繁，缺乏智能分类...\n\n## 目标\n- 支持通知优先级分类（紧急/重要/普通）\n- 智能静默时段\n- 按用户行为聚合通知\n\n## 功能需求\n### P0 - 通知分级\n用户可设置通知优先级规则...\n\n### P1 - 智能聚合\n相似通知在30分钟窗口内聚合展示...",
                status="review",
                modules=["notifications", "user-preferences"],
                keywords=["通知", "notification", "priority", "聚合"],
                author="Alice",
            ),
            Requirement(
                title="新用户引导流程优化",
                content="# 新用户引导流程优化\n\n## 背景\n当前新用户注册后流失率高达45%...\n\n## 目标\n- 7日留存率提升至60%\n- 引导完成率提升至80%\n\n## 方案\n### 渐进式引导\n分3步完成核心功能引导...",
                status="approved",
                modules=["onboarding", "user-profile"],
                keywords=["引导", "onboarding", "留存", "retention"],
                author="Bob",
            ),
            Requirement(
                title="数据看板 MVP",
                content="# 数据看板 MVP\n\n## 背景\n产品团队需要实时查看核心指标...\n\n## 功能\n- DAU/MAU 趋势图\n- 转化漏斗\n- 自定义时间范围",
                status="draft",
                modules=["analytics", "dashboard"],
                keywords=["数据", "analytics", "dashboard", "指标"],
                author="Alice",
            ),
        ]

        # Demo progress items
        demo_progress = [
            ProductProgress(
                title="智能通知系统 V2",
                description="通知分级功能开发中，已完成后端API",
                status="in_progress",
                modules=["notifications", "user-preferences"],
                keywords=["通知", "notification", "priority"],
                author="Alice",
            ),
            ProductProgress(
                title="新用户引导流程优化",
                description="设计稿已通过评审，准备进入开发",
                status="review",
                modules=["onboarding", "user-profile"],
                keywords=["引导", "onboarding", "留存"],
                author="Bob",
            ),
            ProductProgress(
                title="数据看板 MVP",
                description="正在调研可视化方案",
                status="planning",
                modules=["analytics", "dashboard"],
                keywords=["数据", "analytics", "dashboard"],
                author="Alice",
            ),
            ProductProgress(
                title="支付流程安全升级",
                description="已完成3D Secure集成",
                status="done",
                modules=["payments", "security"],
                keywords=["支付", "payment", "安全", "security"],
                author="Charlie",
            ),
        ]

        # Demo templates
        demo_templates = [
            Template(
                name="标准PRD模板",
                category="requirement",
                content="# {产品需求标题}\n\n## 1. 背景与目标\n\n### 1.1 业务背景\n[描述需求的业务上下文]\n\n### 1.2 目标\n- 目标1\n- 目标2\n\n## 2. 用户故事\n\n作为 [角色]，我希望 [功能]，以便 [价值]。\n\n## 3. 功能需求\n\n### 3.1 P0 - 核心功能\n[必须实现的功能]\n\n### 3.2 P1 - 重要功能\n[重要但非必须]\n\n### 3.3 P2 - 锦上添花\n[有则更好]\n\n## 4. 非功能需求\n\n- 性能: [响应时间要求]\n- 安全: [安全要求]\n\n## 5. 数据需求\n\n[需要的数据指标]\n\n## 6. 里程碑\n\n| 阶段 | 时间 | 交付物 |\n|------|------|--------|\n| 设计 | W1-W2 | 设计稿 |\n| 开发 | W3-W5 | 功能代码 |\n| 测试 | W6 | 测试报告 |\n\n## 7. 风险与依赖\n\n- 风险: [潜在风险]\n- 依赖: [外部依赖]",
            ),
            Template(
                name="Sprint评审检查清单",
                category="checklist",
                content="# Sprint 评审检查清单\n\n## 需求确认\n- [ ] 所有User Story已明确验收标准\n- [ ] 优先级已与利益相关者确认\n- [ ] 技术方案已评审通过\n\n## 设计质量\n- [ ] 交互设计已完成可用性测试\n- [ ] UI稿已标注完成\n- [ ] 响应式适配方案已确认\n\n## 开发交付\n- [ ] 核心功能全部完成\n- [ ] 单元测试覆盖率 > 80%\n- [ ] 无P0/P1 Bug遗留\n\n## 发布就绪\n- [ ] 灰度方案已制定\n- [ ] 回滚方案已确认\n- [ ] 监控告警已配置",
            ),
            Template(
                name="产品规范-命名约定",
                category="rule",
                content="# 产品规范 - 命名约定\n\n## 模块命名\n- 使用 kebab-case (如 `user-profile`, `data-analytics`)\n- 不超过3个单词\n- 避免缩写，除非是团队公认的（如 API, UI, UX）\n\n## 需求编号\n- 格式: `PRD-{YYYY}-{序号}`\n- 示例: `PRD-2026-042`\n\n## 状态流转\n```\ndraft → review → approved → archived\n        ↓\n      rejected (回到 draft)\n```\n\n## 优先级定义\n| 等级 | 含义 | SLA |\n|------|------|-----|\n| P0 | 必须本Sprint完成 | 1周内 |\n| P1 | 重要，本版本完成 | 2周内 |\n| P2 | 有则更好 | 下版本 |",
            ),
        ]

        for item in demo_reqs + demo_progress + demo_templates:
            db.add(item)

        # Demo feedback items
        demo_feedback = [
            FeedbackItem(
                title="XX企业投标反馈 — 数据导出能力不足",
                source_type="bid",
                content="评审反馈：\n- 产品功能（70/100）：核心功能满足需求，但数据导出格式有限，不支持自定义报表\n- 用户体验（60/100）：界面现代但操作路径较长，批量操作不够便捷\n- 安全合规（85/100）：满足等保要求\n- 价格（75/100）：中等价位，但高级功能需额外付费不透明",
                user_segment="enterprise",
                sentiment_score=-1,
                themes=["数据导出", "操作效率", "价格透明", "报表"],
                impact_level="high",
                status="analyzed",
                recommendations=["支持自定义报表导出", "添加批量操作功能", "重新设计定价页"],
                author="Alice",
            ),
            FeedbackItem(
                title="App Store用户评价 — 加载速度慢",
                source_type="review",
                content="用户A(⭐2): 每次打开都要等很久，特别是数据图表页面。\n用户B(⭐3): 功能挺好的但是太卡了，希望优化速度。\n用户C(⭐1): 打开就卡死，根本用不了。已卸载。",
                user_segment="core",
                sentiment_score=-2,
                themes=["加载速度", "性能优化", "图表渲染"],
                impact_level="critical",
                status="new",
                recommendations=[],
                author="Bob",
            ),
            FeedbackItem(
                title="用户访谈 — 新手引导缺少视频教程",
                source_type="interview",
                content="访谈对象：3位新注册用户\n共同反馈：\n1. 注册后不知道从哪里开始\n2. 希望有30秒的快速上手视频\n3. 文字帮助太长了不想看\n4. 竞品XX有很好的视频引导",
                user_segment="new",
                sentiment_score=0,
                themes=["新手引导", "视频教程", "上手体验", "竞品对比"],
                impact_level="medium",
                status="analyzing",
                recommendations=["制作30秒快速上手视频", "简化文字帮助为卡片式引导"],
                author="Charlie",
            ),
        ]

        for item in demo_feedback:
            db.add(item)

        db.commit()
        print("📦 Demo data seeded successfully")
    except Exception as e:
        print(f"⚠️  Demo seed error (non-fatal): {e}")
        db.rollback()
    finally:
        db.close()


# ─────────────────────────── Run ───────────────────────────

if __name__ == "__main__":
    import uvicorn

    # Seed demo data for development
    os.makedirs("data", exist_ok=True)
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    init_db()
    seed_demo_data()

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
