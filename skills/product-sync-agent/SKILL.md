---
name: product-sync-agent
description: Sync product progress across your PM team using MCP tools. Use when multiple PMs work on the same product and need to detect conflicts, share status, and maintain a shared progress board.
intent: >-
  Guide product managers through establishing and maintaining a team-wide product progress synchronization practice using MCP-powered shared tools. Covers progress reporting conventions, conflict detection workflows, notification strategies, and kanban board management to eliminate information silos between PMs working on the same product.
type: interactive
theme: pm-collaboration
best_for:
  - "Keeping multiple PMs aligned on a shared product"
  - "Detecting feature conflicts and dependency overlaps before they cause rework"
  - "Maintaining a real-time team progress board without manual status meetings"
scenarios:
  - "I just started scoping a new feature and want to check if another PM is already working on something that overlaps"
  - "Our PM team keeps stepping on each other's toes — features conflict and nobody finds out until sprint review"
  - "I need to set up a progress sync practice for our 4-person PM team"
estimated_time: "15-30 min"
---

## Purpose

Product teams with multiple PMs face a persistent problem: **information silos**. PM-A scopes a notification system while PM-B redesigns the settings page that houses notifications — neither knows about the other until a sprint review collision. This skill teaches you how to use MCP-powered shared tools to maintain continuous progress visibility across your PM team, detect conflicts early, and communicate changes proactively.

The goal is not more meetings or more process. The goal is **ambient awareness** — every PM knows enough about what others are doing to make informed decisions, without dedicating time to status synchronization.

## Key Concepts

### Progress Board

A shared kanban-style board where each PM's active work items are visible to the entire team. Items move through four stages:

| Stage | Meaning | Who Cares |
|-------|---------|-----------|
| **Planning** | PM is scoping/researching | Other PMs — for early conflict detection |
| **In Progress** | Active development underway | Engineers — for dependency awareness |
| **Review** | In stakeholder/QA review | Everyone — imminent changes to the product |
| **Done** | Shipped and measured | Future PMs — for context on what exists |

### Conflict Detection

Two types of conflicts that the MCP tools can detect:

1. **Module Overlap**: Two PMs are both modifying the same product module (e.g., "checkout flow," "user profile," "notifications").
2. **Keyword Overlap**: Two requirements share significant keyword overlap, suggesting they may affect the same user experience even if they target different modules.

_Neither type is automatically a problem. Overlap detection is a conversation starter, not a stop signal._

### Notification Strategy

Not all changes deserve a notification. The framework:

| Change Type | Notify? | Channel |
|------------|---------|---------|
| New item enters "Planning" | Yes — async | Progress board (pull-based) |
| Conflict detected | Yes — push | Direct notification to affected PM |
| Item moves to "In Progress" | No | Board update only |
| Item moves to "Done" | Yes — async | Team summary |
| Item is archived/cancelled | Yes — if others had dependency | Direct notification |

## Application

This skill uses a conversational flow. Ask the following questions to assess the PM's situation, then provide tailored recommendations.

### Question 1: Team Setup Assessment

> How many PMs are on your team, and do you share ownership of any product areas (modules, features, user segments)?

**Why this matters**: Solo PM teams don't need sync tooling. Teams with clear ownership boundaries need lighter sync than teams with overlapping domains.

**Recommendations based on answer**:
1. **2-3 PMs, clear ownership** → Lightweight setup: board + monthly conflict scans
2. **2-3 PMs, overlapping areas** → Standard setup: board + per-commit conflict checks
3. **4-5 PMs, heavy overlap** → Full setup: board + real-time conflict detection + notification rules
4. **Other** → describe your situation

### Question 2: Current Pain Points

> What's the most recent example of a PM conflict or information gap on your team? (e.g., duplicate work, broken feature interaction, stakeholder confusion)

**Why this matters**: The specific pain shapes the sync strategy. Duplicate work needs better planning-stage visibility. Broken interactions need module-level conflict detection. Stakeholder confusion needs better status communication.

**Recommendations based on answer**:
1. **Duplicate/overlapping work** → Focus on planning-stage sync and conflict detection
2. **Features breaking each other** → Focus on module tagging and dependency mapping
3. **Stakeholders getting conflicting info** → Focus on shared board visibility and naming conventions
4. **No specific incident, just want prevention** → Start with basic board setup and iterate
5. **Other** → describe

### Question 3: MCP Configuration

> Have you already configured the PM Team Hub MCP Server in your CodeBuddy, or do you need setup guidance?

**Recommendations based on answer**:
1. **Already configured** → Proceed to workflow setup
2. **Not yet / need help** → Provide MCP configuration instructions (see docs/MCP-Setup-Guide.md)
3. **Don't know what MCP is** → Explain MCP concept, then guide setup

### Question 4: Workflow Definition

Based on answers to Q1-Q3, recommend a specific sync workflow:

