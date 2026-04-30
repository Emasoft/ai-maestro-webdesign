---
name: amw-design-extract
description: Extract a design system (colors, fonts, spacing, shadows, tokens) from a live URL using the `designlang` CLI. Triggers on "extract design tokens", "copy the style of", "get colors and fonts from URL", "reverse-engineer design system", "generate tailwind config from site", "clone visual design". Do NOT trigger on generic "design", "style my page", "build the UI" — those are design-principles' territory.
version: 0.1.0
---

# Design Extract

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> This skill is an executor. Triggers are URL-extraction-specific only.

## Activation

Callable directly via the `/amw-extract-style` command (user shortcut — fast path to extract tokens from a specific URL). Also invoked by the `design-principles` orchestrator during Phase A context-gathering (Rule 1) or at the start of Phase B in Main-agent mode. In Main-agent mode the orchestrator may apply token-mapping and design-system reconstruction techniques from this skill beyond what the `/amw-extract-style` command exposes.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

INPUT. Provides concrete design tokens from a live reference URL, feeding design-principles Rule 1 (gather context). The extracted report feeds straight into `color-system.md`, `typography-system.md`, and `spacing-rhythm.md` so the downstream HTML step uses real tokens, not guesses.

When a structured, machine-parseable token specification is needed (the most common case for handing tokens to a Phase B agent or to an external coding agent), prefer the **`amw-design-md`** skill — it produces a Variant 1 DESIGN.md (the canonical `@google/design.md` format) directly from a URL via `bin/amw-design-md-from-url.sh`, and runs lint + WCAG-AA contrast checks. This skill (`amw-design-extract`) remains the looser-format URL extractor (designlang multi-format dump: Tailwind config, shadcn theme, React theme, Figma variables, CSS vars, W3C tokens, preview HTML); the two skills are siblings, not duplicates. Use `amw-design-md` when the user wants the canonical DESIGN.md format; use this skill when the user wants the multi-format token dump for direct integration into a build pipeline.

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

## Dependencies

- **runtime_binaries (system):** `node ≥ 22`, `npx`
- **runtime_binaries (via /amw-init):** `designlang` (npm package, lazy-installed by `npx` on first call; its internal Playwright browser is fetched by designlang itself, not by this plugin)
- **Optional upstream:** `../amw-dev-browser/` — pairs with this skill when a screenshot + DOM capture is needed alongside token extraction (combined via `/amw-extract-style`)

## Usage

The canonical entry point is `bin/amw-designlang-wrapper.sh`. Do not call `npx designlang` directly from other skills — the wrapper normalizes output paths so downstream skills can locate the emitted files without hard-coded paths.

Four subcommands:

```bash
# Full multi-format token dump (default). Writes an entire token set to
# $TMPDIR/ai-maestro-webdesign-tokens/<slug>/ and prints the directory path.
bin/amw-designlang-wrapper.sh tokens https://stripe.com

# JSON palette only — printed to stdout
bin/amw-designlang-wrapper.sh colors https://stripe.com

# JSON typography only — printed to stdout
bin/amw-designlang-wrapper.sh fonts https://stripe.com

# Plain `:root { --* }` CSS custom properties — file path printed to stdout
bin/amw-designlang-wrapper.sh css https://stripe.com [out.css]
```

Override the output base with `DL_OUT_DIR=/some/path bin/amw-designlang-wrapper.sh tokens <url>`.

A full `tokens` run emits eight files per URL:

| File | Format | Feeds |
|---|---|---|
| `report.md` | multi-section Markdown report (count varies by designlang version) | design-principles Rule 1 context |
| `tokens.w3c.json` | W3C Design Tokens | generic tooling, Style Dictionary |
| `tailwind.theme.css` | Tailwind v4 `@theme` block | tailwind-4 skill |
| `shadcn.theme.css` | shadcn/ui variables | shadcn-ui skill |
| `react.theme.ts` | React theme object | any JSX output |
| `figma.variables.json` | Figma Variables import | handoff to design team |
| `css-vars.css` | `:root { --* }` block | ascii-to-html, svg-creator |
| `preview.html` | Static palette/type preview | quick eyeballing |

For user-facing invocation, the command is `/amw-extract-style <url>`. That command combines this skill with `../amw-dev-browser/` so the user also gets a rendered screenshot alongside the token dump — one call, two inputs for design-principles.

## Cross-references

- `../../bin/amw-designlang-wrapper.sh` — plugin-standard wrapper (the only valid invocation path)
- `../amw-dev-browser/SKILL.md` — pairs with dev-browser for screenshot + DOM + style capture
- `/amw-extract-style` — user-facing command that combines both
- `../amw-design-principles/color-system.md` — extracted palette maps to this skill's oklch structure
- `../amw-design-principles/typography-system.md` — extracted font stack maps to this skill's type rules
- `../amw-design-principles/spacing-rhythm.md` — extracted spacing scale maps to this skill's rhythm rules
- `../amw-ascii-to-html/SKILL.md` — consumes `css-vars.css` when an ASCII wireframe is rendered to HTML

