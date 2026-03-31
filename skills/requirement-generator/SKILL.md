---
name: requirement-generator
description: Generate structured requirement documents from natural language using AI and product knowledge context. Use when turning a feature idea into a team-ready PRD with MCP-powered knowledge retrieval.
intent: >-
  Guide product managers through AI-assisted generation of structured requirement documents (PRDs). The workflow retrieves relevant product context from the shared knowledge base via MCP tools, generates a comprehensive requirement document using a standard template, and stores the result in the shared repository for team visibility. Combines the rigor of traditional PRD writing with the speed of AI generation.
type: workflow
theme: pm-artifacts
best_for:
  - "Turning a rough feature idea into a structured PRD in minutes instead of hours"
  - "Ensuring every requirement document includes product context from the knowledge base"
  - "Maintaining consistent PRD format across the PM team"
scenarios:
  - "I have a feature idea for AI-powered search and need to write a PRD before tomorrow's planning session"
  - "I want to generate a requirement document that automatically references our existing product specs and design guidelines"
  - "Our team needs a consistent requirement format that every PM follows"
estimated_time: "15-30 min"
---

## Purpose

Writing a good PRD takes time — not because the format is hard, but because gathering context is slow. You need to check existing features, reference design specs, understand technical constraints, and ensure you're not duplicating someone else's work. This skill automates the context-gathering step using MCP-powered knowledge retrieval, then generates a structured requirement document that your AI assistant fills in based on your natural language description and the retrieved context.

The result: a PRD that would take 2-4 hours to write manually, produced in 15-30 minutes, with better product context consistency because the AI actually checks the knowledge base instead of relying on your memory.

## Key Concepts

### The Context-First Principle

The quality of an AI-generated PRD is directly proportional to the quality of context it receives. The workflow always starts with knowledge retrieval — never with generation. This is the single most important principle.

_Why: An AI generating a PRD without product context will produce a generic, plausible-sounding document that misses your product's specific constraints, existing features, and design patterns. It looks professional but is functionally useless._

### Template-Driven Generation

Every PRD follows the same template (see Application section). This ensures:
- **Consistency**: Any PM on the team can read any PRD and find information in the expected place.
- **Completeness**: The template's sections act as a checklist — missing a section means missing a dimension.
- **Reviewability**: Stakeholders learn to scan for the sections they care about (engineers → Technical Considerations, execs → Success Metrics).

### MCP Integration Points

This workflow calls MCP tools at three critical moments:

1. **Before generation**: `search_knowledge` to retrieve product context
2. **Before generation**: `get_templates` to load the team's PRD template
3. **After generation**: `create_requirement` to store the result in the shared repository
4. **After storage**: `check_conflicts` to detect overlaps with other PMs' work

## Application

### Phase 1: Context Assembly

**Goal**: Gather all relevant product information before asking the AI to generate anything.

**Activities**:

1. **Retrieve product context** from the shared knowledge base:
   ```
   Call: search_knowledge(query="[your feature topic]", top_k=5)
   ```
   This returns the most relevant product documents — feature specs, design guidelines, technical constraints, user research — that relate to your feature area.

2. **Load the team's PRD template**:
   ```
   Call: get_templates(category="requirement")
   ```
   This returns the team's agreed-upon PRD format. If no custom template exists, use the default template below.

3. **Check the progress board** for related work:
   ```
   Call: get_progress_board()
   ```
   Scan for items in "Planning" or "In Progress" that might overlap with your feature.

**Output**: A context package containing retrieved documents, the PRD template, and awareness of related team work.

### Phase 2: Requirement Generation

**Goal**: Generate the structured PRD using AI with full product context.

**Activities**:

1. Provide your feature description in natural language. Be specific about:
   - What problem you're solving (and for whom)
   - What success looks like (measurable outcomes)
   - What you're NOT building (scope boundaries)

2. The AI generates the PRD using this **default template**:

