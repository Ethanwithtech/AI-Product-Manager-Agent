---
name: feedback-insight-engine
description: Collect and analyze user feedback, bids, or research data to generate actionable product iteration insights through guided discussion.
intent: >-
  Guide PMs through an intelligent, conversational workflow that collects multi-source
  user feedback (bids, support tickets, reviews, interviews, surveys), performs structured
  analysis (sentiment, theme clustering, impact scoring), facilitates product discussion
  with the PM, and outputs prioritized iteration recommendations — all while teaching
  the PM how to think about feedback systematically.
type: interactive
theme: pm-collaboration
best_for:
  - "Collecting and structuring feedback from bids, RFPs, or customer responses"
  - "Analyzing user support tickets, app reviews, or survey results"
  - "Facilitating product iteration discussions with data-backed insights"
  - "Generating prioritized feature requests from raw qualitative feedback"
  - "Identifying churn risks and satisfaction patterns across user segments"
scenarios:
  - "A PM receives 50+ user survey responses and needs to extract actionable patterns"
  - "The team lost a bid and wants to analyze the feedback to improve the product"
  - "Customer support tickets reveal recurring pain points that need prioritization"
  - "A PM wants to discuss product direction with AI based on real user data"
estimated_time: "20-45 min"
---

# Feedback Insight Engine

## Purpose

Product decisions without user feedback are opinions. Product decisions with unstructured feedback are noise. This skill transforms raw, messy user input — bids, reviews, support tickets, interview notes, survey data — into **structured, prioritized, actionable insights** through guided conversation.

Unlike a one-shot analysis tool, this skill **discusses findings with you** like a sharp product analyst would: challenging assumptions, surfacing hidden patterns, and helping you decide what to build next.

**When to use this skill:**
- You have user feedback data (any format) and need to extract what matters
- You lost a bid/deal and want to learn from the feedback
- You want to validate a product direction against real user signals
- You need a structured feedback report to share with stakeholders
- You want an AI thought partner to challenge your interpretation of user data

**What this skill produces:**
1. Structured feedback taxonomy (themes, sentiment, impact)
2. Interactive discussion of findings (AI asks questions, challenges assumptions)
3. Prioritized iteration recommendations with supporting evidence
4. Feedback summary report stored via MCP for team access

## Key Concepts

| Concept | Definition | Why It Matters |
|---------|-----------|---------------|
| **Feedback Triangulation** | Cross-referencing signals from 3+ sources to validate a finding | Single-source feedback is biased; triangulation reveals truth |
| **Theme Clustering** | Grouping related feedback into named categories | Converts 200 scattered comments into 5-8 actionable themes |
| **Sentiment Scoring** | Rating feedback emotion on a -2 to +2 scale (very negative → very positive) | Quantifies qualitative data for prioritization |
| **Impact Matrix** | Plotting themes by frequency × severity × strategic alignment | Prevents "squeaky wheel" bias — loud ≠ important |
| **Silent Signal** | What users did NOT say, or data from users who left without feedback | The most dangerous feedback pattern is the invisible one |
| **Bid Loss Analysis** | Structured post-mortem on competitive losses using evaluator comments | Turns rejection into a product improvement roadmap |
| **Iteration Velocity** | How quickly feedback loops back into product changes | Fast loops = compounding improvement; slow loops = stale product |

_The gap between what users **say** and what they **do** is where the real insights live. Always triangulate behavioral data (actions) against stated feedback (words)._

## Application

This skill operates as a **5-phase intelligent conversation**. Each phase adapts based on your input.

### Question 1: What Feedback Are We Working With?

_Understanding the source and format of your data determines the entire analysis approach._

**Ask the PM:**
> What type of feedback do you want me to analyze? You can paste raw data, describe what you have, or point me to stored documents.

**Options:**
1. **标书/投标反馈 (Bid & RFP Feedback)** — Lost/won bid evaluator comments, scoring breakdowns, competitive comparisons
2. **用户评价与工单 (Reviews & Support Tickets)** — App store reviews, support conversations, bug reports
3. **调研与访谈 (Research & Interviews)** — User interview transcripts, survey responses, usability test results
4. **产品内行为数据 (In-Product Behavioral Signals)** — Feature usage data, funnel drop-offs, session recordings summary
5. **混合来源 (Mixed Sources)** — I have feedback from multiple channels

**Adaptive behavior:**
- If the PM pastes raw text → automatically detect format and classify
- If the PM says "bid feedback" → switch to **Bid Loss Analysis** mode with competitive lens
- If the PM says "mixed" → ask for each source type and weigh reliability accordingly
- **MCP action**: Call `search_knowledge` to check for existing related feedback or product context

### Question 2: Who Are These Users?

_User segmentation changes everything. A complaint from your top-spending enterprise client has different weight than a free-tier user reviewing on the app store._

**Ask the PM:**
> Who is this feedback from? Help me understand the user segment so I can weight the analysis correctly.

