---
name: ui-draft-generator
description: Generate React + Arco Design UI code from requirement descriptions. Use when you want to skip the wireframe-to-visual-to-code pipeline and produce front-end-ready component code directly from a PRD.
intent: >-
  Guide product managers through AI-assisted generation of production-ready React + Arco Design UI code directly from requirement documents. The workflow maps requirement sections to UI components, applies Arco Design's component library systematically, and outputs TSX code that front-end engineers can directly integrate. Eliminates the traditional wireframe → visual design → front-end handoff pipeline for standard business interfaces.
type: workflow
theme: pm-artifacts
best_for:
  - "Generating front-end-ready UI code directly from a requirement document"
  - "Skipping the wireframe-to-visual-to-code pipeline for standard business interfaces"
  - "Producing consistent UI that follows your team's Arco Design component conventions"
scenarios:
  - "I just wrote a PRD for a new dashboard and want to generate the initial React code for the front-end team"
  - "I need a quick UI prototype for a settings page to share with stakeholders before committing engineering time"
  - "Our team uses Arco Design and I want AI-generated UI code that matches our component library"
estimated_time: "10-20 min"
---

## Purpose

The traditional path from requirement to UI is: PM writes PRD → designer creates wireframes → designer creates visual mockups → front-end developer translates to code. For standard business interfaces (dashboards, forms, tables, settings pages), this pipeline adds weeks of latency and multiple handoff points where information gets lost.

This skill short-circuits that pipeline by generating React + Arco Design TSX code directly from requirement descriptions. The output isn't a pixel-perfect final product — it's a **high-fidelity starting point** that captures 70-80% of the UI structure, component selection, and interaction logic. Front-end engineers refine rather than rebuild.

_When NOT to use this: Novel interaction patterns, brand-critical marketing pages, or complex data visualizations still benefit from dedicated designer involvement. This skill is for the 80% of interfaces that are variations of known patterns._

## Key Concepts

### Arco Design Component Mapping

The skill maps requirement concepts to specific Arco Design components:

| Requirement Pattern | Arco Component(s) | When to Use |
|---|---|---|
| "User fills out..." | `Form`, `Input`, `Select`, `DatePicker` | Any data entry flow |
| "Show a list of..." | `Table` with sort/filter/pagination | Structured data with >5 items |
| "Display details of..." | `Descriptions`, `Card` | Single entity detail view |
| "User navigates between..." | `Tabs`, `Menu`, `Breadcrumb` | In-page or cross-page navigation |
| "User uploads..." | `Upload.Dragger` | File upload functionality |
| "Confirm before..." | `Popconfirm`, `Modal` | Destructive or significant actions |
| "Show status of..." | `Tag`, `Badge`, `Steps` | Status indicators and progress |
| "Search/filter..." | `Input.Search`, `Select` with filters | Data filtering interfaces |
| "Page layout with sidebar" | `Layout`, `Layout.Sider`, `Layout.Content` | Page-level structure |
| "Cards in a grid" | `Grid.Row`, `Grid.Col`, `Card` | Card-based listing pages |
| "Edit rich text" | `Input.TextArea` + Markdown renderer | Content editing |
| "Show empty state" | `Empty` | No-data scenarios |
| "Loading state" | `Spin`, `Skeleton` | Async data loading |

### Code Output Standards

Every generated component must include:

1. **TypeScript interfaces** for all props
2. **Arco Design imports** (named imports from `@arco-design/web-react`)
3. **Tailwind CSS classes** for custom layout and spacing
4. **All interaction states**: default, hover, loading, empty, error
5. **Responsive breakpoints**: mobile-first with `Grid` responsive props
6. **Accessibility basics**: semantic HTML, ARIA labels for interactive elements

### The 70-80% Rule

AI-generated UI code is a starting point, not a final product. Expect:
- **Correct**: Component selection, layout structure, data flow, basic interactions (70-80%)
- **Needs refinement**: Micro-interactions, pixel-perfect spacing, edge case handling, brand-specific styling (20-30%)

## Application

### Phase 1: Requirement Analysis

**Goal**: Extract UI-relevant information from the requirement document.

**Activities**:

1. **Load the requirement** (if stored in the shared repository):
   ```
   Call: get_requirement(id="[requirement-id]")
   — or —
   Call: list_requirements(status="approved")
   ```

