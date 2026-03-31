#!/usr/bin/env bash
#
# package-skills-for-codebuddy.sh — Package PM skills + agents for CodeBuddy installation.
#
# This script packages the PM Team Toolkit skills and agent definitions
# into a format that CodeBuddy can import. It creates:
#   1. Individual skill folders with sanitized SKILL.md files
#   2. Agent role definitions
#   3. A manifest.json for CodeBuddy plugin discovery
#
# Usage:
#   ./scripts/package-skills-for-codebuddy.sh                    # Package all PM toolkit skills
#   ./scripts/package-skills-for-codebuddy.sh --output dist/cb   # Custom output directory
#   ./scripts/package-skills-for-codebuddy.sh --zip               # Also create ZIP archives
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$ROOT/dist/codebuddy-skills"
CREATE_ZIP=false

# PM Toolkit skills to package
PM_TOOLKIT_SKILLS=(
  "product-knowledge-base"
  "requirement-generator"
  "ui-draft-generator"
  "product-sync-agent"
  "fullchain-efficiency"
  "feedback-insight-engine"
)

# Agent definitions to include
AGENT_FILES=(
  "product-manager.md"
  "ui-designer.md"
  "ux-architect.md"
  "sprint-prioritizer.md"
  "feedback-synthesizer.md"
  "agents-orchestrator.md"
)

# ─── Argument parsing ───

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --zip)
      CREATE_ZIP=true
      shift
      ;;
    -h|--help)
      cat <<EOF
Usage: $0 [OPTIONS]

Package PM Team Toolkit skills and agents for CodeBuddy installation.

Options:
  --output <dir>   Output directory (default: dist/codebuddy-skills)
  --zip            Also create ZIP archives for each skill
  -h, --help       Show this help

Packaged skills: ${PM_TOOLKIT_SKILLS[*]}
EOF
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$1'. Run '$0 --help' for usage." >&2
      exit 1
      ;;
  esac
done

# ─── Setup ───

