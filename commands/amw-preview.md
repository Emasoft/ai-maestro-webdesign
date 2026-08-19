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

### 3b. Push the preview into the AI Maestro dashboard side panel (when available)

If `bin/amw-panel-preview.sh` reports the AI Maestro panel CLI is available (exit 0 on
`status`), also push the live preview to the human's web browser panel so they see it
without leaving the dashboard:

- Self-contained HTML → `bin/amw-panel-preview.sh show --html-file <path>`
- Served via the local preview server → `bin/amw-panel-preview.sh show --url <http-url>`
- After each subsequent edit iteration → `bin/amw-panel-preview.sh refresh`
- Drain click feedback the human generated inside the panel with
  `bin/amw-panel-preview.sh feedback` and fold it into the report.

The panel is a LIVE surface, not a queue: a response with `"delivered": 0` means no
dashboard had the panel open and the push was DROPPED — say so in the report instead of
claiming the preview was shown. Outside an AI Maestro environment (exit 3) skip this
step silently; dev-browser screenshots remain the canonical verification path.

### 4. Self-check against design-principles

Load [ai-slop-avoid](../skills/amw-design-principles/ai-slop-avoid.md) in lightweight mode (scan for matches, don't reload the whole file into main context). Check the rendered page for the most common slop signals:
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

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