## Non-negotiables

- **Do not bypass `bin/amw-designlang-wrapper.sh`.** It pins output paths so other skills can locate the artifacts; calling `npx designlang` directly defeats that.
- **Do not cache tokens inside the plugin repo.** Output goes to `$TMPDIR/ai-maestro-webdesign-tokens/<slug>/` or `$DL_OUT_DIR` — never inside `skills/` or `bin/`.
- **Respect robots.txt and login walls.** If the target URL requires auth or forbids crawling, warn the user and stop. Do not pass `--cookie` or `--header` without explicit instruction.
- **One URL at a time by default.** Bulk brand comparisons go through designlang's `brands` subcommand via raw pass-through — not this wrapper's four standard subcommands.
- **Do not feed token output into design-principles without user review.** Extracted tokens are a proposal, not a spec — the orchestrator decides whether to adopt them.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `design-extract` is the user asking about?
  - **designlang** (9 techniques)
    - [TECH-designlang-basic-extraction](./references/TECH-designlang-basic-extraction.md) — Basic URL extraction (`designlang <url>`)
    - [TECH-designlang-brands](./references/TECH-designlang-brands.md) — `designlang brands` — N-way brand comparison matrix
    - [TECH-designlang-dark-mode](./references/TECH-designlang-dark-mode.md) — `--dark` — dark-mode extraction
    - [TECH-designlang-diff](./references/TECH-designlang-diff.md) — `designlang diff` — pairwise brand comparison
    - [TECH-designlang-full-mode](./references/TECH-designlang-full-mode.md) — `--full` — everything-at-once extraction
    - [TECH-designlang-interactions](./references/TECH-designlang-interactions.md) — `--interactions` — hover / focus / active state capture
    - (see `## References` for the remaining 3 in this group)

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-designlang-basic-extraction.md](./references/TECH-designlang-basic-extraction.md)**
  - Description: Basic URL extraction (`designlang <url>`)
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-brands.md](./references/TECH-designlang-brands.md)**
  - Description: `designlang brands` — N-way brand comparison matrix
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-dark-mode.md](./references/TECH-designlang-dark-mode.md)**
  - Description: `--dark` — dark-mode extraction
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-diff.md](./references/TECH-designlang-diff.md)**
  - Description: `designlang diff` — pairwise brand comparison
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-full-mode.md](./references/TECH-designlang-full-mode.md)**
  - Description: `--full` — everything-at-once extraction
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-interactions.md](./references/TECH-designlang-interactions.md)**
  - Description: `--interactions` — hover / focus / active state capture
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - 12. Interaction States
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-responsive.md](./references/TECH-designlang-responsive.md)**
  - Description: `--responsive` — breakpoint capture
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - 11. Responsive Design
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-score.md](./references/TECH-designlang-score.md)**
  - Description: `designlang score` — design-quality scoring
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-designlang-screenshots.md](./references/TECH-designlang-screenshots.md)**
  - Description: `--screenshots` — component screenshot capture
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-design-extract/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per `../amw-design-principles/ai-slop-avoid.md` (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. `designlang/` output folders (tokens.json, palette.json, screenshots, report.html)). The output path is determined by **project inference**, NOT hardcoded. See [`../amw-design-principles/references/project-output-routing.md`](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/tokens/` or `./design/references/` created fresh)
   - Last-resort scratch: `/tmp/amw-design-extract-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- [path/to/artifact.ext](./path/to/artifact.ext) — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.

## Failure modes

- **`npx: command not found`** — Node.js is not installed. User must install node ≥ 22 (surfaced by `/amw-doctor`).
- **First call stalls for 30–90 s** — expected. `npx` is downloading `designlang` and its Playwright browser on first use. Subsequent calls are cached.
- **Blank report / missing colors** — single-page app that fetches styles client-side. Re-run with `DL_ARGS="--wait 3000"` (passed through to designlang) or use `dev-browser` to screenshot + inspect first.
- **Auth wall (401/403)** — the page required login. Stop and ask the user whether they want to pass a session cookie; do not proceed silently.
- **Oversized palette (500+ colors)** — utility-CSS site (e.g. Tailwind-powered demo). Re-run with `--depth 0 --no-history` via raw pass-through; consider `colors` subcommand for just the essentials.
- **`preview.html` opens blank** — browser blocked a local-file fetch. Serve the output directory with `bin/amw-preview-server.py` instead of double-clicking.
