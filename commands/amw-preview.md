---
name: amw-preview
description: "Shortcut for users who want to preview a specific local HTML file in dev-browser with a design-principles self-check directly. An agent in Main-agent mode may also invoke skills/amw-dev-browser/ directly via the orchestrator as part of Phase B scenario testing, capturing screenshots and running broader checks than this command covers."
---

# /amw-preview

Open the HTML file referenced by `$ARGUMENTS` (or the most recently edited `.html` in the current working directory if `$ARGUMENTS` is empty) in `dev-browser`, screenshot it at desktop and mobile widths, and run a brief design-principles self-check against the render.

## Arguments

- Optional: a file path to a local `.html`. Absolute, or relative to the project root.
- If absent, find the latest-modified `.html` under the user's working directory (excluding `node_modules/`, `.next/`, `dist/`, `build/`, `external/`). If multiple, ask the user which one.

## Action

### 1. Prerequisite check

Quick check: `dev-browser --version` must succeed. If not, stop and point at `/amw-init`.

### 2. Serve the file

- If the HTML references relative assets (images, CSS, JS), start a local HTTP server from the file's parent directory via `bin/amw-preview-server.py --port 7883 --root <dir>` (once Phase B1 lands; until then, use `python3 -m http.server 7883` in that directory as a placeholder).
- If the HTML is self-contained (no external asset refs), skip the server and open the file:// URL directly.

### 3. Capture two screenshots

Call `dev-browser` twice:

- Desktop: viewport 1440×900, full-page screenshot → `/tmp/amw-preview-<slug>-desktop.png`.
- Mobile: viewport 375×812, full-page screenshot → `/tmp/amw-preview-<slug>-mobile.png`.

Also capture console logs and any network failures → `/tmp/amw-preview-<slug>-console.txt`.

### 4. Self-check against design-principles

Load [ai-slop-avoid](skills/amw-design-principles/ai-slop-avoid.md) in lightweight mode (scan for matches, don't reload the whole file into main context). Check the rendered page for the most common slop signals:

- Body font detected — is it Inter / Roboto / Arial / system-ui (item 7)?
- Primary CTA present and ≥ 44×44px hit target (Fitts's Law / design-principles §Dimensional hard limits)?
- Any `border-radius + border-left: 4px accent` pattern (item 2)?
- Any large purple-blue or pink-orange linear-gradient background (item 1)?
- Count of distinct colors on the page ≤ 7 (item 24)?
- Body vs background contrast ≥ 4.5:1 at the dominant copy block (color-system.md §WCAG)?

Run these via DOM inspection through dev-browser — do not guess from the screenshot alone.

### 5. Produce a compact report

Write `/tmp/amw-preview-<slug>-report.md`:

```
# Preview: <filename>
- Desktop: /tmp/amw-preview-<slug>-desktop.png
- Mobile:  /tmp/amw-preview-<slug>-mobile.png
- Console: /tmp/amw-preview-<slug>-console.txt (0 errors, 0 warnings)

## Self-check against design-principles
- Body font: Suisse Int'l ✓ (non-slop face)
- Primary CTA: 48×48px ✓ (Fitts OK)
- Slop patterns: 0 matches
- Contrast: body 4.8:1 ✓ (AA)
- Palette size: 5 ✓

## Recommended next steps
- Nothing blocking — ship.
- OR: <list of issues>. Run /amw-eval for a deeper scoring.
```

Surface the report path + one-line verdict to the user. Do not dump the full report into chat.

## Non-negotiables

- **dev-browser only.** No Playwright-direct, no Puppeteer, no Chrome DevTools MCP.
- **No writes to the HTML file.** Preview is read-only on the user's source.
- **Temp outputs only.** All screenshots and reports go under `/tmp/` by default; honor an explicit `--out <dir>` if the user supplies one.
- **Never auto-fix issues found.** Report them; let the user decide whether to run `/amw-eval` or re-enter design-principles for rework.

## Failure modes

- File not found → list the candidate `.html` files found and ask the user to pick one.
- dev-browser fails to load the URL → retry once with a longer timeout; if still failing, dump console errors to the report and mark the run as degraded.
- HTML uses CDN assets blocked by offline network → note it in the report and suggest running again with network.
