# Install Commands

## Table of Contents

- [Auxiliary Skills](#auxiliary-skills)
- [Figma MCP (only if user requests Figma)](#figma-mcp-only-if-user-requests-figma)
- [Browser Preview (plugin-standard)](#browser-preview-plugin-standard)

Tools, skills, and MCPs that ux-flows can propose to the user.

## Auxiliary Skills

| Skill | Purpose | Phase | Install Command |
|-------|---------|-------|-----------------|
| ui-ux-pro-max | Downstream: visual design | After | `npx skills find ui-ux-pro-max` |
| product-manager-toolkit | Upstream: PRD | Before | `npx skills find product-manager-toolkit` |
| brainstorming | Ideation if no PRD | Before | `npx skills find brainstorming` |

## Figma MCP (only if user requests Figma)

| MCP | Purpose | Install Command |
|-----|---------|-----------------|
| Figma Dev Mode MCP Server | Code to Canvas — bidirectional Figma integration | Enable in Figma desktop preferences, then: `claude mcp add --transport sse figma-dev-mode-mcp-server http://localhost:3845/sse` |

## Browser Preview (plugin-standard)

This plugin uses `dev-browser` (via the plugin-standard wrapper) for any interactive browser work — wireframe preview, live inspection, screenshots. Chrome DevTools MCP is NOT used by this plugin.

| Tool | Purpose | Install Command |
|-----|---------|-----------------|
| `dev-browser` CLI | Browser automation for wireframe preview (wrapped by `bin/amw-dev-browser-wrapper.sh`) | `/amw-init` (plugin-managed install) or manually: run `npm install -g dev-browser`, then `dev-browser install` |
| `bin/amw-dev-browser-wrapper.sh` | Plugin-standard wrapper enforcing viewport/UA/output conventions | Bundled with the plugin — no install step |

Wireframe preview invocation from this skill:

```bash
# Desktop preview (1440×900 default)
bin/amw-dev-browser-wrapper.sh shot file://$(pwd)/docs/ux-flows/wireframes/{entry-screen}.html

# Mobile preview (375×812) — matches the 375px wireframe target
bin/amw-dev-browser-wrapper.sh mobile file://$(pwd)/docs/ux-flows/wireframes/{entry-screen}.html

# Interactive session (user clicks through the prototype manually)
bin/amw-dev-browser-wrapper.sh open file://$(pwd)/docs/ux-flows/wireframes/{entry-screen}.html
```
