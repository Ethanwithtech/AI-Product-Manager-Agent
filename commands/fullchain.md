---
name: fullchain
description: Run the complete feature pipeline from idea to front-end code — knowledge retrieval, requirement generation, conflict detection, UI code generation, and team sync in one pass.
argument-hint: "<feature idea or problem description>"
uses:
  - product-knowledge-base
  - requirement-generator
  - ui-draft-generator
  - product-sync-agent
  - fullchain-efficiency
outputs:
  - Structured requirement document (stored in shared repository)
  - Conflict detection report
  - React + Arco Design component files
  - Progress board update
  - Complete delivery package
---

# /fullchain

Run the complete PM pipeline from feature idea to front-end-ready code in a single session. Chains knowledge retrieval → requirement generation → conflict detection → UI code generation → team synchronization.

## Invocation

```
/fullchain I want to build a team activity feed that shows when PMs create requirements, update progress, or upload documents — so the team stays informed without checking each section separately
```

## Workflow

1. **Context Assembly** (uses: `product-knowledge-base`)
   - Call `search_knowledge` with the feature description to retrieve product specs, design docs, and user research.
   - Call `get_templates` to load the team's PRD template.
   - Call `get_progress_board` to understand current team workload.
   - **Quality Gate**: Confirm retrieved context is relevant. If critical docs are missing, pause and upload them.

2. **Requirement Generation** (uses: `requirement-generator`)
   - Generate a structured PRD combining: PM's feature description + knowledge base context + team template.
   - AI produces all standard sections: Problem Statement, User Stories, Success Metrics, Solution Overview, Technical Considerations, Release Plan.
   - Call `create_requirement` to store in shared repository.
   - Call `check_conflicts` to detect module/keyword overlaps with other PMs.
   - **Quality Gate**: Verify PRD completeness. If conflicts detected, flag for PM review.

3. **UI Code Generation** (uses: `ui-draft-generator`)
   - Analyze the requirement to identify pages, components, and interaction patterns.
   - Retrieve design system docs: `search_knowledge` for Arco Design conventions.
   - Generate React + Arco Design TSX for each page/view with full state handling.
   - **Quality Gate**: Verify user story coverage, component selection, responsive design, state handling.

4. **Team Sync & Delivery** (uses: `product-sync-agent`)
   - Call `update_progress` to register the new feature on the team progress board.
   - Compile the complete delivery package:
     ```
     Delivery Package:
     ├── requirement.md        — Full PRD document
     ├── conflict-report.md    — Detected conflicts (if any)
     ├── components/
     │   ├── [Page].tsx        — React components per page
     │   └── ...
     └── handoff-notes.md      — Dependencies, TODOs, refinement areas
     ```
   - **Quality Gate**: Confirm progress board is updated and delivery package is complete.

## Checkpoints

### Phase 1: Context
- [ ] Knowledge base returns relevant documents (top 3 are on-topic)
- [ ] PRD template is loaded (custom or default)
- [ ] Team progress board reviewed for potential overlaps

### Phase 2: Requirement
- [ ] All 7 PRD sections are populated
- [ ] Problem statement cites evidence from knowledge base
- [ ] Success metrics have baselines, targets, and timeframes
- [ ] Out of Scope is explicit (≥3 items)
- [ ] Requirement stored in shared repository
- [ ] Conflict check completed

### Phase 3: UI Code
- [ ] Every user story maps to a UI element
- [ ] Arco Design components match data patterns
- [ ] Loading, empty, and error states handled
- [ ] Responsive design present
- [ ] TypeScript types are correct

### Phase 4: Delivery
- [ ] Progress board updated with new item
- [ ] All artifacts compiled into delivery package
- [ ] Handoff notes explain what needs front-end refinement

## Next Steps

- Share the delivery package with the front-end team
- If conflicts were detected, resolve with affected PMs before sprint planning
- Schedule a review with stakeholders using the generated PRD
- Upload any new design decisions back to the knowledge base for future reference
