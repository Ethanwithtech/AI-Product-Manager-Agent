---
name: fullchain-efficiency
description: Run the full requirement-to-UI pipeline in one workflow. Use when you want to go from a feature idea to front-end-ready React code in a single session, with knowledge base context and team sync built in.
intent: >-
  Orchestrate the complete product manager workflow from natural language feature description to front-end-ready React + Arco Design code in a single end-to-end session. Chains knowledge retrieval, requirement generation, conflict detection, UI code generation, and team progress updates into one cohesive pipeline. This is the "press one button, get everything" workflow for standard business features.
type: workflow
theme: pm-workflow
best_for:
  - "Going from feature idea to front-end code in one session"
  - "Running the complete PM pipeline without manually chaining skills"
  - "Demonstrating the full value of the Skills + MCP toolkit to your team"
scenarios:
  - "I have a feature idea and want to produce both a PRD and initial UI code before end of day"
  - "I need to show the team how the full PM pipeline works from idea to code"
  - "I want to scope a feature, check for team conflicts, and produce a UI starting point in one go"
estimated_time: "30-60 min"
---

## Purpose

Individual PM skills are powerful, but their real value emerges when they're chained together. This skill orchestrates the complete pipeline:

```
Feature Idea → Knowledge Retrieval → Requirement Document → Team Sync → UI Code → Handoff
```

Running this pipeline manually means: calling `search_knowledge`, then switching to the requirement-generator skill, then storing the result, then checking conflicts, then switching to the ui-draft-generator skill, then packaging the output. That's 6+ context switches.

This skill reduces it to one continuous flow. The AI maintains context across all stages, so the UI code references the exact requirement it was generated from, which references the exact product knowledge that informed it.

_When NOT to use this: When you only need a PRD (use `requirement-generator`), only need UI code (use `ui-draft-generator`), or when the feature is too novel/complex for a single-session treatment._

## Key Concepts

### Pipeline Stages

| Stage | Skill Used | MCP Tools Called | Output |
|-------|-----------|-----------------|--------|
| 1. Context Assembly | `product-knowledge-base` | `search_knowledge`, `get_templates`, `get_progress_board` | Product context package |
| 2. Requirement Generation | `requirement-generator` | `create_requirement`, `check_conflicts` | Stored PRD + conflict report |
| 3. UI Code Generation | `ui-draft-generator` | `search_knowledge` (design docs) | React + Arco Design TSX files |
| 4. Team Sync | `product-sync-agent` | `update_progress` | Progress board updated |

### Context Continuity

The key advantage of running the full chain vs. individual skills: **context carries forward**. The requirement generation stage has the knowledge base results. The UI generation stage has both the knowledge base results AND the requirement document. The team sync stage has the complete picture.

This means:
- The PRD references specific product constraints from the knowledge base
- The UI code implements the exact user stories from the PRD
- The progress update includes accurate module tags and keywords from the PRD

### Quality Gates

Each stage has a checkpoint before advancing:

1. **After Context Assembly**: "Are the retrieved documents relevant? Is there enough context to proceed?"
2. **After Requirement Generation**: "Does the PRD have all required sections? Are success metrics specific? Is scope defined?"
3. **After UI Code Generation**: "Do the components map to user stories? Are all states handled? Are imports correct?"
4. **After Team Sync**: "Were conflicts detected? Do they need resolution before proceeding?"

If any gate fails, the pipeline pauses for human input rather than producing lower-quality downstream output.

## Application

### Phase 1: Input & Context Assembly (5-10 min)

**Goal**: Gather everything the AI needs to produce a high-quality requirement and UI.

**Step 1**: Describe your feature in natural language. Include:
- The problem you're solving
- Who experiences the problem
- What success looks like
- Any known constraints

**Step 2**: The AI retrieves context:
```
search_knowledge(query="[feature topic]", top_k=5)
→ Product specs, design docs, user research

get_templates(category="requirement")
→ Team's PRD template

get_progress_board()
→ What other PMs are working on
```