**Options:**
1. **高价值企业客户 (Enterprise / High-Value)** — Large accounts, high ARR, strategic relationships
2. **核心活跃用户 (Core Active Users)** — Regular users who represent your primary use case
3. **新用户/试用期 (New Users / Trial)** — First-time or onboarding users
4. **流失/沉默用户 (Churned / Silent Users)** — Users who left or stopped engaging
5. **不确定/混合 (Unsure / Mixed)** — Multiple segments or unidentified

**Adaptive behavior:**
- Enterprise + Bid feedback → emphasize competitive positioning and feature gaps
- Churned users → focus on "what drove them away" root cause analysis
- New users → focus on onboarding friction and first-value-time
- If PM selects "unsure" → suggest segmentation criteria before analysis

### Question 3: Deep Analysis — Let Me Show You What I See

_This is where the AI does heavy lifting: clustering, scoring, pattern detection. But critically, it also **discusses** findings with the PM rather than just dumping a report._

**After processing the feedback, the AI should:**

1. **Present Theme Clusters** (3-8 themes, each with):
   ```
   🏷️ Theme: [Name]
   📊 Mentions: [N] ([%] of total)
   😊 Sentiment: [score -2 to +2] [emoji indicator]
   📈 Trend: [↑ 增长 / → 稳定 / ↓ 减少]
   💬 Representative Quote: "[verbatim]"
   ```

2. **Ask the PM's reaction:**
   > Here's what I found. Let me know:
   > 1. **哪个主题让你意外？** (Which theme surprises you?) — Surprise = gap in your mental model
   > 2. **哪个你已经知道？** (Which did you already know?) — If you knew but didn't act, why?
   > 3. **哪个你不同意？** (Which do you disagree with?) — Let's debate it with data
   > 4. **还有什么我漏掉的？** (What am I missing?) — Your context + my analysis = better insight
   > 5. **继续深入某个主题** (Go deeper on a specific theme) — I'll pull more detail

**Adaptive behavior:**
- If PM says "I disagree with theme X" → present supporting evidence, ask what their data shows, facilitate a structured debate
- If PM says "theme Y surprises me" → explore root causes, check if knowledge base has related context
- If PM wants to "go deeper" → drill into sub-themes, individual quotes, user journey mapping for that theme
- **MCP action**: Call `search_knowledge` to enrich themes with existing product context

### Question 4: So What Do We Build? — Prioritization Discussion

_The hardest part of feedback isn't analysis — it's deciding what to do about it. This phase helps the PM make that call._

**Ask the PM:**
> Based on our analysis, here are my prioritized recommendations. Let's discuss which ones make sense for your next sprint.

**Present an Impact × Effort matrix:**

```
               High Impact
                   │
     ┌─────────────┼─────────────┐
     │  💎 Quick    │  🚀 Strategic│
     │  Wins        │  Projects   │
     │  (DO FIRST)  │  (PLAN)     │
Low ─┼─────────────┼─────────────┼─ High
Effort│  🗑️ Skip    │  ⚠️ Question│
     │  These       │  Worth      │
     │              │             │
     └─────────────┼─────────────┘
                   │
              Low Impact
```

**For each recommendation:**
```
📌 Recommendation: [specific action]
🎯 Expected Impact: [metric improvement]
👥 Affected Segment: [user group]
📊 Evidence Strength: [strong/medium/weak]
💬 Key Quote: "[supporting user quote]"
⏱️ Effort: [T-shirt size: S/M/L/XL]
🔗 Related Theme: [theme name]
```

**Discussion prompts:**
1. **同意这个优先级吗？** — Do you agree with this prioritization? What would you change?
2. **有什么约束我不知道的？** — Any constraints I'm not aware of? (tech debt, team capacity, dependencies)
3. **这和当前规划冲突吗？** — Does this conflict with your current roadmap? Let me check the progress board.
4. **要我把某个建议转成需求单吗？** — Should I convert any recommendation into a formal requirement?

**Adaptive behavior:**
- If PM agrees → proceed to generate requirements via MCP
- If PM disagrees → ask why, adjust weights, re-prioritize
- If PM says "conflicts with roadmap" → **MCP action**: call `get_progress_board` and `check_conflicts` to show real overlaps
- **MCP action**: Call `get_templates` to get requirement template for conversion

### Question 5: Output & Next Steps

_Ship the analysis where the team can see it._

**Ask the PM:**
> How should I package this analysis? And what should happen next?

**Options:**
1. **保存反馈分析报告** — Store the full analysis to MCP knowledge base so team has access
2. **转化为需求单** — Convert top recommendations into formal PRD requirement docs
3. **更新产品进度** — Add iteration items to the progress board
4. **生成利益相关者汇报** — Create an executive summary for stakeholder presentation
5. **设置反馈追踪** — Note which themes to monitor in the next feedback cycle
6. **以上全部** — All of the above (recommended for thorough follow-through)

**MCP Actions by choice:**

| Choice | MCP Tools Used |
|--------|---------------|
| 保存报告 | `add_knowledge_document` — store analysis as searchable document |
| 转化需求 | `create_requirement` for each top-priority item |
| 更新进度 | `update_progress` for each iteration work item |
| 汇报摘要 | `get_templates` for executive summary format |
| 反馈追踪 | `add_knowledge_document` — store monitoring checklist |

