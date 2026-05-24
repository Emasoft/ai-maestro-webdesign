---
name: amw-mermaid-render
description: Render Mermaid diagram text to themed SVG or terminal/markdown ASCII via the vendored beautiful-mermaid backend. Triggers on "render mermaid as SVG", "mermaid to SVG", "mermaid ASCII", "themed mermaid diagram", "batch render .mmd files", "apply dracula/tokyo-night theme to mermaid". ONLY Mermaid renderer in the plugin — all skills producing Mermaid source delegate rendering here. Use when rendering Mermaid source to themed SVG or ASCII. Trigger with /amw-create-or-modify-mermaid-diagram.
version: 1.0.0
author: ai-maestro-webdesign
---

# Mermaid Render

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> This skill is an executor. `design-principles` routes here when the user
> has committed to a Mermaid diagram and wants it as SVG (for docs/slides)
> or ASCII (for terminal/markdown/READMEs).

## Overview

Renders Mermaid diagram source text to themed SVG or Unicode/ASCII output via the vendored `beautiful-mermaid` backend (`external/mermaid-render/`). The plugin's single Mermaid renderer — all skills that produce `.mmd` source must delegate rendering here. Supports 15 built-in themes, 2-color Mono Mode derivation, 7-color enriched palette, transparent backgrounds, and batch directory rendering. ASCII output is post-processed through `bin/amw-validate-ascii.py` as a warn-only gate.

## Prerequisites

Standard plugin runtime — no skill-specific prerequisites beyond the global plugin dependencies.

## Instructions

1. Confirm the input is Mermaid source text (fenced block or `.mmd` file); if not, route back to `../amw-design-principles/` for format selection.
2. Select a theme from the 15 built-in options or supply `--bg` + `--fg` for Mono Mode derivation (all other tokens auto-derived); default recommendation for technical docs is `tokyo-night`.
3. Choose output format: `--format svg` (default, themed SVG with Inter font @import) or `--format ascii` (Unicode box-drawing; add `--use-ascii` for pure-ASCII environments).
4. Invoke `bin/amw-mermaid-render.sh --input <file.mmd> --format <svg|ascii> --theme <name>` (or `--bg #hex --fg #hex` for Mono Mode); for batch rendering pass a directory path.
5. For ASCII output, check stderr for alignment warnings from `bin/amw-validate-ascii.py` (warn-only gate); if warnings appear, shorten node labels and re-render — do not edit the rendered text directly.
6. Return the SVG string or ASCII block to the caller; save to disk only when the user requests a file output.

See the `## Usage` section below for the full flag surface and shell invocation patterns.

## Activation

Callable directly via `/amw-create-or-modify-mermaid-diagram`. Also invoked by `design-principles` (Phase B Mermaid renderer after Phase A approval) and internally by diagram-editorial, diagram-architecture, ux-flows when they need rendering.

Autonomous and self-contained — any agent can use it by reading this SKILL.md and references.

## Position in flow

**OUTPUT (Phase B).** Mermaid text in → themed SVG or Unicode/ASCII out. Owns no design decisions.

Does NOT substitute for:
- `../amw-diagram-editorial/` — HTML+SVG editorial diagrams (13 fixed types, brand tokens).
- `../amw-diagram-architecture/` — free-text architecture → JSON/Mermaid/SVG/PNG.
- `../amw-diagram-svg/` — freeform SVG primitives.
- `../amw-ascii-validator/` — pixel-perfect JSON-driven ASCII diagrams.

Generic "a diagram" requests without Mermaid source → route to `design-principles`.

## Trigger conditions

Activate only on narrow rendering intents naming Mermaid or supplying Mermaid source text. Examples: "render this Mermaid as SVG", "mermaid → SVG", "apply the dracula theme", "mermaid ASCII for terminal/README", "batch-render these .mmd files", or a fenced ` ```mermaid ``` ` block with a render request.

Do NOT activate on: generic design intent (→ `../amw-design-principles/`), editorial diagram intent (→ `../amw-diagram-editorial/`), free-text architecture descriptions without Mermaid source (→ `../amw-diagram-architecture/`), ASCII wireframes (→ `../amw-ascii-sketch/` + `../amw-ascii-validator/`).

