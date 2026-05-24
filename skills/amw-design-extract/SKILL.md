---
name: amw-design-extract
description: Extract a design system (colors, fonts, spacing, shadows, tokens) from a live URL using the `designlang` CLI. Triggers on "extract design tokens", "copy the style of", "get colors and fonts from URL", "reverse-engineer design system", "generate tailwind config from site". Does NOT trigger on generic "design", "style my page" — those route to design-principles. Use when extracting a design system from a live URL. Trigger with /amw-extract-style.
version: 0.1.0
---

# Design Extract

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. Triggers are URL-extraction-specific only.

## Overview

Extracts a design system (colors, fonts, spacing, shadows, tokens) from a live URL using the `designlang` CLI. Outputs multi-format token dumps (Tailwind config, shadcn theme, React tokens, Figma tokens, CSS variables, W3C tokens).

## Activation

Callable directly via the `/amw-extract-style` command (user shortcut — fast path to extract tokens from a specific URL). Also invoked by the `design-principles` orchestrator during Phase A context-gathering (Rule 1) or at the start of Phase B in Main-agent mode. In Main-agent mode the orchestrator may apply token-mapping and design-system reconstruction techniques from this skill beyond what the `/amw-extract-style` command exposes.

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

INPUT. Provides concrete design tokens from a live reference URL, feeding design-principles Rule 1 (gather context). The extracted report feeds into the color / typography / spacing references so downstream HTML uses real tokens, not guesses.

For a structured, machine-parseable token spec (canonical DESIGN.md), prefer the **`amw-design-md`** skill — it runs lint + WCAG-AA contrast checks. This skill is the looser-format URL extractor (designlang multi-format dump: Tailwind / shadcn / React / Figma / CSS-vars / W3C / preview HTML); the two are siblings, not duplicates.

## Trigger conditions
Fires on these specific phrasings:

- "extract design tokens from <url>"
- "copy the style of <url>"
- "get colors and fonts from <url>"
- "reverse-engineer <url>'s design system"
- "generate tailwind config from <url>"
- "clone the visual design of <url>"
- "pull CSS variables from <url>"
- "scrape the palette from <url>"

Do NOT fire on: "design a landing page", "style my page", "build the UI", "make it look clean". Those are design-principles' vocabulary — the orchestrator decides when to call this skill.

## Prerequisites

- **runtime_binaries (system):** `node ≥ 22`, `npx`
- **runtime_binaries (via /amw-init):** `designlang` (npm package, lazy-installed by `npx` on first call; its internal Playwright browser is fetched by designlang itself, not by this plugin)
- **Optional upstream:** `../amw-dev-browser/` — pairs with this skill when a screenshot + DOM capture is needed alongside token extraction (combined via `/amw-extract-style`)

## Instructions

1. Invoke `bin/amw-designlang-wrapper.sh` with one of four subcommands: `tokens`, `colors`, `fonts`, or `css` plus the target URL.
2. For a full token dump (`tokens` subcommand), the wrapper emits eight files per URL (W3C tokens, Tailwind theme, shadcn theme, React theme, Figma variables, CSS vars, preview HTML, and report).
3. Locate the output directory printed to stdout (default `$TMPDIR/ai-maestro-webdesign-tokens/<slug>/`), or override with `DL_OUT_DIR`.
4. Pass the relevant output files (e.g. `css-vars.css`, `tailwind.theme.css`) to downstream skills (`ascii-to-html`, `svg-creator`, `tailwind-4`).
5. For combined screenshot + token extraction, use `/amw-extract-style <url>` which pairs this skill with `../amw-dev-browser/`.
6. Document the token source and output paths in the job-completion report.

## Usage

The canonical entry point is `bin/amw-designlang-wrapper.sh`. Do not call `npx designlang` directly — the wrapper normalizes output paths.

Four subcommands: `tokens` (full multi-format dump), `colors` (JSON palette to stdout), `fonts` (JSON typography to stdout), `css` (`:root { --* }` file). Examples:

```bash
bin/amw-designlang-wrapper.sh tokens https://stripe.com
bin/amw-designlang-wrapper.sh colors https://stripe.com
bin/amw-designlang-wrapper.sh fonts https://stripe.com
bin/amw-designlang-wrapper.sh css https://stripe.com [out.css]
```

Override the output base with `DL_OUT_DIR=/some/path bin/amw-designlang-wrapper.sh tokens <url>`.

A full `tokens` run emits eight files per URL: `report.md`, `tokens.w3c.json` (W3C tokens), `tailwind.theme.css`, `shadcn.theme.css`, `react.theme.ts`, `figma.variables.json`, `css-vars.css`, `preview.html`.

User-facing command `/amw-extract-style <url>` combines this skill with `../amw-dev-browser/` so the user gets a rendered screenshot alongside the token dump.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- `../../bin/amw-designlang-wrapper.sh` — plugin-standard wrapper (the only valid invocation path)
- [SKILL](../amw-dev-browser/SKILL.md) — pairs for screenshot + DOM + style capture
- `/amw-extract-style` — user-facing command combining both
- [color-system](../amw-design-principles/color-system.md) — extracted palette maps to oklch structure
  > I. Always prefer oklch over rgb / hex / hsl · II. WCAG contrast — hard requirement · III. Palette structure (cap at 5–7 colors) · IV. Dark mode is not a simple inversion · V. Color temperature · VI. Palette inspiration libraries (use these instead of inventing) · VII. Self-check list
