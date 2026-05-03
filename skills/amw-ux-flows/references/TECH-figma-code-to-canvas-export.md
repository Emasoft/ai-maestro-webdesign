---
name: TECH-figma-code-to-canvas-export
category: ux-flow-wireframe
source: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/SKILL.md
also-in: SKILLS-TO-INTEGRATE/diagrams-skills/ux-flow-designer-main/references/figma-integration.md
---

# TECH-figma-code-to-canvas-export

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Prerequisites (MUST be mentioned before any Figma operation)](#prerequisites-must-be-mentioned-before-any-figma-operation)
  - [Protocol](#protocol)
  - [Export workflow (once prerequisites are confirmed)](#export-workflow-once-prerequisites-are-confirmed)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


## What it does

Exports the clickable HTML wireframes to Figma as editable frames using
Figma's official **Code to Canvas** integration via the Dev Mode MCP
Server. The export is **opt-in** — the skill never attempts it silently;
it is mentioned at the end of Phase 4 as an optional next step, and the
user must confirm the prerequisites before any Figma operation runs.

## When to use

- **After Phase 4 handoff is complete** — only as an explicit optional
  next step mentioned to the user.
- **Whenever the user says "export to Figma"** or equivalent phrasing.
- **Never silently** — always inform the prerequisites first.

Do not fire on generic "make it look nice in Figma" intent — that
belongs to downstream visual design (`ui-ux-pro-max` or similar), not
this skill.

## How it works

### Prerequisites (MUST be mentioned before any Figma operation)

1. **Figma desktop app** installed and running.
2. **Dev Mode MCP Server** enabled in Figma desktop
   (Preferences → "Enable Dev Mode MCP Server").
3. **MCP added to Claude Code**:
   ```
   claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse
   ```
4. **Chrome DevTools MCP** already installed (used for wireframe preview
   in Phase 3).

### Protocol

1. **Inform the requirements FIRST** before attempting anything:
   > "Figma export requires:
   > - Figma desktop with Dev Mode MCP Server enabled
   > - MCP added via `claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse`
   > - Chrome DevTools MCP already installed
   > Please confirm these are set up before I proceed."
2. **Wait for user confirmation.** Do not read
   `references/figma-integration.md` or check MCP availability until
   the user confirms.
3. **Once confirmed**, read `references/figma-integration.md` for the
   detailed steps.

### Export workflow (once prerequisites are confirmed)

1. **Verify toolchain** — check Dev Mode MCP is responding at
   `http://127.0.0.1:3845/sse`, check Chrome DevTools MCP is
   available.
2. **Open each wireframe in the browser** via Chrome DevTools MCP or
   `open` (already mobile-first 375px from Phase 3).
3. **"Send this to Figma"** via the Dev Mode MCP for each open
   wireframe. Each screen becomes an editable Figma frame.
4. **Organize frames in Figma:**
   - Group by use case flow
   - Add flow connections between screens
   - Name frames matching the screen inventory from
     `docs/ux-flows/wireframes/INDEX.md`
5. **Apply design tokens** (if a design system exists):
   - Read existing design tokens via the MCP
   - Map wireframe elements to design tokens
   - Apply colors, typography, spacing

## Minimal example

User invocation:

```
User: "Export the wireframes to Figma"
Agent: "Figma export via the Code to Canvas integration requires:
  1. Figma desktop app with Dev Mode MCP Server enabled
     (Preferences → Enable Dev Mode MCP Server)
  2. MCP added to Claude Code:
     claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse
  3. Chrome DevTools MCP installed (already used for wireframe preview)
Please confirm these are set up, or ask for setup guidance."

User: "Confirmed, let's go"
Agent: [reads references/figma-integration.md, runs the export workflow]
```

## Gotchas

- **Never silently attempt Figma operations.** The hard rule: always
  present the requirements first. Silent attempts waste time when the
  MCP isn't running and confuse users when it suddenly "works".
- **Only official Code to Canvas.** Third-party HTML-to-Figma tools
  exist but have different semantics; this skill specifically uses
  Figma's official path.
- **Bidirectional once connected.** Code → Figma AND Figma → Code. The
  user can edit in Figma and the edits round-trip to the HTML if they
  want; most people use it one-way initially.
- **Frame naming matches screen inventory.** Pull names from
  `docs/ux-flows/wireframes/INDEX.md`. Random Figma frame names
  ("Frame 1", "Frame 2") break the traceability that the clickable
  prototype established.
- **Design tokens are optional.** If the user has an existing token
  system in Figma, the export can apply tokens automatically. If not,
  the frames land with the wireframe grayscale styling — which is
  fine for flow validation.

## Cross-references

- [SKILL](../SKILL.md) — Figma export section at the end of the workflow
- [figma-integration](figma-integration.md) — the detailed steps (loaded only after user
  > Code to Canvas · Export Workflow
  confirmation)
- [install-commands](install-commands.md) — MCP install commands
  > Auxiliary Skills · Figma MCP (only if user requests Figma) · Browser Preview (plugin-standard)
- [TECH-wireframe-html-mobile-first](TECH-wireframe-html-mobile-first.md) — the wireframes being exported
  > What it does · When to use · How it works · Scaffold · Aesthetic tokens · Utility classes · Minimal example · Gotchas · Cross-references
- [TECH-wireframe-index-inventory](TECH-wireframe-index-inventory.md) — source of frame names
  > What it does · When to use · How it works · Minimal example · Gotchas · Validation pass · Cross-references
