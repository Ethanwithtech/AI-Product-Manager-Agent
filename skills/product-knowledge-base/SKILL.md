---
name: product-knowledge-base
description: Organize and maintain a product knowledge base for AI-powered context retrieval. Use when setting up or improving the shared knowledge repository that powers all MCP-based PM skills.
intent: >-
  Teach product managers how to build and maintain a high-quality product knowledge base using MCP tools. Covers document taxonomy, content preparation best practices, embedding strategies, retrieval optimization, and knowledge base hygiene routines. A well-maintained knowledge base is the foundation for all AI-assisted PM workflows — requirement generation, UI drafting, and product decisions all depend on the quality of retrievable context.
type: component
theme: pm-infrastructure
best_for:
  - "Setting up a product knowledge base from scratch for your PM team"
  - "Improving retrieval quality when AI-generated documents lack product-specific context"
  - "Establishing knowledge base maintenance routines for your team"
scenarios:
  - "I'm setting up the MCP knowledge base for our team and need to know what documents to upload first"
  - "Our AI-generated PRDs are too generic — they don't reference our actual product constraints and specs"
  - "Our knowledge base has 200 documents but search results are often irrelevant"
estimated_time: "30-60 min (initial setup), 10 min/week (maintenance)"
---

## Purpose

Every AI-powered PM skill in this toolkit depends on one thing: **context quality**. When you call `search_knowledge` to retrieve product information before generating a requirement or UI draft, the quality of that retrieval determines whether the AI output is product-aware or generically plausible. This skill teaches you how to build and maintain the knowledge base that makes all other skills work well.

Think of the knowledge base as the AI's "product memory." If that memory is disorganized, outdated, or incomplete, every AI interaction suffers. If it's well-curated, every AI interaction improves.

## Key Concepts

### Document Taxonomy

Organize documents into categories that match how PMs think about product information:

| Category | What Goes Here | Examples | Priority |
|----------|---------------|---------|----------|
| **Product Specs** | Feature specifications, system architecture | Feature spec docs, API docs, data models | 🔴 High — upload first |
| **Design System** | UI guidelines, component standards, brand rules | Arco Design conventions, color/spacing tokens | 🔴 High — critical for UI generation |
| **User Research** | Interview transcripts, survey results, personas | User interview notes, persona docs, journey maps | 🟡 Medium — improves requirement quality |
| **Business Context** | Strategy docs, OKRs, competitive analysis | Product strategy, quarterly OKRs, competitor briefs | 🟡 Medium — improves prioritization |
| **Historical Decisions** | ADRs, retrospectives, post-mortems | Architecture Decision Records, sprint retros | 🟢 Low — useful but not urgent |
| **Process & Templates** | Team conventions, review checklists | PRD templates, code review guidelines, DoD | 🟢 Low — better stored as Templates via MCP |

### Document Preparation

Raw documents often produce poor retrieval results. Preparation improves quality:

1. **Clear Headings**: Use descriptive headings that match how PMs would search. "User Authentication Flow" > "Section 3.2.1"
2. **Self-Contained Sections**: Each section should make sense without reading the whole document. The chunking algorithm splits on headings — if a chunk references "the above diagram" but the diagram is in a different chunk, context is lost.
3. **Explicit Metadata**: Start each document with a brief summary: what it covers, when it was written, who it's for.
4. **Remove Noise**: Delete boilerplate headers/footers, table of contents, page numbers, meeting logistics. These dilute retrieval relevance.

### Retrieval Quality

The knowledge base uses **semantic search** — it finds documents by meaning, not keyword matching. This means:

- ✅ Searching "how does checkout work?" will find a doc titled "Payment Processing Flow"
- ✅ Searching "user frustration with search" will find a doc about "Search UX Research Q3"
- ❌ Searching "checkout" won't necessarily rank higher than searching with a full question
- ❌ Very short queries ("auth") produce worse results than descriptive queries ("user authentication error handling")

_Rule of thumb: Search with the question you'd ask a colleague, not with a keyword._

## Application

### Step 1: Initial Knowledge Base Setup

**Gather your priority documents** (start with Product Specs and Design System):

```
For each document:
  Call: add_knowledge_document(
    title="[descriptive title]",
    content="[prepared document content]",
    doc_type="md"  // or "txt", "pdf"
  )
```

**Recommended upload order** (most impactful first):
1. Product feature specifications (current state)
2. Design system documentation (component guidelines, patterns)
3. Active requirement documents (in-flight PRDs)
4. User research summaries (not raw transcripts — too noisy)
5. Business strategy briefs (current quarter priorities)

### Step 2: Verify Retrieval Quality

After uploading, test that the knowledge base returns relevant results:

```
Call: search_knowledge(query="how does our checkout flow work?", top_k=5)
```

Check:
- [ ] Top result is directly relevant to the query
- [ ] Results come from the expected document category
- [ ] Returned content chunks are self-contained and meaningful
- [ ] No irrelevant results in top 3

If retrieval quality is poor:
- **Too many irrelevant results** → Your documents have too much boilerplate. Clean them.
- **Missing expected results** → The document may not be uploaded, or the relevant section lacks descriptive headings.
- **Results are too generic** → Add more specific product context to your documents.