2. **Check for design guidelines** in the knowledge base:
   ```
   Call: search_knowledge(query="design system UI guidelines Arco Design component standards")
   ```

3. From the requirement, identify:
   - [ ] User stories → map each to a UI view or component
   - [ ] Data entities → determine display components (Table, Card, Descriptions)
   - [ ] User actions → determine interaction components (Button, Form, Modal)
   - [ ] Navigation flow → determine page structure (Tabs, Menu, Breadcrumb)

**Output**: A UI component map listing each page/section with its primary Arco components.

### Phase 2: Code Generation

**Goal**: Generate React + Arco Design TSX code for each identified UI component.

**Activities**:

1. Describe the UI you need. Be specific about:
   - What data is displayed (field names, types)
   - What actions users can take (create, edit, delete, filter)
   - How the page is structured (sidebar + content, tabs, single column)

2. The AI generates code following this **output template**:

```tsx
// [ComponentName].tsx
// Description: [what this component does]
// Requirement: [which requirement/user story this implements]
// Dependencies: @arco-design/web-react, react, tailwindcss

import React, { useState } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Space, 
  Tag, 
  Input,
  Typography 
} from '@arco-design/web-react';

const { Title } = Typography;

// TypeScript interfaces
interface DataItem {
  id: string;
  // ... fields from requirement
}

interface ComponentNameProps {
  // typed props
}

const ComponentName: React.FC<ComponentNameProps> = () => {
  // State management
  const [data, setData] = useState<DataItem[]>([]);
  const [loading, setLoading] = useState(false);

  // Columns definition (for Table components)
  const columns = [
    // ... columns mapping to data fields
  ];

  // Render with all states
  return (
    <div className="p-6">
      {/* Page header */}
      <div className="flex items-center justify-between mb-6">
        <Title heading={4}>Page Title</Title>
        <Space>
          <Button type="primary">Primary Action</Button>
        </Space>
      </div>

      {/* Main content */}
      <Card>
        <Table 
          columns={columns} 
          data={data} 
          loading={loading}
          pagination={{ pageSize: 10 }}
          noDataElement={<div>暂无数据</div>}
        />
      </Card>
    </div>
  );
};

export default ComponentName;
```

3. For multi-page features, generate each page component separately, then a routing configuration.

### Phase 3: Review & Handoff

**Goal**: Verify the generated code is usable and hand off to front-end.

**Activities**:

1. Review the generated code for:
   - [ ] All user stories have corresponding UI elements
   - [ ] Component imports are correct (`@arco-design/web-react`)
   - [ ] TypeScript interfaces match the data model
   - [ ] All interaction states are handled (loading, empty, error)
   - [ ] Responsive layout is present (Grid responsive props or Tailwind breakpoints)

2. Add TODO comments for areas needing front-end refinement:
   ```tsx
   // TODO: Replace mock data with actual API call
   // TODO: Add form validation rules
   // TODO: Implement search debounce
   ```

3. Package the output for the front-end team:
   - Component files (`.tsx`)
   - Required dependencies list
   - Notes on which requirement sections each component implements

**Output**: A set of React component files ready for front-end integration.

## Examples

### Example: Knowledge Base Management Page

**Requirement excerpt**: "Users can upload product documents (MD, TXT, PDF), view a list of uploaded documents with metadata, search the knowledge base, and delete documents."

**Generated code** (excerpt):