```markdown
# Requirement: [Feature Name]

## 1. Problem Statement
### Problem Description
[What user pain or business gap are we solving?]

### Evidence
[Data, interviews, support tickets, or observations that validate this problem]

### Impact of Not Solving
[What happens if we do nothing?]

## 2. User Stories
[As a [persona], I want to [action] so that [outcome]]

### Acceptance Criteria
[Given/When/Then format for each story]

## 3. Success Metrics
| Metric | Current Baseline | Target | Measurement Method | Timeframe |
|--------|-----------------|--------|-------------------|-----------|
|        |                 |        |                   |           |

## 4. Solution Overview
### Approach
[High-level solution description]

### Key Design Decisions
[Decisions made and their rationale]

### Out of Scope
[What we are explicitly NOT building]

## 5. Technical Considerations
### Dependencies
[Systems, APIs, teams this feature depends on]

### Constraints
[Technical limitations, performance requirements, compatibility needs]

### Risks
[Known risks with mitigation strategies]

## 6. Release Plan
### Rollout Strategy
[Big bang / phased / feature flag / A-B test]

### Rollback Plan
[How to revert if things go wrong]

### Support Readiness
[Documentation, training, support team preparation]

## 7. Appendix
### Related Documents
[Links to research, designs, competitive analysis]

### Changelog
| Date | Author | Change |
|------|--------|--------|
|      |        |        |
```

3. Review the generated PRD. Check that:
   - [ ] Problem statement references real evidence, not assumptions
   - [ ] User stories have acceptance criteria
   - [ ] Success metrics have baselines and targets
   - [ ] Out of Scope is explicitly defined
   - [ ] Technical risks have mitigation strategies

### Phase 3: Storage & Team Sync

**Goal**: Store the requirement and alert the team.

**Activities**:

1. **Store the requirement**:
   ```
   Call: create_requirement(
     title="[Feature Name]",
     content="[full PRD markdown]",
     modules=["module1", "module2"],
     author="[your name]"
   )
   ```

2. **Check for conflicts**:
   ```
   Call: check_conflicts(
     title="[Feature Name]",
     modules=["module1", "module2"],
     keywords=["keyword1", "keyword2", ...]
   )
   ```

3. If conflicts are detected, review them and reach out to the affected PM before proceeding.

**Output**: Stored requirement document, conflict report (if any).

### Phase 4: TAPD Sync (Optional — requires TAPD credentials)

**Goal**: Synchronize the generated PRD to TAPD for engineering handoff and project tracking.

**Prerequisites**:
- TAPD credentials configured at `~/.tapd/credentials` with format:
  ```
  access_token=<your-tapd-access-token>
  env=OA
  ```
- TAPD MCP tools available (stories_create, stories_update, etc.)
- TAPD Toolkit scripts available at `skills/tapd-toolkit/scripts/`

**Activities**:

1. **Create the requirement in TAPD**:
   ```
   Call: stories_create(
     workspace_id="<your-workspace-id>",
     name="[Feature Name]",
     description="[PRD summary — first 2000 chars or executive summary section]",
     priority="high",
     owner="[author name]"
   )
   → Returns: story_id (e.g., "1112345678001234567")
   ```

2. **Upload the full PRD as an attachment** (for the complete document):
   ```
   Run: python skills/tapd-toolkit/scripts/upload-attachment.py \
     --workspace_id <workspace-id> \
     --file <path-to-prd-file> \
     --type story \
     --entry_id <story_id-from-step-1>
   ```
   _Note: First save the PRD markdown to a temporary file, then upload. Max file size: 250MB._

3. **Upload images and embed in description** (if the PRD contains diagrams/screenshots):
   ```
   Run: python skills/tapd-toolkit/scripts/upload-image.py \
     --workspace_id <workspace-id> \
     --file <path-to-image>
   → Returns: html_code (e.g., '<img src="..." />')
   
   Call: stories_update(
     workspace_id="<workspace-id>",
     id="<story_id>",
     description="[updated description with embedded html_code]"
   )
   ```

4. **Confirm sync status** to the PM:
   - Report the TAPD story URL: `https://www.tapd.cn/<workspace_id>/prong/stories/view/<story_id>`
   - Mention any images or attachments uploaded
   - Note if any step failed (partial sync is acceptable)

**Output**: TAPD story created with PRD content, attachments, and embedded images.

**Anti-pattern: Blind Sync Without Review**

_Don't automatically sync every generated PRD to TAPD._ The PM should review and approve the PRD in Phase 3 before Phase 4 executes. A half-baked PRD pushed to TAPD creates noise for the engineering team.

**Recommendation Flow**:
After Phase 3 completes, ask the PM:
> "PRD 已生成并存入本地。是否要同步到 TAPD？请提供 workspace_id。"

Only proceed to Phase 4 upon explicit confirmation.

## Examples

### Example: AI-Powered Search Feature

**PM's input**: "I want to add AI-powered search to our e-commerce platform. Users currently struggle to find products when they don't know the exact name — they use vague descriptions like 'that blue thing for the kitchen' and get zero results."

**Step 1 — Knowledge retrieval**:
```
search_knowledge(query="search functionality product catalog user experience")
→ Returns: existing search architecture doc, product catalog schema, previous user research on search frustration
```