## Output modes

### SVG — themed, high fidelity

Mostly self-contained. The SVG `<style>` block has one `@import url(...)` for Inter (Google Fonts CSS2). For CSP-strict / offline embedding, strip that line — the SVG falls back to `'Inter', system-ui, sans-serif`. No external scripts, no CDN images. 15 built-in themes; also accepts 2-color (`--bg` + `--fg`) or 7-color enriched palette. Transparent mode via `--transparent`. Live re-theming without re-render — see Themes section below.

### ASCII / Unicode — terminal + markdown

Default is Unicode box-drawing. `--use-ascii` switches to pure ASCII (`+ - | >`) for legacy terminals or plain-ASCII pipelines. The wrapper pipes output through `bin/amw-validate-ascii.py` as a **warn-only** gate — CJK / emoji / long arrows can break column alignment; the wrapper writes anyway and logs to stderr. Fix is to shorten node labels, NOT to edit the rendered text.

## Themes

15 built-in themes, shipped with the backend. All are `beautiful-mermaid` defaults — this skill does not add or remove themes.

- **Light:** `zinc-light`, `github-light`, `solarized-light`, `nord-light`, `catppuccin-latte`, `tokyo-night-light`
- **Dark:** `zinc-dark`, `tokyo-night` (default recommendation), `tokyo-night-storm`, `catppuccin-mocha`, `nord`, `dracula`, `github-dark`, `solarized-dark`, `one-dark`

List them at runtime: `bin/amw-mermaid-render.sh --list-themes`.

For the complete theme list, derivation rationale, and decision tree see [TECH-built-in-themes](references/TECH-built-in-themes.md) and [TECH-theme-selection-guide](references/TECH-theme-selection-guide.md).

### Mono Mode, Shiki integration, and live theme-switching

When `--bg`+`--fg` alone are supplied, all other tokens derive via `color-mix(in srgb, ...)` ratios. See [TECH-mono-mode](references/TECH-mono-mode.md) for the full blend table.

Shiki VS Code themes can be piped via `fromShikiTheme()` — see [TECH-shiki-theme-import](references/TECH-shiki-theme-import.md) for the Shiki→token mapping table and minimal example.

The output SVG exposes `--bg`, `--fg`, `--line`, `--accent`, `--muted`, `--surface`, `--border` as CSS custom properties on the root `<svg>`, so host pages can re-theme at runtime without re-rendering. See [TECH-live-theme-switch](references/TECH-live-theme-switch.md) for the full interface.

## Usage

All invocations go through the shell wrapper `../../bin/amw-mermaid-render.sh`.
It handles the "external/mermaid-render/ is missing" case cleanly, adds
stdin input (the vendored render.mjs also supports `-i -`), and pipes
ASCII output through the alignment validator.

### Full flag surface

The wrapper forwards all flags verbatim to the vendored `render.mjs`. The backend accepts 17 flags. Core flags: `--input` / `-i` (file or `-` for stdin), `--out` / `-o`, `--format` (svg|ascii), `--theme`, `--bg`/`--fg` (Mono Mode), `--line`/`--accent`/`--muted`/`--surface`/`--border` (7-color enriched), `--font`, `--transparent` (SVG only), `--use-ascii` (pure ASCII), `--padding-x`/`--padding-y`/`--box-border-padding` (ASCII only, default 5/5/1).

Full per-flag detail: [TECH-custom-colors-override](references/TECH-custom-colors-override.md) and [TECH-ascii-padding-options](references/TECH-ascii-padding-options.md).

### stdin fallback and gotchas

If `--input` is omitted AND stdin is not a TTY, the wrapper reads Mermaid text from stdin into a temp file. Both `--input -` and the bare stdin form work.

Prefer newlines over semicolons in piped input — shells sometimes re-escape `;` in ways that mangle the parse tree.

```bash
# Reliable
printf 'graph LR\nA --> B\nB --> C\n' | bin/amw-mermaid-render.sh --format svg --out d.svg
```

### Common invocation patterns