## Examples

### Example: Bid Loss Analysis

**Scenario**: Your team lost a B2B SaaS bid to a competitor. The evaluator returned a scoring sheet with comments.

**PM pastes:**
```
评审反馈：
- 产品功能（70/100）：核心功能满足需求，但数据导出格式有限，不支持自定义报表
- 用户体验（60/100）：界面现代但操作路径较长，批量操作不够便捷
- 安全合规（85/100）：满足等保要求，加密方案完善
- 价格（75/100）：中等价位，但高级功能需要额外付费不透明
- 服务支持（80/100）：响应及时，但缺乏专属客户成功经理
```

**AI Analysis Output:**
```
🏷️ Theme 1: 数据导出 & 报表能力不足
📊 Impact: HIGH — directly scored; competitive gap
😊 Sentiment: -1 (明确不满)
📌 Recommendation: 支持自定义报表导出(CSV/Excel/PDF)
⏱️ Effort: M
🔗 This is a common B2B blocker — 3 of last 5 enterprise deals mentioned this

🏷️ Theme 2: 操作效率 — 批量操作缺失
📊 Impact: HIGH — UX score was lowest
😊 Sentiment: -1
📌 Recommendation: 添加批量选择/操作功能，减少重复点击
⏱️ Effort: M

🏷️ Theme 3: 价格透明度
📊 Impact: MEDIUM — not a deal-breaker but erodes trust
😊 Sentiment: -0.5
📌 Recommendation: 重新设计定价页，所有功能价格一目了然
⏱️ Effort: S (Quick Win!)
```

**AI then asks:**
> 这个丢单模式你之前见过吗？"数据导出"在其他客户反馈里也出现过吗？让我搜一下知识库看看…
>
> *[calls search_knowledge("数据导出 报表 enterprise")]*
>
> 找到了！上个月的用户调研报告也提到了类似问题。这说明这不是个案——是一个系统性的产品缺陷。建议优先级提到P0。你同意吗？

_This example shows the key difference: the AI doesn't just analyze — it **connects dots across time**, challenges the PM's awareness, and drives toward a decision._

### Anti-Pattern in This Example

❌ **Bad**: AI dumps a table and says "here are 5 themes, pick what matters."
✅ **Good**: AI presents themes, then asks "which one surprises you?" and "does this match what you already knew?" — because the gap between expectation and reality is where learning happens.

## Common Pitfalls

| # | Symptom | Consequence | Fix |
|---|---------|-------------|-----|
| 1 | **Treating all feedback equally** | Free-tier complaints drown out enterprise deal-breaker signals | Always segment first (Question 2). Weight by business impact, not volume |
| 2 | **Only analyzing what users say** | Miss behavioral signals — what users _do_ often contradicts what they _say_ | Triangulate: stated feedback + behavioral data + competitive intel |
| 3 | **Analysis paralysis** | PM spends 2 weeks analyzing instead of acting | Use the Impact × Effort matrix to force a decision within the conversation |
| 4 | **Confirmation bias** | PM only accepts themes that match their existing plan | Question 3 deliberately asks "what surprises you?" and "what do you disagree with?" to surface blind spots |
| 5 | **One-and-done analysis** | Feedback analyzed once, never revisited | Question 5 includes "set up feedback tracking" to create a monitoring loop |
| 6 | **Ignoring silent signals** | Focus on loud complainers, miss the quiet churners | Always ask: "Who is NOT giving feedback? Why?" |

_Anti-pattern spotlight:_ **The "Everything is P0" Trap.** When a PM marks every feedback theme as highest priority, nothing is actually prioritized. The Impact × Effort matrix in Question 4 forces honest ranking. If the PM pushes back ("they're ALL important"), ask: "If you could only fix ONE this sprint, which would it be?" That's your real P0.

## References

### Related Skills
- [`product-knowledge-base`](../product-knowledge-base/SKILL.md) — Store feedback analysis results for future AI context
- [`requirement-generator`](../requirement-generator/SKILL.md) — Convert top recommendations into formal PRDs
- [`product-sync-agent`](../product-sync-agent/SKILL.md) — Sync iteration items to the team progress board

### MCP Tools Used

| Tool | When |
|------|------|
| `search_knowledge` | Before analysis — find previous feedback reports and product context |
| `add_knowledge_document` | After analysis — store the feedback report for team access |
| `create_requirement` | When converting recommendations to formal PRDs |
| `update_progress` | When adding iteration work items to the board |
| `get_progress_board` | When checking if recommendations conflict with current work |
| `check_conflicts` | When validating recommendations against team's active items |
| `get_templates` | When retrieving report templates or requirement templates |
| `list_requirements` | When checking if similar requirements already exist |

### Frameworks Referenced
- **Kano Model** — Categorizing features as Must-have / Performance / Delighter
- **RICE Scoring** — Reach × Impact × Confidence / Effort
- **Jobs-to-be-Done** — Understanding the "job" users hire your product for
- **Voice of Customer (VoC)** — Systematic feedback collection and analysis methodology