**Step 2 — AI generates PRD** (excerpt):
```markdown
# Requirement: AI-Powered Semantic Search

## 1. Problem Statement
### Problem Description
Users cannot find products when using natural language descriptions. Current keyword search requires exact product name matches, creating a discovery gap for users who know what they want but not what it's called.

### Evidence
- Knowledge base: User research doc (2024-Q3) shows 34% of search queries return zero results
- Knowledge base: Support ticket analysis reveals "can't find product" is the #2 complaint category
- Product catalog contains 12,000+ SKUs but search only indexes product titles

### Impact of Not Solving
Estimated 15-20% of potential purchases are abandoned due to search frustration (based on zero-result-rate × average conversion rate).
```

_Notice how the AI referenced specific data from the knowledge base — "34% zero results," "support ticket #2 category." This is what context-first generation produces._

## Common Pitfalls

### Pitfall 1: Skipping Knowledge Retrieval

**Symptom**: PM goes straight to "generate a PRD for X" without calling `search_knowledge` first.

**Consequence**: The AI produces a generic PRD with no product-specific context. It sounds professional but contains no real evidence, no awareness of existing features, and no reference to actual user data.

**Fix**: Always call `search_knowledge` before generation. Even if the results seem tangential, they give the AI grounding in your product's reality. A PRD with "User research from Q3 shows 34% zero-result rate" is infinitely more credible than "Users may struggle with search."

### Pitfall 2: Accepting the First Draft

**Symptom**: PM takes the AI-generated PRD as final without review or editing.

**Consequence**: AI-generated PRDs are good starting points but often miss nuance — organizational politics, unwritten technical constraints, recent decisions not yet in the knowledge base.

**Fix**: Treat the AI output as a first draft that's 70-80% complete. Your job is to add the 20-30% that requires human judgment: political context, prioritization rationale, stakeholder-specific concerns.

### Pitfall 3: Vague Success Metrics

**Symptom**: The generated PRD has success metrics like "improve user satisfaction" or "increase engagement."

**Consequence**: You can't measure what you can't define. Vague metrics make it impossible to evaluate whether the feature succeeded.

**Fix**: Every metric needs four elements: what you're measuring, the current baseline, the target number, and the measurement method. "Improve search conversion from 2.1% to 3.5% measured by GA events within 90 days of launch."

### Pitfall 4: Empty Out of Scope

**Symptom**: The "Out of Scope" section is blank or says "N/A."

**Consequence**: Without explicit scope boundaries, every stakeholder assumes their pet feature is included. Scope creep is guaranteed.

**Fix**: Out of Scope should list at least 3 things that someone might reasonably expect to be included but aren't. If you can't think of any, you haven't talked to enough stakeholders.

## References

### Related Skills
- `skills/prd-development/SKILL.md` — comprehensive PRD development workflow (manual, non-AI-assisted)
- `skills/user-story/SKILL.md` — detailed user story writing with Gherkin acceptance criteria
- `skills/problem-statement/SKILL.md` — problem framing before solution design
- `skills/product-knowledge-base/SKILL.md` — managing the knowledge base that powers context retrieval
- `skills/tapd-toolkit/SKILL.md` — TAPD file upload tools for Phase 4 sync (image upload, attachment upload)

### Related Commands
- `commands/generate-requirement.md` — one-command shortcut for this workflow
- `commands/fullchain.md` — extends this workflow through UI draft generation

### MCP Tools Used
- `search_knowledge` — retrieve relevant product context before generation
- `get_templates` — load the team's PRD template
- `create_requirement` — store the generated requirement in the shared repository
- `check_conflicts` — detect overlaps with other PMs' work
- `stories_create` — (Phase 4) create a TAPD story from the generated PRD
- `stories_update` — (Phase 4) update TAPD story description with embedded images

### TAPD Toolkit Scripts Used (Phase 4)
- `skills/tapd-toolkit/scripts/upload-attachment.py` — upload full PRD document as TAPD attachment
- `skills/tapd-toolkit/scripts/upload-image.py` — upload images and get embeddable HTML code

### Related Agents
- `agents/product-manager.md` — PM agent role with PRD templates and quality standards

---

_Skill type: workflow_
_Suggested filename: SKILL.md_
_Suggested placement: skills/requirement-generator/_
_Dependencies: MCP Server (pm-team-hub) configured; product knowledge base populated; TAPD credentials at ~/.tapd/credentials (optional, for Phase 4)_