- [typography-system](../amw-design-principles/typography-system.md) — extracted font stack maps to type rules
  > I. Modular type scale · II. Font-weight hierarchy (only 2–3 levels) · III. Line-height · IV. Letter-spacing · V. Font-pairing rules · VI. Recommended font stacks (avoiding AI slop) · VII. Fallback-stack syntax
- [spacing-rhythm](../amw-design-principles/spacing-rhythm.md) — extracted spacing scale maps to rhythm rules
  > I. 8pt grid system · II. Fibonacci spacing rhythm (large-scale) · III. Vertical rhythm (baseline grid) · IV. Hit targets (tappable areas) · V. Alignment · VI. Three principles of whitespace · VII. Border radius · VIII. Shadow system · IX. Self-check
- [SKILL](../amw-ascii-to-html/SKILL.md) — consumes `css-vars.css` for HTML rendering

## Non-negotiables

- **Do not bypass `bin/amw-designlang-wrapper.sh`.** It pins output paths so other skills can locate the artifacts; calling `npx designlang` directly defeats that.
- **Do not cache tokens inside the plugin repo.** Output goes to `$TMPDIR/ai-maestro-webdesign-tokens/<slug>/` or `$DL_OUT_DIR` — never inside `skills/` or `bin/`.
- **Respect robots.txt and login walls.** If the target URL requires auth or forbids crawling, warn the user and stop. Do not pass `--cookie` or `--header` without explicit instruction.
- **One URL at a time by default.** Bulk brand comparisons go through designlang's `brands` subcommand via raw pass-through — not this wrapper's four standard subcommands.
- **Do not feed token output into design-principles without user review.** Extracted tokens are a proposal, not a spec — the orchestrator decides whether to adopt them.

## References

Every technique is documented as a single reference file under `./references/`. Read only the file whose TOC matches the current need.

- [TECH-designlang-basic-extraction](./references/TECH-designlang-basic-extraction.md) — Basic URL extraction (`designlang <url>`)
- [TECH-designlang-brands](./references/TECH-designlang-brands.md) — N-way brand comparison matrix
- [TECH-designlang-dark-mode](./references/TECH-designlang-dark-mode.md) — `--dark` extraction
- [TECH-designlang-diff](./references/TECH-designlang-diff.md) — pairwise brand comparison
- [TECH-designlang-full-mode](./references/TECH-designlang-full-mode.md) — `--full` everything-at-once
- [TECH-designlang-interactions](./references/TECH-designlang-interactions.md) — hover / focus / active state capture
- [TECH-designlang-responsive](./references/TECH-designlang-responsive.md) — `--responsive` breakpoint capture
- [TECH-designlang-score](./references/TECH-designlang-score.md) — `designlang score` design-quality scoring
- [TECH-designlang-screenshots](./references/TECH-designlang-screenshots.md) — `--screenshots` component capture

Each reference contains: What it does · When to use · How it works · Minimal example · Gotchas · Cross-references.

## Completion checklist

Verify every item before reporting complete. FAIL on any item should trigger a remediation loop.

- Inputs captured verbatim (no silent paraphrasing).
- At least one `TECH-*.md` from `references/` was consulted and cited.
- Output passes the skill's Non-negotiables section.
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
- Emitted HTML/SVG/ASCII validated via `bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`.
- Cross-skill hand-offs documented — name any consumed skill's SKILL.md + TECH file in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — `designlang/` output folders (tokens.json, palette.json, screenshots, report.html). Output path is determined by **project inference**, NOT hardcoded. See [project-output-routing](../amw-design-principles/references/project-output-routing.md) for the full detection rules (priority order: user-supplied path → framework convention → existing `./design/` folder → generic fallback → `/tmp/amw-design-extract-<slug>/` scratch).
   > When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
2. **Job-completion report** at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md` with sections: Inputs, Method, Artifacts (each `- <path> — <desc> — **How to use:** <tip> — **Next steps:** <followup>`), Checklist (PASS/FAIL/N/A), Deviations.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`. Every artifact MUST be linked from the report.

## Error Handling

- **`npx: command not found`** — Node.js is not installed. User must install node ≥ 22 (surfaced by `/amw-doctor`).
- **First call stalls for 30–90 s** — expected. `npx` is downloading `designlang` and its Playwright browser on first use. Subsequent calls are cached.
- **Blank report / missing colors** — single-page app that fetches styles client-side. Re-run with `DL_ARGS="--wait 3000"` (passed through to designlang) or use `dev-browser` to screenshot + inspect first.
- **Auth wall (401/403)** — the page required login. Stop and ask the user whether they want to pass a session cookie; do not proceed silently.
- **Oversized palette (500+ colors)** — utility-CSS site (e.g. Tailwind-powered demo). Re-run with `--depth 0 --no-history` via raw pass-through; consider `colors` subcommand for just the essentials.
- **`preview.html` opens blank** — browser blocked a local-file fetch. Serve the output directory with `bin/amw-preview-server.py` instead of double-clicking.