```bash
# File → themed SVG
bin/amw-mermaid-render.sh --input diagram.mmd --format svg --theme tokyo-night --out diagram.svg

# Stdin → Unicode ASCII
echo 'graph LR; A --> B --> C' | bin/amw-mermaid-render.sh --input - --format ascii

# Stdin → pure ASCII for README
cat architecture.mmd | bin/amw-mermaid-render.sh --input - --format ascii --use-ascii --out architecture.txt

# Custom 2-color palette (no built-in theme)
bin/amw-mermaid-render.sh --input diagram.mmd --format svg --bg "#0f0f0f" --fg "#e0e0e0" --accent "#ff6b6b" --out diagram.svg

# Transparent background (SVG only)
bin/amw-mermaid-render.sh --input diagram.mmd --format svg --theme github-dark --transparent --out diagram.svg
```

For per-flag color overrides see [TECH-custom-colors-override](references/TECH-custom-colors-override.md); for ASCII padding flags see [TECH-ascii-padding-options](references/TECH-ascii-padding-options.md).

### Batch render

```bash
node external/mermaid-render/scripts/batch.mjs --input-dir ./diagrams --output-dir ./rendered --format svg --theme tokyo-night --workers 4
```

`--workers N` defaults to 4 (max ≈ CPU cores). Use for 3+ diagrams. `batch.mjs` has a different arg shape from the wrapper — invoke directly. Full details: [TECH-batch-rendering](references/TECH-batch-rendering.md).

## Supported diagram types

| Type | Header | Example |
|---|---|---|
| Flowchart | `graph TD` / `graph LR` / `graph BT` / `graph RL` / `flowchart ...` | `graph LR; A --> B` |
| State | `stateDiagram-v2` | `stateDiagram-v2\n[*] --> Active` |
| Sequence | `sequenceDiagram` | `sequenceDiagram\nAlice->>Bob: Hi` |
| Class | `classDiagram` | `classDiagram\nAnimal <\|-- Dog` |
| ER | `erDiagram` | `erDiagram\nUSER \|\|--o{ ORDER : places` |

Templates for all 5 types live under `../../external/mermaid-render/examples/`. Copy one, edit, render.

## Non-negotiables (house rules)

1. **No external CDN refs beyond the single Google Fonts @import for Inter.** Backend inlines everything else. For CSP-locked SVG, strip the `@import url(...)` line — system font stack takes over.
2. **ASCII output passes `bin/amw-validate-ascii.py` or warns loudly.** Wrapper enforces this. Never silence the stderr warning — fix is to shorten/rename Mermaid node labels.
3. **15 built-in themes is the total theme surface.** Custom colors → 2-color or 7-color palette args. Do not add new named themes (upstream owns the namespace).
4. **No substitute Mermaid backend.** Do NOT add `@mermaid-js/mermaid-cli` (Puppeteer+Chrome), `mermaid` npm (DOM), or WASM build. beautiful-mermaid is headless, zero-browser, 50× smaller.

## Runtime dependencies

- Node.js ≥ 18 — checked by `bin/amw-mermaid-render.sh` and by `/amw-doctor`.
- `external/mermaid-render/` directory present with `package.json` and `scripts/`.
- On first render, the wrapper calls `npm install` inside
  `external/mermaid-render/` to fetch `beautiful-mermaid@^0.1.3`. The
  resulting `node_modules/` is gitignored.

### Auto-install fallback

On `MODULE_NOT_FOUND`, the wrapper silently runs `npm install` in `external/mermaid-render/` (120s timeout), then re-imports. First run after `git clone` takes 20-60s; subsequent runs are sub-second. `/amw-doctor` pre-warms the install. If `external/mermaid-render/` is missing entirely the wrapper exits with code 2 and tells the user to run `/amw-init`. Full algorithm: [TECH-auto-install-dependency](references/TECH-auto-install-dependency.md).

## Resources