if [[ "$OUTPUT_DIR" != /* ]]; then
  OUTPUT_DIR="$ROOT/$OUTPUT_DIR"
fi

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/skills" "$OUTPUT_DIR/agents" "$OUTPUT_DIR/commands"

# ─── Package Skills ───

echo "📦 Packaging PM Toolkit skills..."

for skill_name in "${PM_TOOLKIT_SKILLS[@]}"; do
  skill_dir="$ROOT/skills/$skill_name"

  if [[ ! -d "$skill_dir" ]]; then
    echo "  ⚠️  Skill not found: $skill_name (skipping)"
    continue
  fi

  target_dir="$OUTPUT_DIR/skills/$skill_name"
  mkdir -p "$target_dir"

  # Copy SKILL.md
  if [[ -f "$skill_dir/SKILL.md" ]]; then
    cp "$skill_dir/SKILL.md" "$target_dir/SKILL.md"
    echo "  ✅ $skill_name"
  fi

  # Copy any extra files (templates, examples, scripts)
  for extra in template.md examples scripts; do
    if [[ -e "$skill_dir/$extra" ]]; then
      cp -R "$skill_dir/$extra" "$target_dir/"
    fi
  done
done

# ─── Package Agents ───

echo "📦 Packaging agent definitions..."

for agent_file in "${AGENT_FILES[@]}"; do
  src="$ROOT/agents/$agent_file"
  if [[ -f "$src" ]]; then
    cp "$src" "$OUTPUT_DIR/agents/"
    echo "  ✅ $agent_file"
  else
    echo "  ⚠️  Agent not found: $agent_file (skipping)"
  fi
done

# ─── Package Commands ───

echo "📦 Packaging commands..."

for cmd_file in generate-requirement.md generate-ui-draft.md fullchain.md; do
  src="$ROOT/commands/$cmd_file"
  if [[ -f "$src" ]]; then
    cp "$src" "$OUTPUT_DIR/commands/"
    echo "  ✅ $cmd_file"
  else
    echo "  ⚠️  Command not found: $cmd_file (skipping)"
  fi
done

# ─── Generate manifest.json ───

echo "📝 Generating manifest.json..."

cat > "$OUTPUT_DIR/manifest.json" <<'MANIFEST'
{
  "name": "pm-team-toolkit",
  "version": "1.0.0",
  "description": "PM Team MCP Toolkit — AI-powered skills, agent roles, and workflow commands for product management teams using CodeBuddy.",
  "author": "PM Team",
  "skills": [
    {
      "name": "product-knowledge-base",
      "path": "skills/product-knowledge-base/SKILL.md",
      "description": "Teach PMs how to organize and query a product knowledge base for optimal AI-assisted output.",
      "type": "component"
    },
    {
      "name": "requirement-generator",
      "path": "skills/requirement-generator/SKILL.md",
      "description": "Generate structured PRD requirement documents from natural language descriptions with knowledge context.",
      "type": "workflow"
    },
    {
      "name": "ui-draft-generator",
      "path": "skills/ui-draft-generator/SKILL.md",
      "description": "Generate React + Arco Design UI draft code from requirement descriptions.",
      "type": "workflow"
    },
    {
      "name": "product-sync-agent",
      "path": "skills/product-sync-agent/SKILL.md",
      "description": "Guide PMs in synchronizing product progress and detecting team conflicts via MCP.",
      "type": "interactive"
    },
    {
      "name": "fullchain-efficiency",
      "path": "skills/fullchain-efficiency/SKILL.md",
      "description": "End-to-end workflow from requirement input to UI draft output with knowledge context and team sync.",
      "type": "workflow"
    }
  ],
  "agents": [
    "agents/product-manager.md",
    "agents/ui-designer.md",
    "agents/ux-architect.md",
    "agents/sprint-prioritizer.md",
    "agents/feedback-synthesizer.md",
    "agents/agents-orchestrator.md"
  ],
  "commands": [
    "commands/generate-requirement.md",
    "commands/generate-ui-draft.md",
    "commands/fullchain.md"
  ],
  "mcp_server": {
    "name": "pm-team-hub",
    "description": "Remote MCP Server for shared product data — knowledge base, requirements, progress, templates.",
    "config_example": {
      "mcpServers": {
        "pm-team-hub": {
          "url": "http://your-server:8000/mcp",
          "description": "PM团队共享数据中心"
        }
      }
    }
  }
}
MANIFEST

# ─── Create ZIPs (optional) ───

if [[ "$CREATE_ZIP" == true ]]; then
  echo "🗜️  Creating ZIP archives..."
  ZIP_DIR="$ROOT/dist/codebuddy-zips"
  mkdir -p "$ZIP_DIR"

  for skill_name in "${PM_TOOLKIT_SKILLS[@]}"; do
    skill_dir="$OUTPUT_DIR/skills/$skill_name"
    if [[ -d "$skill_dir" ]]; then
      (cd "$OUTPUT_DIR/skills" && zip -qr "$ZIP_DIR/$skill_name.zip" "$skill_name")
      echo "  📦 $skill_name.zip"
    fi
  done

  # Full toolkit zip
  (cd "$OUTPUT_DIR" && zip -qr "$ZIP_DIR/pm-team-toolkit.zip" .)
  echo "  📦 pm-team-toolkit.zip (full package)"
  echo "ZIPs created in: ${ZIP_DIR#$ROOT/}"
fi

# ─── Summary ───

skill_count=$(find "$OUTPUT_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(find "$OUTPUT_DIR/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
cmd_count=$(find "$OUTPUT_DIR/commands" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "✅ PM Team Toolkit packaged successfully!"
echo "   Skills:   $skill_count"
echo "   Agents:   $agent_count"
echo "   Commands: $cmd_count"
echo "   Output:   ${OUTPUT_DIR#$ROOT/}"