**Step 3**: Review the retrieved context. If critical documents are missing, upload them now via `add_knowledge_document` or tell the AI what additional context to consider.

**Quality Gate**: Confirm the context is sufficient. If not, add more context before proceeding.

### Phase 2: Requirement Generation (10-15 min)

**Goal**: Produce a structured requirement document.

**Step 1**: The AI generates a PRD using the retrieved context and your feature description, following the team template.

**Step 2**: Review the generated PRD:
- [ ] Problem statement cites real evidence from knowledge base
- [ ] User stories have acceptance criteria
- [ ] Success metrics have baselines and targets
- [ ] Out of scope is explicit
- [ ] Technical risks are identified

**Step 3**: Store and check:
```
create_requirement(title, content, modules, author)
→ Stored in shared repository

check_conflicts(title, modules, keywords)
→ Returns any overlaps with other PMs' work
```

**Quality Gate**: If conflicts are found, decide whether to proceed (notify affected PM later) or pause (resolve conflict first).

### Phase 3: UI Code Generation (10-20 min)

**Goal**: Transform the requirement into React + Arco Design code.

**Step 1**: The AI analyzes the requirement document and identifies:
- Pages/views needed
- Components per page
- Data entities and their display format
- User actions and interaction patterns

**Step 2**: For each identified page, the AI generates:
- TypeScript component file (`.tsx`)
- Arco Design imports and configuration
- Tailwind CSS layout classes
- All interaction states (loading, empty, error, success)

**Step 3**: Review the generated code:
- [ ] Every user story has a corresponding UI element
- [ ] Component selection matches data patterns (Table for lists, Card for items, Form for input)
- [ ] Responsive design is present
- [ ] Empty and loading states are handled

**Quality Gate**: Code must have correct imports, valid TSX, and responsive layout. Add TODO comments for areas needing front-end refinement.

### Phase 4: Team Sync & Handoff (5 min)

**Goal**: Update the team and package the delivery.

**Step 1**: Update the progress board:
```
update_progress(
  title="[Feature Name]",
  description="[one-sentence summary]",
  status="planning",
  modules=["module1", "module2"],
  keywords=["keyword1", "keyword2"]
)
```

**Step 2**: Compile the delivery package:
```
Delivery Package:
├── requirement.md          — Full PRD document
├── conflict-report.md      — Any detected conflicts
├── components/
│   ├── PageOne.tsx         — React component for page 1
│   ├── PageTwo.tsx         — React component for page 2
│   └── ...
└── handoff-notes.md        — Dependencies, TODO items, refinement areas
```

**Step 3**: Share with the front-end team with framing: "Here's a PRD and initial UI code. The PRD is the source of truth; the code is a high-fidelity starting point that implements the user stories."

## Examples

### Example: Full Pipeline for "Team Activity Feed"

**PM Input**: "I want to add a team activity feed to our internal tool. When a PM creates a requirement, updates progress, or uploads a knowledge doc, it should appear in a shared feed so the team stays aware of activity without needing to check each section separately."

**Phase 1 output**: Retrieved 3 relevant docs (existing notification system spec, current dashboard layout, team preferences research).

**Phase 2 output** (excerpt):
```markdown
# Requirement: Team Activity Feed

## Problem Statement
PMs must check 3 separate sections (requirements, progress board, knowledge base) 
to stay informed about team activity. This creates information fragmentation...

## User Stories
- As a PM, I want to see a chronological feed of team actions so I can 
  stay informed without checking each section
- As a PM, I want to filter the feed by activity type so I can focus on 
  what's relevant to my work
```

