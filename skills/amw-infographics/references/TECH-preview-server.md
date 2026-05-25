---
name: TECH-preview-server
category: infographic-builder
source: image-generation/create-infographics/scripts/preview_server.py
also-in: image-generation/create-infographics/SKILL.md
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Start the server](#start-the-server)
- [User instruction](#user-instruction)
- [How auto-refresh works](#how-auto-refresh-works)
- [Workflow during iteration](#workflow-during-iteration)
- [Preview file structure](#preview-file-structure)
- [Full design fidelity in preview](#full-design-fidelity-in-preview)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Preview server — live reload during builder sessions

## What it does

Lightweight HTTP server on port 7783 that serves
`.infographic/.preview.html` and auto-refreshes the browser tab
whenever the file changes. Used by Interactive Builder mode for
live component preview.

## When to use

- Mode A (Interactive Builder) — mandatory.
- Anytime you want a live-reloading HTML preview during iteration.

## Start the server

```bash
# source: image-generation/create-infographics/SKILL.md
python scripts/preview_server.py &
```

One-liner to start only if not running:

<!-- cpv-fp SSRF_PATTERN: the localhost URL below is a liveness probe for a local dev preview server (documented example), not a server-side request forgery. -->

```bash
curl -s http://localhost:7783/__mtime__ > /dev/null 2>&1 \
  || python scripts/preview_server.py &
```

The `__mtime__` endpoint is the liveness probe — fast way to check
if the server's up.

## User instruction

Tell the user ONCE:
> "Preview server running at http://localhost:7783 — open it in
> your browser. It auto-refreshes on every render."

Don't repeat this message on subsequent components.

## How auto-refresh works

The browser polls `/__mtime__` every ~500ms. When the mtime of
`.preview.html` changes, the browser reloads the page.

## Workflow during iteration

1. Claude writes `.infographic/.preview.html` (full HTML doc).
2. Browser auto-refreshes, user sees the component.
3. User says "looks good" or requests changes.
4. If changes: Claude re-writes `.preview.html`. Browser refreshes.
5. Repeat until user approves.
6. Approved HTML is saved to state.components[].html.

## Preview file structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Component Label} — Preview</title>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0D0D0D;
      display: flex; align-items: center; justify-content: center;
      min-height: 100vh; padding: 48px;
    }
    .component-wrapper { width: 100%; max-width: 900px; }
    :root {
      --bg: #0D0D0D;
      --primary: #E99A00;
      --secondary: #E8943A;
      --text: #FFFFFF;
      --muted: #8B8B8B;
      --border: rgba(255,255,255,0.1);
    }
    /* Component CSS inline */
  </style>
</head>
<body>
  <div class="component-wrapper">
    <!-- Component HTML — full design fidelity -->
  </div>
</body>
</html>
```

## Full design fidelity in preview

Preview components use **full design fidelity** — gradients, box-
shadows, glows, all of it. This is a real browser tab, not a
sandbox. Nothing is restricted.

## Gotchas

- Port 7783 must be free. If taken, the server fails silently.
- `.preview.html` must be a complete HTML document, not a fragment.
- The state file (`project.json`) is NOT served — only
  `.preview.html`.

## Cross-references

- [TECH-interactive-builder-mode](TECH-interactive-builder-mode.md) — the mode this enables.
  > What it does · When to use · The flow · State file — `.infographic/{project}.json` · Preview server · The approval gate (A4) · State schema per component · Why verbatim HTML · Session resume · Gotchas · Cross-references
- [TECH-preview-animations](TECH-preview-animations.md) — browser-only entrance animations.
  > What it does · When to use · Per-component animation table · Stat counter — JS · Bar chart — CSS transition · Feature card stagger — CSS · SVG line draw · The export capture · Gotchas · Cross-references
- [TECH-export-pipeline](TECH-export-pipeline.md) — where finalized HTML goes.
  > What it does · When to use · Install · Basic invocation · With local server (recommended) · Width and scale · Per-platform widths · Wait-for-render helper · SVG export · Gotchas · Cross-references
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
