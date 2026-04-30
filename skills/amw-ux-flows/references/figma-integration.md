# Figma Integration

Only load this file when user explicitly requests Figma export.

## Table of Contents

- [Code to Canvas](#code-to-canvas)
- [Export Workflow](#export-workflow)

---

## Code to Canvas

Figma's official **Code to Canvas** integration captures rendered UI from the browser and converts it into editable Figma frames.

### Requirements

| Requirement | Detail |
|-------------|--------|
| Figma desktop app | Must be installed and running |
| Dev Mode MCP Server | Enabled in Figma desktop preferences |
| `dev-browser` CLI | For opening wireframes in the browser (plugin-standard, wrapped by `bin/amw-dev-browser-wrapper.sh`) |

### Setup (2 steps)

1. **Enable Dev Mode MCP Server** in Figma desktop:
   - Open Figma desktop → Preferences → Enable "Dev Mode MCP Server"
2. **Add the MCP to Claude Code**:
   ```
   claude mcp add --transport sse figma-dev-mode-mcp-server http://127.0.0.1:3845/sse
   ```

### Capabilities

- **Bidirectional**: Code → Figma and Figma → Code
- **Semantic reading**: Understands components, variables, styles, and layout structure
- **Browser capture**: Converts rendered HTML directly into editable Figma frames
- **Official support**: Maintained by Figma

---

## Export Workflow

### Prerequisites

1. Figma desktop app with Dev Mode MCP Server enabled
2. `dev-browser` CLI installed via `/amw-init` (same tool used for wireframe preview in Phase 3)
3. Connection verified: Dev Mode MCP Server responding on `http://127.0.0.1:3845/sse`

### Steps

1. **Verify toolchain**
   - Check Dev Mode MCP Server is active in Figma desktop
   - Check `dev-browser` CLI is on PATH (`command -v dev-browser`)
   - Offer install commands for any missing tool (see `references/install-commands.md`)

2. **Open wireframes in browser**
   - Use `bin/amw-dev-browser-wrapper.sh open file://$(pwd)/docs/ux-flows/wireframes/<screen>.html` (or `mobile` for 375px) to load each wireframe
   - Wireframes are already mobile-first (375px) from Phase 3
   - For bulk capture, iterate over each screen in `docs/ux-flows/wireframes/INDEX.md`

3. **Send to Figma**
   - For each wireframe open in the browser, use "Send this to Figma" via the Dev Mode MCP
   - Each screen becomes an editable Figma frame

4. **Organize in Figma**
   - Group frames by use case flow
   - Add flow connections between screens
   - Name all frames matching the screen inventory from `docs/ux-flows/wireframes/INDEX.md`

5. **Apply design tokens** (if design system exists)
   - Read existing design tokens via the MCP
   - Map wireframe elements to design tokens
   - Apply colors, typography, spacing