```tsx
// KnowledgeBase.tsx
import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Upload,
  Input,
  Space,
  Tag,
  Popconfirm,
  Message,
  Typography,
  Statistic,
  Grid,
} from '@arco-design/web-react';
import { IconUpload, IconSearch, IconDelete } from '@arco-design/web-react/icon';

const { Title } = Typography;
const { Row, Col } = Grid;

interface KnowledgeDoc {
  id: string;
  title: string;
  doc_type: 'md' | 'txt' | 'pdf';
  chunks: number;
  created_at: string;
  size_bytes: number;
}

const KnowledgeBase: React.FC = () => {
  const [documents, setDocuments] = useState<KnowledgeDoc[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);

  const columns = [
    { title: '文档名称', dataIndex: 'title', sorter: true },
    {
      title: '类型',
      dataIndex: 'doc_type',
      render: (type: string) => (
        <Tag color={type === 'pdf' ? 'red' : type === 'md' ? 'blue' : 'green'}>
          {type.toUpperCase()}
        </Tag>
      ),
    },
    { title: '分块数', dataIndex: 'chunks' },
    { title: '上传时间', dataIndex: 'created_at', sorter: true },
    {
      title: '操作',
      render: (_: any, record: KnowledgeDoc) => (
        <Popconfirm title="确定删除此文档？" onOk={() => handleDelete(record.id)}>
          <Button type="text" status="danger" icon={<IconDelete />}>
            删除
          </Button>
        </Popconfirm>
      ),
    },
  ];

  const handleDelete = (id: string) => {
    // TODO: Call API to delete document
    Message.success('文档已删除');
  };

  return (
    <div className="p-6">
      {/* Statistics */}
      <Row gutter={16} className="mb-6">
        <Col span={8}>
          <Card>
            <Statistic title="文档总数" value={documents.length} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="总分块数" value={documents.reduce((sum, d) => sum + d.chunks, 0)} />
          </Card>
        </Col>
      </Row>

      {/* Upload area */}
      <Card className="mb-6">
        <Upload
          drag
          multiple
          accept=".md,.txt,.pdf"
          tip="支持 MD、TXT、PDF 格式文件"
          // TODO: Configure upload endpoint
        />
      </Card>

      {/* Document list */}
      <Card title="文档列表">
        <Table columns={columns} data={documents} loading={loading} pagination={{ pageSize: 10 }} />
      </Card>
    </div>
  );
};

export default KnowledgeBase;
```

_This is a 70% starting point. The front-end engineer adds: actual API integration, upload progress handling, search debounce, responsive adjustments for mobile, and error boundary._

## Common Pitfalls

### Pitfall 1: Generating UI Without a Requirement

**Symptom**: PM asks "generate a dashboard page" without specifying what data, what actions, what user stories.

**Consequence**: The AI produces a generic dashboard with placeholder charts and meaningless KPIs. It looks impressive in a demo but maps to no actual product need.

**Fix**: Always start from a requirement document (even a rough one). The minimum input is: what data is displayed, what actions users take, who the user persona is.

### Pitfall 2: Treating AI Code as Production-Ready

**Symptom**: PM sends the generated TSX directly to the front-end team with "here's the code, just deploy it."

**Consequence**: Generated code lacks error handling, API integration, edge cases, accessibility testing, and performance optimization. Front-end engineers lose trust in the process.

**Fix**: Frame the output correctly: "Here's a high-fidelity starting point with the component structure and Arco Design patterns. Please refine the API integration, add error handling, and adjust spacing/animations."

### Pitfall 3: Wrong Component Selection

**Symptom**: The AI uses a `Table` for 3 items, or a `Card` grid for 500 items.

**Consequence**: Poor UX — tables are overhead for small datasets, card grids don't scale for large datasets.

**Fix**: Apply the component mapping table in Key Concepts. Rule of thumb: <10 items and card-friendly data → `Card` grid. >10 items or tabular data → `Table`. 1 item detail → `Descriptions`.

### Pitfall 4: Ignoring Empty and Error States

**Symptom**: Generated code only handles the "happy path" — data loaded successfully, list has items.

**Consequence**: Users see blank screens when data is loading, cryptic errors when API fails, or confusing layouts when lists are empty.

**Fix**: Every generated component must handle: loading (show `Spin` or `Skeleton`), empty (show `Empty` with message), error (show error message with retry button). If the generated code doesn't include these, add them before handoff.

## References

### Related Skills
- `skills/requirement-generator/SKILL.md` — generates the requirement documents that feed into this skill
- `skills/product-knowledge-base/SKILL.md` — provides design system docs for better code generation

### Related Commands
- `commands/generate-ui-draft.md` — one-command shortcut for this workflow
- `commands/fullchain.md` — runs requirement generation + UI generation in sequence

### Related Agents
- `agents/ui-designer.md` — UI Designer agent with comprehensive Arco Design component mapping
- `agents/ux-architect.md` — UX Architect for information architecture and layout frameworks

### MCP Tools Used
- `search_knowledge` — retrieve design system guidelines and component standards
- `get_templates` — load UI pattern templates

### External References
- [Arco Design React Components](https://arco.design/react/docs/start)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

---

_Skill type: workflow_
_Suggested filename: SKILL.md_
_Suggested placement: skills/ui-draft-generator/_
_Dependencies: Arco Design knowledge in the product knowledge base (recommended)_
