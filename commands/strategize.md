---
name: strategize
description: Run the PM Strategist autonomous product planning pipeline — from customer need to validated product strategy with GAN-style critique loop.
argument-hint: "<customer need description> [--repo <path>] [--constraints <known constraints>]"
uses:
  - pm-strategist
  - problem-statement
  - jobs-to-be-done
  - product-knowledge-base
  - requirement-generator
  - roadmap-planning
  - multi-perspective-evaluation
  - proto-persona
  - prioritization-advisor
outputs:
  - Complete product strategy document
  - Three-proposal comparison (conservative / balanced / aggressive)
  - Recommended proposal with full PRD
  - Risk register
  - Implementation roadmap
  - Critic review audit trail
---

# /strategize

Run the PM Strategist's five-role autonomous pipeline with GAN-style generate-critique iteration. Input a customer need; get a validated product strategy with zero human intervention during execution.

## Invocation

```text
/strategize Our e-commerce platform needs an intelligent recommendation system.
Users report "Guess You Like" is completely inaccurate — click-through rate is 2%
vs industry average of 8%. Team: 3 backend + 2 frontend, no ML engineers.
Must launch by Q3, budget <= 200K/month. Repo: /path/to/ecommerce-platform
```

Or minimal:

```text
/strategize Customers want real-time collaboration features in our document editor
```

## Workflow

### Phase 1: Planner — Problem Decomposition
1. Extract goals, users, scenarios, constraints from the customer input.
2. Build structured problem statement with `problem-statement`.
3. Uncover user jobs with `jobs-to-be-done`.
4. Construct hypothesis tree with evidence and failure conditions.
5. Define success metrics (baseline → target → measurement method).
6. Set explicit scope boundaries (IN / OUT / DEFERRED).

**Quality gate**: Problem statement exists, ≥2 user segments identified, ≥2 hypotheses with testable conditions.

### Phase 2: Researcher — Context & Code Analysis
1. If repo provided: invoke `code-explorer` subagent to analyze directory structure, key modules, APIs, data models, configs, and tests.
2. Call `search_knowledge` to retrieve relevant product docs and historical decisions.
3. Call `get_templates` to load PRD template.
4. Call `get_progress_board` to check in-flight work.
5. Build capability-opportunity map and flag information gaps.

**Quality gate**: Tech stack identified, ≥3 knowledge base docs retrieved (or gap flagged), capability map complete.

### Phase 3: Synthesizer — Three-Proposal Generation
1. Generate three genuinely differentiated proposals (conservative / balanced / aggressive).
2. For each proposal: full PRD skeleton via `requirement-generator`, phased roadmap via `roadmap-planning`.
3. If user-facing: build personas via `proto-persona`.
4. Write trade-off analysis and pre-loaded self-critique per proposal.
5. Produce side-by-side comparison table.

**Quality gate**: Three proposals differ in technical approach (not just wording), each has PRD + roadmap + trade-offs + "why this might be wrong."

### Phase 4: Critic — GAN Discriminator Loop
1. Establish Sprint Contract: define "what counts as a good proposal" with specific, scoreable criteria.
2. Run `multi-perspective-evaluation` (5 dimensions) on each proposal.
3. Score each proposal on 4 axes: Requirement Fit (30%), Technical Feasibility (25%), Business Value (25%), Risk Control (20%).
4. For proposals scoring < 7.0 weighted total: issue specific revision requirements.
5. Refiner rewrites only failing dimensions → Critic re-scores.
6. Repeat up to 4 rounds. If still < 7.0 after 4 rounds: take highest score + attach "Known Limitations."

**Quality gate**: All proposals scored, score spread > 1.0 across proposals, no vague critiques.

### Phase 5: Validator — Final Consistency Check
1. Run 8-point validation checklist on the recommended (highest-scoring) proposal.
2. Verify problem-need alignment, code feasibility, metric measurability, risk actionability, timeline realism, internal consistency, scope clarity, honest self-critique.
3. Produce confidence assessment (High/Medium/Low) with key uncertainty identified.
4. If APPROVED: compile final strategy document.
5. If NEEDS REVISION: route back to Synthesizer with specific revision instructions.

**Quality gate**: All 8 checks addressed, final verdict is APPROVED (or max revision cycles exhausted).

### Final Assembly
Compile all phase outputs into the 11-section Product Strategy Document:
1. Executive Summary
2. Problem Definition
3. Technical & Product Context
4. Three Proposals Compared
5. Critical Review Record
6. Recommended Proposal (full PRD)
7. Implementation Roadmap
8. Risk Register
9. Success Metrics & Measurement Plan
10. Known Limitations & Open Questions
11. Appendix: Iteration Log

Store the recommended PRD via `create_requirement` MCP tool.

## Checkpoints

- **After Phase 1**: Confirm problem is framed as a user problem, not a feature request.
- **After Phase 2**: Confirm technical constraints are grounded in actual code analysis, not assumptions.
- **After Phase 3**: Confirm three proposals are genuinely different strategies, not parameter variations.
- **After Phase 4**: Confirm Critic found real issues (not rubber-stamped). Score spread should be meaningful.
- **After Phase 5**: Confirm the final document is internally consistent and actionable.

## Key Principles

- **No human intervention during execution**: The pipeline runs autonomously from input to output.
- **Critic is the most important role**: Without it, the system degenerates into a "confident idea generator" — which is exactly what we don't want.
- **Uncertainty is a feature, not a bug**: The output should honestly say "I don't know X" rather than fabricate confidence.
- **Evidence > opinion**: Every claim references code, data, or knowledge base docs. Ungrounded claims are marked as assumptions.
- **Iteration has diminishing returns**: 4 rounds max. After that, the bottleneck is input quality, not iteration count.

## Next Steps

After `/strategize` completes:
- Run `/generate-requirement` to further refine the recommended PRD with additional detail.
- Run `/strategy` if broader positioning and competitive strategy work is needed.
- Run `/plan-roadmap` for release-level sequencing of the implementation phases.
- Run `/fullchain` to extend the recommended proposal through UI draft generation.
- Hand off to `agents/product-manager.md` (Alex) for day-to-day PM execution.
