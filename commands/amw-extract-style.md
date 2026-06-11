---
name: amw-extract-style
description: "Shortcut for users who want to extract design tokens from a specific live URL directly — chains dev-browser + design-extract to satisfy design-principles Rule 1 context-gathering. An agent in Main-agent mode may also invoke skills/amw-dev-browser/ and skills/amw-design-extract/ directly via the orchestrator during Phase A or Phase B, applying token-mapping techniques beyond what this command covers."
---

# /amw-extract-style

Pipe a live URL through `dev-browser` (for the page render / DOM / screenshot) and `design-extract` (for token extraction via `designlang`) so design-principles has concrete context to work from. This satisfies Rule 1 of design-principles (gather context before designing) when the user wants to match or reference an existing site.

## Arguments

`$ARGUMENTS` should contain a single URL. If the arg is missing or not a valid URL, ask: *"Which URL should I extract the style from?"* and stop.

## Action

### 1. Prerequisite check

Run `/amw-doctor` quickly (or inline the dev-browser and designlang checks). If either is missing, stop and point the user at `/amw-init`.

### 2. Capture the page with dev-browser

Use the `dev-browser` CLI (via [SKILL](../skills/amw-dev-browser/SKILL.md)) to:

- Open the URL with a realistic desktop viewport (1440×900).
- Wait for `networkidle` or a 3-second settle, whichever is shorter.
- Capture a full-page screenshot to a temp path like `/tmp/amw-extract-<slug>-full.png`.
- Capture above-the-fold screenshot to `/tmp/amw-extract-<slug>-hero.png`.
- Dump the DOM + computed styles for the top 3 heading tags, primary buttons, and body text to `/tmp/amw-extract-<slug>-dom.json`.

Prefer `bin/amw-dev-browser-wrapper.sh` for the exact invocation once Phase B2 lands; until then, use the underlying `dev-browser` CLI directly.

### 3. Extract tokens with design-extract

Invoke the `design-extract` skill (which wraps `npx designlang <url>`):

- Run `npx designlang <url>` with default output mode `multi` (emits markdown, HTML preview, Tailwind config, React theme, shadcn theme, Figma variables, W3C tokens, CSS vars).
- Save outputs under `/tmp/amw-extract-<slug>-tokens/`.

If design-extract is missing, fall back to the dev-browser computed-style dump only and note the degraded mode in the report.

### 4. Produce the report

Write one markdown file the user can read directly: `/tmp/amw-extract-<slug>-report.md`. Include:

**Source**
- URL, capture timestamp, viewport size, dev-browser and designlang versions.

**Visual summary**
- Embedded hero screenshot.
- Dominant colors extracted (with oklch conversions — design-principles prefers oklch over hex).
- Font families detected (with fallback stacks).
- Spacing scale inferred (likely 4pt / 8pt grid).
- Border radius scale, shadow library if any.

**Token drops (copy-paste ready)**
- CSS custom properties block.
- Tailwind v4 `@theme` block.
- A `:root { ... }` oklch palette matching design-principles' [color-system](../skills/amw-design-principles/color-system.md) structure (surface-0..2, text-1..3, border, primary, success/warning/danger).
> [color-system.md] I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list

**Compliance checks**
- Body vs background contrast: pass/fail against WCAG AA (4.5:1).
- Font stack includes a non-generic display face? (if all Inter / Roboto / Arial, flag as AI-slop-adjacent per ai-slop-avoid item 7).
- Palette within 7 colors? (per ai-slop-avoid item 24).

**Integration hints**
- Which starter-component from `skills/amw-design-principles/starter-components/` fits best (browser-window / ios-frame / deck-stage / design-canvas).
- Whether the site uses Tailwind (flag for `skills/amw-tailwind-4/`), shadcn (flag for `skills/amw-shadcn-ui/`), or custom CSS.

### 5. Hand back to design-principles

After producing the report, prompt the user: *"Tokens captured. Ready to design against them? I recommend `/amw-sketch <intent>` next — it will propose 3 layout variants that respect these tokens."*

If they say yes, proceed via `design-principles` with the extracted tokens as the context input for Rule 1.

## Non-negotiables

- **dev-browser is the only interactive browser automation.** Do not open the page with Playwright directly, Chrome DevTools MCP, or puppeteer. The rendering backend in `bin/amw-html-export.py` is not a substitute — it is for output HTML→PNG, not for loading arbitrary URLs.
- **Respect robots.txt and the site's terms of service.** If the URL returns a `X-Robots-Tag: noindex` or the site's robots.txt disallows scraping, warn the user and stop.
- **Do not persist tokens inside the plugin repo.** All outputs go under `/tmp/` unless the user explicitly asks to save to a project directory.
- **Never bypass login walls.** If the URL redirects to a login page, stop and ask the user to supply a public URL.

## Failure modes

- `dev-browser` times out → retry once with a longer wait; if still failing, report and stop.
- `designlang` fails on a single-page app → fall back to screenshot-only mode and note it in the report.
- Page uses only system-ui fonts → note in the report; recommend the user supply their own font choice.