**For lightweight setup:**
```
When starting new work:
1. Call `update_progress` with title, description, modules, status="planning"
2. Call `check_conflicts` to scan for overlaps
3. If conflicts found → reach out to the other PM before proceeding
4. When work advances → call `update_progress` to move status
```

**For full setup:**
```
When starting new work:
1. Call `get_progress_board` to review what everyone is working on
2. Call `update_progress` to register your new item
3. Call `check_conflicts` with your modules and keywords
4. If conflicts → review and discuss with affected PMs
5. On every status change → call `update_progress`
6. Before sprint planning → call `get_progress_board` for team overview
```

### Question 5: Review and Commitment

> Here's the sync workflow I recommend for your team. Which parts will you adopt now, and which would you like to defer?

Present the recommended workflow and let the PM choose which elements to implement immediately.

## Examples

### Example 1: Detecting a Module Overlap

**Scenario**: PM-A is scoping a "Smart Notifications" feature. She calls the MCP tools:

```
PM-A calls: check_conflicts(
  title="Smart Notifications System",
  modules=["notifications", "user-preferences", "mobile-push"],
  keywords=["notification", "alert", "push", "preference", "settings"]
)

Response:
{
  "conflicts": [
    {
      "type": "module_overlap",
      "your_item": "Smart Notifications System",
      "existing_item": "Settings Page Redesign (PM-B)",
      "overlap_modules": ["user-preferences"],
      "overlap_detail": "Both items modify the user-preferences module. PM-B's Settings Page Redesign is currently in 'in_progress' status.",
      "recommendation": "Coordinate with PM-B to ensure notification preferences UI aligns with the new settings page layout."
    }
  ]
}
```

**Outcome**: PM-A reaches out to PM-B. They discover PM-B's settings redesign moves the notification preferences to a new tabbed layout. PM-A adjusts her notification preferences UI to match the new tab structure, saving a week of rework.

### Example 2: Progress Board Review Before Sprint Planning

```
PM calls: get_progress_board()

Response:
{
  "planning": [
    {"title": "AI-Powered Search", "author": "PM-C", "modules": ["search", "ml-pipeline"]}
  ],
  "in_progress": [
    {"title": "Settings Page Redesign", "author": "PM-B", "modules": ["user-preferences", "account"]},
    {"title": "Checkout Flow v2", "author": "PM-A", "modules": ["checkout", "payments"]}
  ],
  "review": [
    {"title": "Onboarding Wizard", "author": "PM-D", "modules": ["onboarding", "user-profile"]}
  ],
  "done": []
}
```

The PM can now see the full team workload at a glance — no standup meeting required.

## Common Pitfalls

### Pitfall 1: Notification Fatigue

**Symptom**: PMs start ignoring progress notifications because there are too many of them.

**Consequence**: The sync system becomes noise, and real conflicts get buried in routine updates.

**Fix**: Apply the notification strategy table above. Only push-notify on actual conflicts. Use the board as a pull-based system for general awareness. If more than 3 notifications per PM per day, your granularity is too fine.

### Pitfall 2: Over-Tagging Modules

**Symptom**: Every feature claims to affect 8+ modules, making conflict detection useless (everything conflicts with everything).

**Consequence**: False positive conflicts erode trust in the system. PMs stop running conflict checks.

**Fix**: Limit module tags to 1-3 per item. Tag only the modules where you're making _structural changes_, not modules you merely _read from_. If "user-profile" is just a data source for your feature, don't tag it.

### Pitfall 3: Stale Board

**Symptom**: Items sit in "In Progress" for months. The board doesn't reflect reality.

**Consequence**: New PMs can't trust the board to make decisions. The system degrades to decoration.

**Fix**: Set a team convention — items in "Planning" for >2 weeks must be moved to "In Progress" or archived. Items in "In Progress" for >1 sprint must be status-checked. Automate reminders if possible.

### Pitfall 4: Treating Conflicts as Blockers

**Symptom**: When a conflict is detected, PMs freeze and wait for a meeting to resolve it.

**Consequence**: The sync system slows down the team instead of speeding it up.

**Fix**: Conflicts are conversation starters, not stop signs. The default response is a 5-minute DM or async message: "Hey, I see we're both touching [module]. Here's my plan — does this conflict with yours?" Most conflicts resolve in minutes.

## References

### Related Skills
- `skills/prd-development/SKILL.md` — for creating the requirements that get tracked on the board
- `skills/requirement-generator/SKILL.md` — for AI-assisted requirement generation with automatic progress tracking

### MCP Tools Used
- `update_progress` — register and update work items on the shared board
- `get_progress_board` — retrieve the full team progress view
- `check_conflicts` — detect module and keyword overlaps with other PMs' work

### External Frameworks
- Kanban board methodology (David J. Anderson)
- Team Topologies — interaction modes for reducing cognitive load across teams

---

_Skill type: interactive_
_Suggested filename: SKILL.md_
_Suggested placement: skills/product-sync-agent/_
_Dependencies: MCP Server (pm-team-hub) configured and running_
