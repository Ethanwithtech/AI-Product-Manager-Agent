---
name: generate-ui-draft
description: Generate React + Arco Design UI code from a requirement document, with design system context from the knowledge base.
argument-hint: "<requirement title or ID, or paste requirement content>"
uses:
  - product-knowledge-base
  - ui-draft-generator
outputs:
  - React + Arco Design TSX component files
  - Component dependency list
  - Handoff notes with TODO items
---

# /generate-ui-draft

Generate front-end-ready React + Arco Design code from a requirement document, using design system context from the product knowledge base.

## Invocation

```
/generate-ui-draft Smart Notification System requirement
```

Or with an existing requirement ID:

```
/generate-ui-draft --requirement-id 42
```

## Workflow

1. **Load Requirement** (uses: `product-knowledge-base`)
   - If a requirement ID is provided, call `get_requirement` to load it from the shared repository.
   - If a title/description is provided, call `search_knowledge` to find the matching requirement and related design docs.
   - Call `search_knowledge` specifically for design system guidelines (Arco Design conventions, component patterns, spacing/color tokens).

2. **Analyze & Map** (uses: `ui-draft-generator`)
   - Extract UI-relevant information from the requirement: user stories → pages/views, data entities → display components, user actions → interaction components.
   - Map requirement patterns to Arco Design components using the component mapping table.
   - Identify the page structure (layout type, navigation, number of views).

3. **Generate Code** (uses: `ui-draft-generator`)
   - For each identified page/view, generate a complete React + TypeScript component:
     - Arco Design component imports
     - TypeScript interfaces for data types
     - State management hooks
     - All interaction states (loading, empty, error, success)
     - Tailwind CSS for custom layout
     - Responsive breakpoints
   - Add TODO comments for areas needing front-end refinement.

4. **Package Output**
   - Compile all generated components into a delivery package.
   - List required npm dependencies.
   - Write handoff notes explaining which requirement sections each component implements.

## Checkpoints

- [ ] Requirement document is loaded and understood
- [ ] Design system context is retrieved from knowledge base
- [ ] Every user story has a corresponding UI element
- [ ] Component selection matches data patterns (Table for lists, Form for input, Card for items)
- [ ] All components handle loading, empty, and error states
- [ ] Responsive design is present in all components
- [ ] TypeScript interfaces are correctly typed
- [ ] Arco Design imports are from `@arco-design/web-react`

## Next Steps

- Share components with front-end team for refinement and API integration
- If no requirement exists yet, run `/generate-requirement` first
- For the full end-to-end pipeline, use `/fullchain` instead