### Step 3: Establish Maintenance Routine

Knowledge bases degrade over time. Set a weekly 10-minute routine:

| Frequency | Action | MCP Tool |
|-----------|--------|----------|
| Weekly | Upload new PRDs and design docs | `add_knowledge_document` |
| Weekly | Remove outdated specs for shipped/cancelled features | `delete_knowledge_document` (via Web Admin) |
| Monthly | Review retrieval quality with test queries | `search_knowledge` |
| Quarterly | Audit full document list, archive stale content | Web Admin → Knowledge Base page |

### Step 4: Team Convention

Establish a team agreement:

- **When creating a new PRD**: Upload it to the knowledge base after approval.
- **When shipping a feature**: Update the product spec in the knowledge base to reflect the shipped state.
- **When cancelling a feature**: Archive (don't delete) the spec — it's useful context for "why we didn't do X."

## Examples

### Example 1: Setting Up a Knowledge Base from Scratch

**Scenario**: New PM team with 3 PMs, building an e-commerce platform. No existing knowledge base.

**Step 1**: PM lead gathers 5 priority documents:
```
1. "Product Architecture Overview" (15 pages) → upload as-is
2. "Arco Design Component Guidelines" (team-specific conventions) → upload after removing generic Arco docs
3. "Checkout Flow v2 PRD" (current in-flight) → upload
4. "User Research: Search Experience" (interview summary) → upload the summary, not raw transcripts
5. "Q1 OKRs and Priorities" → upload
```

**Step 2**: Test retrieval:
```
search_knowledge("what payment methods do we support?")
→ Returns: Checkout Flow v2 PRD section on payment integration ✅

search_knowledge("what did users say about search?")  
→ Returns: User Research summary on search frustration ✅

search_knowledge("what's our design system color palette?")
→ Returns: Arco Design Component Guidelines color section ✅
```

**Step 3**: PM sets up a weekly Monday routine: review new docs from last week, upload relevant ones, delete outdated ones.

### Example 2: Improving Poor Retrieval Quality

**Problem**: PM calls `search_knowledge("user authentication")` but gets results about "product catalog search" instead.

**Diagnosis**: The authentication spec document has a generic title ("System Spec v3.2") and the auth section is buried in a large multi-topic document.

**Fix**:
1. Split the monolithic "System Spec v3.2" into focused documents: "User Authentication System", "Product Catalog Architecture", "Payment Processing Flow"
2. Add descriptive headings to each section
3. Re-upload the focused documents
4. Delete the monolithic original
5. Test again: `search_knowledge("user authentication")` → now returns "User Authentication System" ✅

## Common Pitfalls

### Pitfall 1: Upload Everything Approach

**Symptom**: Team uploads every document they have — meeting notes, email threads, draft brainstorms, raw interview transcripts.

**Consequence**: Knowledge base becomes noisy. Search results mix authoritative specs with casual meeting notes. AI generates requirements citing someone's unfinished brainstorm as if it were a product decision.

**Fix**: Curate aggressively. Only upload documents that represent team-approved decisions, completed research, or current specifications. Meeting notes and brainstorms belong in your note-taking tool, not the knowledge base.

### Pitfall 2: Set and Forget

**Symptom**: Knowledge base is populated once and never updated.

**Consequence**: After 3 months, the AI references outdated specs, deprecated features, and old priorities. PMs stop trusting the AI output and stop using the skills.

**Fix**: The 10-minute weekly maintenance routine is non-negotiable. Assign a rotating "knowledge base owner" each week if needed. Treat it like code — stale docs are tech debt.

### Pitfall 3: Monolithic Documents

**Symptom**: One 50-page document covers everything from authentication to payment to search.

**Consequence**: When the chunking algorithm splits this document, chunks lose context. A chunk about "error handling" might come from the auth section or the payment section — the AI can't tell which.

**Fix**: Split large documents into focused, single-topic files. Each file should cover one feature area, one research topic, or one design subsystem. Aim for 2-10 pages per document.

### Pitfall 4: No Metadata or Context

**Symptom**: Documents are uploaded without titles, dates, or authorship context.

**Consequence**: When the AI retrieves a chunk, it can't assess recency, authority, or relevance. A 2-year-old spec and a current spec look identical.

**Fix**: Every document should start with: title, date, author/owner, status (current/deprecated/draft), and a 2-sentence summary of what it covers.

## References

### Related Skills
- `skills/requirement-generator/SKILL.md` — primary consumer of knowledge base context
- `skills/ui-draft-generator/SKILL.md` — uses design system docs from the knowledge base
- `skills/product-sync-agent/SKILL.md` — progress board data complements knowledge base context

### MCP Tools Used
- `add_knowledge_document` — upload documents to the knowledge base
- `search_knowledge` — semantic search for relevant document chunks
- `list_knowledge_documents` — view all documents in the knowledge base (via REST API)
- `delete_knowledge_document` — remove outdated documents (via REST API)

### External References
- RAG (Retrieval-Augmented Generation) best practices
- Document chunking strategies for vector databases

---

_Skill type: component_
_Suggested filename: SKILL.md_
_Suggested placement: skills/product-knowledge-base/_
_Dependencies: MCP Server (pm-team-hub) configured and running_
