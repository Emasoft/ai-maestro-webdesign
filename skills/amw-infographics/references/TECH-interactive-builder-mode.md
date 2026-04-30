---
name: TECH-interactive-builder-mode
category: infographic-builder
source: image-generation/create-infographics/SKILL.md
also-in:
---

# Interactive Builder (Mode A) — component-by-component iteration

## What it does

A session mode where Claude writes each component as a full self-
contained HTML file to `.infographic/.preview.html`, a preview server
auto-refreshes the user's browser tab, and the user approves each
component before it's written to state.

## When to use

- "Show me each component one by one"
- "Let me iterate"
- User wants browser preview with live refresh
- Exploratory briefs: "I'm not sure exactly what I want"

## The flow

```
A1. Session Start — check for existing state, start preview server
A2. Plan — state the layout intent + component list
A3. Render — write .preview.html for current component
A4. Approval — user says "approve" or requests changes
A5. State persistence — locked components saved as verbatim HTML
A6. Assembly — combine approved components into final HTML
```

## State file — `.infographic/{project}.json`

```json
{
  "version": "1.0",
  "project": "project-name",
  "created": "ISO-8601",
  "updated": "ISO-8601",
  "brief": {
    "brand_color": "#E99A00",
    "aesthetic": "Bold/Cyber",
    "platform": "website",
    "top_insight": "The one number or idea viewers must remember"
  },
  "metadata": {
    "platform": "website",
    "palette_name": "AMBER DARK",
    "bg": "#0D0D0D",
    "primary": "#E99A00",
    "secondary": "#E8943A",
    "font_display": "Bebas Neue",
    "font_body": "Montserrat"
  },
  "plan": [],
  "components": []
}
```

## Preview server

```bash
# source: image-generation/create-infographics/SKILL.md
curl -s http://localhost:7783/__mtime__ > /dev/null 2>&1 \
  || python scripts/preview_server.py &
```

Tell the user once: *"Preview server running at http://localhost:7783.
Open it. Auto-refreshes on every render."*

## The approval gate (A4)

| User says | Action |
|-----------|--------|
| approve / looks good / next / ✓ / yes | Save HTML to state, move on |
| Any correction | Re-write `.preview.html` only — don't touch state |
| skip | Mark `status: "skipped"` |
| start over | Mark `status: "rejected"`, redo from scratch |
| assemble / finalize / done | Trigger assembly (A6) |

**Never write a component to state until the user explicitly
approves.** Revision cycles happen in the browser.

## State schema per component

```json
{
  "id": "bar-chart-hours",
  "type": "bar_chart",
  "label": "Weekly hours worked",
  "status": "approved",
  "approved_at": "ISO-8601",
  "html": "<!-- verbatim full body content of approved preview -->"
}
```

## Why verbatim HTML

On assembly, the approved component's HTML is placed **exactly** as
the user approved it — no regeneration, no modification. Preserves
the approved state byte-for-byte.

## Session resume

When returning to an existing project:
1. Load the state file
2. Report what's approved
3. Continue from where the plan left off

## Gotchas

- Don't write to state during revision — only on explicit approval.
- Preview server runs on port 7783 — make sure it's free.
- State file lives at `{cwd}/.infographic/{project_name}.json` —
  gitignored per project convention.

## Cross-references

- `TECH-one-shot-mode.md` — the alternative pipeline (generate in
  one pass).
- `TECH-guided-creative-mode.md` — a middle ground (two-option UX).
- `TECH-template-registry.md` — the assembled HTML starting points.
- `TECH-preview-server.md` — the server implementation.
- [`../SKILL.md`](../SKILL.md) — parent skill

