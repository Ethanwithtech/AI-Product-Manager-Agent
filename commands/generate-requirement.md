---
name: generate-requirement
description: Generate a structured requirement document by chaining knowledge retrieval, AI generation, and team sync via MCP tools.
argument-hint: "<feature description or problem statement>"
uses:
  - product-knowledge-base
  - requirement-generator
  - product-sync-agent
outputs:
  - Structured requirement document (PRD format)
  - Conflict detection report
  - Progress board update
---

# /generate-requirement

Generate a structured requirement document from a natural language feature description, powered by product knowledge base context and automatic team synchronization.

## Invocation

```
/generate-requirement I want to add a smart notification system that learns user preferences and reduces notification fatigue
```

## Workflow

1. **Retrieve Context** (uses: `product-knowledge-base`)
   - Call `search_knowledge` with the feature description to find related product specs, design docs, and user research.
   - Call `get_templates` to load the team's PRD template (falls back to default if none exists).
   - Call `get_progress_board` to check what other PMs are currently working on.

2. **Generate Requirement** (uses: `requirement-generator`)
   - Combine the retrieved context + feature description + PRD template.
   - AI generates a structured requirement document with all standard sections: Problem Statement, User Stories, Success Metrics, Solution Overview, Technical Considerations, Release Plan.
   - Review the output for completeness and product-specific accuracy.

3. **Store & Sync** (uses: `product-sync-agent`)
   - Call `create_requirement` to store the approved requirement in the shared repository.
   - Call `check_conflicts` with the requirement's modules and keywords to detect overlaps.
   - If no conflicts: done. If conflicts detected: review and notify affected PMs.

## Checkpoints

- [ ] Knowledge base results are relevant to the feature topic
- [ ] Generated PRD has all 7 standard sections populated
- [ ] Success metrics include baselines and targets (not vague "improve X")
- [ ] Out of Scope section lists at least 3 explicit exclusions
- [ ] Requirement is stored in shared repository
- [ ] Conflict check completed (conflicts addressed or acknowledged)

## Next Steps

- Run `/generate-ui-draft` to produce React + Arco Design code from the generated requirement
- Run `/fullchain` to do both requirement and UI generation in one pass
- Share the requirement with stakeholders for review before sprint planning