**Phase 3 output** (excerpt):
```tsx
// ActivityFeed.tsx — Implements "Team Activity Feed" requirement
import React, { useState, useEffect } from 'react';
import { Card, List, Tag, Avatar, Select, Typography, Space, Empty } from '@arco-design/web-react';

interface ActivityItem {
  id: string;
  type: 'requirement' | 'progress' | 'knowledge';
  author: string;
  action: string;
  title: string;
  timestamp: string;
}

const ActivityFeed: React.FC = () => {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [filter, setFilter] = useState<string>('all');
  // ... full component implementation
};
```

**Phase 4 output**: Progress board updated, no conflicts detected, delivery package assembled.

**Total time**: ~35 minutes from idea to full delivery package.

## Common Pitfalls

### Pitfall 1: Running the Full Chain for Everything

**Symptom**: PM runs the fullchain workflow for a minor bug fix or a copy change.

**Consequence**: Overkill. A 30-minute pipeline for a task that needs a 2-line code change. The team learns to associate the workflow with unnecessary overhead.

**Fix**: Use the full chain for **new features and significant enhancements** only. For bug fixes, use `requirement-generator` alone (or just write the ticket). For UI tweaks, use `ui-draft-generator` alone.

### Pitfall 2: Skipping Quality Gates

**Symptom**: PM rushes through all four phases without reviewing intermediate output.

**Consequence**: A bad requirement produces a bad UI. The UI looks complete but implements the wrong user stories, cites incorrect product data, or targets the wrong user persona.

**Fix**: Each quality gate is a "stop and think" moment. The 2 minutes you spend reviewing the PRD before generating UI saves 2 hours of front-end rework.

### Pitfall 3: Not Resolving Conflicts Before Proceeding

**Symptom**: `check_conflicts` returns a module overlap, PM ignores it and generates UI anyway.

**Consequence**: Two PMs produce requirements and UI code for overlapping features. Engineering discovers the conflict during implementation, requiring one feature to be redesigned.

**Fix**: When conflicts are detected, pause the pipeline. Send a message to the other PM: "I see we're both touching [module]. Can we align in 5 minutes before I proceed?" Resolution takes 5 minutes now; unresolved conflicts take weeks later.

### Pitfall 4: Over-Relying on the Pipeline

**Symptom**: PM treats the pipeline output as final product, never adding human judgment.

**Consequence**: The requirement lacks organizational context, political awareness, and nuanced tradeoffs. The UI misses brand-specific details and edge cases only a human would catch.

**Fix**: The pipeline produces an excellent first draft. Your job is to add the 20% that requires product judgment: "This feature interacts with the partner API launch next month," "The legal team needs to review this copy," "The CTO specifically asked for this to use the new design system."

## References

### Related Skills (chained in this workflow)
- `skills/product-knowledge-base/SKILL.md` — Phase 1: Knowledge retrieval foundation
- `skills/requirement-generator/SKILL.md` — Phase 2: Requirement generation
- `skills/ui-draft-generator/SKILL.md` — Phase 3: UI code generation
- `skills/product-sync-agent/SKILL.md` — Phase 4: Team synchronization

### Related Commands
- `commands/fullchain.md` — single command invocation of this workflow
- `commands/generate-requirement.md` — Phase 1-2 only
- `commands/generate-ui-draft.md` — Phase 3 only

### Related Agents
- `agents/agents-orchestrator.md` — defines the pipeline orchestration pattern
- `agents/product-manager.md` — PM role with PRD quality standards
- `agents/ui-designer.md` — UI design role with Arco Design expertise

### MCP Tools Used (all tools in sequence)
- `search_knowledge` — Phase 1 context retrieval + Phase 3 design docs
- `get_templates` — Phase 1 template loading
- `get_progress_board` — Phase 1 team context
- `create_requirement` — Phase 2 requirement storage
- `check_conflicts` — Phase 2 conflict detection
- `update_progress` — Phase 4 team sync

---

_Skill type: workflow_
_Suggested filename: SKILL.md_
_Suggested placement: skills/fullchain-efficiency/_
_Dependencies: MCP Server (pm-team-hub) configured; product knowledge base populated; all chained skills available_