- Orchestrator: [SKILL](../amw-design-principles/SKILL.md)
- Validator the ASCII path pipes through: [SKILL](../amw-ascii-validator/SKILL.md)
- Editorial diagram alternative (HTML+SVG, 13 fixed types, brand tokens): [SKILL](../amw-diagram-editorial/SKILL.md)
- Architecture diagram pipeline (accepts free text, emits Mermaid or SVG): [SKILL](../amw-diagram-architecture/SKILL.md)
- Vendored backend + LICENSE: `../../external/mermaid-render/`
- Shell wrapper: `../../bin/amw-mermaid-render.sh`

## Error Handling

- `exit 2` — `external/mermaid-render/` missing. Run `/amw-init`.
- `exit 3` — `node` not on PATH. Install Node.js ≥ 18.
- `exit 1 + "Parse error on line N"` — invalid Mermaid syntax. Test it at https://mermaid.live first.
- `exit 1 + "Unknown theme"` — theme name typo. Run `bin/amw-mermaid-render.sh --list-themes`.
- `validate-ascii.py` warnings on stderr — the ASCII output has variable-width glyphs. Fix the input labels (shorten, remove CJK/emoji) and re-render.

## Troubleshooting

- **"Cannot find module 'beautiful-mermaid'"** — auto-install failed. `cd external/mermaid-render && npm install`.
- **Empty SVG output** — invalid Mermaid syntax. Test at https://mermaid.live first.
- **Fonts not rendering** — target system lacks the font; use `"Inter, system-ui, sans-serif"` or `@font-face` in host page.
- **CJK/emoji breaking ASCII alignment** — expected (double-width). Rename labels or switch to SVG.

## Examples

See the `## Usage` section above for worked shell invocation examples (SVG render, ASCII render, custom palette, transparent background, batch directory). Template files for all 5 supported diagram types live under `../../external/mermaid-render/examples/`.

## Technique selection

Walk this map by intent to pick the right reference (`./references/TECH-*.md`):

| Intent | Reference |
|---|---|
| Render Mermaid → SVG | `TECH-svg-render-api` |
| Render Mermaid → ASCII/Unicode | `TECH-ascii-render-api` |
| Wrap ASCII output for Markdown | `TECH-ascii-markdown-integration` |
| Tune ASCII padding/spacing | `TECH-ascii-padding-options` |
| Add ANSI colors to ASCII | `TECH-terminal-output-ansi` |
| Pick a built-in theme | `TECH-built-in-themes`, `TECH-theme-selection-guide` |
| 2-color brand theming | `TECH-mono-mode` |
| Override individual derived tokens | `TECH-enriched-mode` |
| Per-invocation CLI color overrides | `TECH-custom-colors-override` |
| Import a Shiki/VS Code theme | `TECH-shiki-theme-import` |
| Browser runtime theme switch | `TECH-live-theme-switch` |
| Batch directory render (worker pool) | `TECH-batch-rendering` |
| Auto-install dependency on first use | `TECH-auto-install-dependency` |

## References

All techniques are documented under `./references/` as `TECH-*.md` files. Read only the file matching your current need — the **Technique selection** decision tree above maps intent to file.

Full list (14 reference files): `TECH-ascii-markdown-integration`, `TECH-ascii-padding-options`, `TECH-ascii-render-api`, `TECH-auto-install-dependency`, `TECH-batch-rendering`, `TECH-built-in-themes`, `TECH-custom-colors-override`, `TECH-enriched-mode`, `TECH-live-theme-switch`, `TECH-mono-mode`, `TECH-shiki-theme-import`, `TECH-svg-render-api`, `TECH-terminal-output-ansi`, `TECH-theme-selection-guide`.

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-mermaid-render/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

Two kinds of output:

1. **Artifact(s)** — SVG or terminal-ASCII renderings. Output path determined by project inference (user-supplied > framework convention > existing `./design/<subtype>/` > `./design/diagrams/` > `/tmp/amw-mermaid-render-<slug>/`). Full rules: [project-output-routing](../amw-design-principles/references/project-output-routing.md).
2. **Job-completion report** — markdown file at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`. Contains: Inputs, Method (TECH references consulted), Artifacts (path + 1-line description + usage tip + next steps), Checklist (PASS/FAIL/N/A), Deviations. Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`.

Every artifact MUST be linked from the report.
