---
name: amw-mermaid-render
description: Render Mermaid diagram text to themed SVG or terminal/markdown ASCII via the vendored beautiful-mermaid backend. Triggers on "render mermaid as SVG", "mermaid to SVG", "mermaid ASCII", "mermaid ASCII for terminal", "themed mermaid diagram", "flowchart to SVG", "sequence diagram to SVG", "mermaid flowchart/state/class/ER diagram render", "batch render .mmd files", "apply dracula/tokyo-night theme to mermaid". This is the ONLY Mermaid renderer in the plugin — all skills that produce Mermaid source text must delegate rendering here. See body for what does NOT trigger this skill. Use when rendering Mermaid source text to themed SVG or terminal ASCII output. Trigger with /amw-create-or-modify-mermaid-diagram.
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

Callable directly via the `/amw-create-or-modify-mermaid-diagram` command (user shortcut — fast path for Mermaid source authoring and rendering). Also invoked by the `design-principles` orchestrator as a Phase B renderer after Phase A approval in Main-agent mode, and internally by diagram-editorial, diagram-architecture, and ux-flows when they need Mermaid output rendered. In Main-agent mode the orchestrator may apply any of the 15+ themes and batch-render techniques from this skill beyond what the command parameters expose.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**OUTPUT (Phase B).** Takes Mermaid text in, emits either a themed SVG string or a
Unicode/ASCII text rendering. Does not own any design decisions — the
caller decides what the diagram says and which theme to pick.

This skill does NOT substitute for:
- `../amw-diagram-editorial/` — editorial-quality HTML+SVG of 13 fixed diagram types, with brand tokens and blog-ready styling.
- `../amw-diagram-architecture/` — free-text architecture descriptions converted to JSON / Mermaid / SVG / PNG pipelines.
- `../amw-diagram-svg/` — freeform SVG primitives from natural-language intent.
- `../amw-ascii-validator/` — pixel-perfect ASCII diagrams from structured JSON (this skill's Mermaid ASCII is different: it is a Mermaid renderer output, not a JSON-driven layout).

When someone asks for "a diagram" without qualifying "Mermaid" or without supplying Mermaid source text, route back to `design-principles` so the right executor can be chosen.

## Trigger conditions

Activate only on narrow rendering intents that name Mermaid or supply Mermaid source text:

- "render this Mermaid as SVG"
- "mermaid → SVG"
- "turn this flowchart/sequence/state/class/ER diagram into SVG"
- "apply the dracula theme to this mermaid diagram"
- "mermaid ASCII for the terminal"
- "mermaid ASCII for the README"
- "batch-render these .mmd files"
- "list beautiful-mermaid themes"
- The user pastes a fenced \`\`\`mermaid … \`\`\` block and asks for rendering

Do NOT activate on:
- Generic design intent — `../amw-design-principles/`
- "Editorial" / "blog-ready" diagram intent — `../amw-diagram-editorial/`
- Free-text architecture descriptions without Mermaid source — `../amw-diagram-architecture/`
- ASCII wireframes (framed UI mockups) — `../amw-ascii-sketch/` (authoring) + `../amw-ascii-validator/` (validation)

## Output modes

### SVG — themed, high fidelity

- Mostly self-contained. One external reference: the SVG `<style>` block
  contains a single `@import url(...)` declaration pointing to the Google
  Fonts CSS2 endpoint for `Inter` (with the appropriate weight axis range)
  so the Inter font renders correctly when embedded in HTML.
  If the skill user needs a **fully offline** / CSP-strict SVG (no
  outbound font fetch), post-process the output by deleting the
  `@import url(...)` line — the SVG will then fall back to
  `'Inter', system-ui, sans-serif` (the `system-ui` stack ships on every
  modern OS). This is documented here so that callers who embed the SVG
  into CSP-locked pages know what to strip.
- No external scripts, no external CSS links, no CDN-hosted images —
  only the Inter font @import described above. Safe to embed in static
  HTML, MDX, or a sandboxed iframe when the iframe can reach Google
  Fonts (most do).
- 15 built-in themes (full list below). Also accepts any 2-color custom
  pair via `--bg` + `--fg` (the backend derives all other tokens from
  those two — see **Mono Mode derivation** below), or a 7-color enriched
  palette (`--bg` `--fg` `--line` `--accent` `--muted` `--surface`
  `--border`).
- Transparent-background mode available (`--transparent`) for dark/light
  compatibility.
- **Live theme-switching via CSS custom properties.** The SVG exposes
  `--bg`, `--fg`, `--line`, `--accent`, `--muted`, `--surface`, and
  `--border` as CSS custom properties on the root `<svg>` element. Host
  pages can override them *without re-rendering* — see the
  **Live theme-switching** section below.

### ASCII / Unicode — terminal + markdown

- Default is Unicode box-drawing (`+---+` for nodes, `│─┼└┘┐┌┤├` for edges).
- `--use-ascii` switches to pure ASCII (`+` `-` `|` `>` only) for
  environments with no Unicode support (legacy terminals, plain-ASCII log
  pipelines, very old markdown renderers).
- The wrapper post-processes ASCII output through `../../bin/amw-validate-ascii.py`
  as a **warn-only** gate. Mermaid's ASCII renderer is deterministic but
  its output width depends on the input labels — CJK characters, emoji,
  and long arrows can break column alignment. When this happens, the
  wrapper writes the output anyway and logs the alignment issues to
  stderr. The fix in that case is to shorten or rename the node labels,
  not to edit the rendered text.

## Themes

15 built-in themes, shipped with the backend. All are the `beautiful-mermaid` defaults — this skill does not add or remove themes.

**Light:**
- `zinc-light` — clean, high contrast, printable
- `github-light` — GitHub style
- `solarized-light` — Ethan Schoonover's classic
- `nord-light` — arctic blue
- `catppuccin-latte` — warm purple
- `tokyo-night-light` — Tokyo Night's light sibling

**Dark:**
- `zinc-dark` — minimalist
- `tokyo-night` — modern dev-friendly (default recommendation for technical docs)
- `tokyo-night-storm` — deeper Tokyo Night variant
- `catppuccin-mocha` — warm dark
- `nord` — arctic blue dark
- `dracula` — high-contrast purple/pink accents
- `github-dark` — GitHub dark
- `solarized-dark` — Solarized dark variant
- `one-dark` — Atom One Dark

List them at runtime:

```bash
bin/amw-mermaid-render.sh --list-themes
```

### Theme-selection guide by context

<!-- Source: Pretty-mermaid-skills-main/SKILL.md lines 277-289 -->

| Context | Recommended theme |
|---------|-------------------|
| Dark documentation (Markdown / MDX) | `tokyo-night` (default recommendation), `github-dark` |
| Light documentation | `github-light`, `zinc-light` |
| Vibrant / high-contrast | `dracula` |
| Print-friendly | `zinc-light`, `solarized-light` |
| High-contrast presentations | `zinc-light` (light), `zinc-dark` (dark) |
| Terminal output (screenshots in READMEs) | `tokyo-night`, `dracula` |
| Warm / friendly tone | `catppuccin-latte` (light), `catppuccin-mocha` (dark) |
| Minimalist arctic-blue | `nord-light`, `nord` |
| Brand-matching (not in list) | **Use 2-color Mono Mode** with the brand's `--bg` + `--fg` |

### Mono Mode — 2-color derivation ratios

<!-- Source: beautiful-mermaid-main/references/THEMES.md (derivation rules table) -->

When the caller supplies only `--bg` and `--fg`, the backend derives all
other tokens by blending `fg` into `bg` with fixed ratios (using the CSS
`color-mix(in srgb, ...)` function). This table lets downstream skills
*explain* their theme choice with the numbers:

| Element | Blend |
|---------|-------|
| Text (primary) | `--fg` at 100% |
| Text (secondary) | `--fg` 60% into `--bg` |
| Edge labels | `--fg` 40% into `--bg` |
| Connectors | `--fg` 30% into `--bg` |
| Arrow heads | `--fg` 50% into `--bg` |
| Node fill | `--fg` 3% into `--bg` |
| Node stroke | `--fg` 20% into `--bg` |

For finer control, pass any subset of `--line`, `--muted`, `--surface`,
`--border`, `--accent` to override individual derived tokens. Unprovided
colors still fall back to the Mono-Mode derivation above.

### Shiki integration — pipe a VS Code theme in

<!-- Source: beautiful-mermaid-main/references/THEMES.md lines 137-167 -->

If the caller already has a Shiki highlighter instance (e.g. because the
host site uses Shiki for code syntax highlighting), the library exposes
`fromShikiTheme()` so the Mermaid diagram picks up the *same* colors as
the surrounding code blocks. The wrapper does not surface this directly
— it is a library-level entry point you reach by writing a small Node
script against `external/mermaid-render/node_modules/beautiful-mermaid`:

```typescript
import { getSingletonHighlighter } from 'shiki'
import { renderMermaid, fromShikiTheme } from 'beautiful-mermaid'

const highlighter = await getSingletonHighlighter({
  themes: ['vitesse-dark', 'rose-pine', 'material-theme-darker']
})
const colors = fromShikiTheme(highlighter.getTheme('vitesse-dark'))
const svg = await renderMermaid(diagram, colors)
```

#### Shiki → beautiful-mermaid color mapping

| Shiki / VS Code token | Diagram role |
|-----------------------|--------------|
| `editor.background`           | `bg` |
| `editor.foreground`           | `fg` |
| `editorLineNumber.foreground` | `muted` |
| `focusBorder`                 | `accent` |
| `editorWidget.background`     | `surface` |
| `editorWidget.border`         | `border` |

### Live theme-switching (browser)

<!-- Source: beautiful-mermaid-main/references/THEMES.md lines 170-200 -->

SVG output declares its theme as CSS custom properties on the root
`<svg>` element, which means a host page can flip themes at runtime
*without re-rendering* the diagram:

```javascript
const svgElement = document.querySelector('svg')

// Switch to dark
svgElement.style.setProperty('--bg', '#1a1b26')
svgElement.style.setProperty('--fg', '#a9b1d6')

// Switch to light
svgElement.style.setProperty('--bg', '#ffffff')
svgElement.style.setProperty('--fg', '#27272a')
```

The full custom-property interface on the SVG root is:

```css
svg {
  --bg: #ffffff;
  --fg: #27272a;
  --line: /* derived via Mono Mode if not set */;
  --accent: /* derived */;
  --muted: /* derived */;
  --surface: /* derived */;
  --border: /* derived */;
}
```

Set only `--bg` + `--fg` for a Mono-Mode runtime switch; the browser
re-derives the other tokens via `color-mix()`. Set the full 7 to
override each token explicitly.

## Usage

All invocations go through the shell wrapper `../../bin/amw-mermaid-render.sh`.
It handles the "external/mermaid-render/ is missing" case cleanly, adds
stdin input (the vendored render.mjs also supports `-i -`), and pipes
ASCII output through the alignment validator.

### Full flag surface

<!-- Source: Pretty-mermaid-skills-main/scripts/render.mjs lines 60-98 (parseArgs) -->

The wrapper forwards *all* flags verbatim to the vendored `render.mjs`
except `--format` and `--out`, which it also records for ASCII
post-processing. The backend accepts 17 flags total:

| Flag | Default | Purpose |
|---|---|---|
| `--input <file>` / `-i <file>` | (required) | Input `.mmd` file. Use `-` to read from stdin. |
| `--out <file>` / `--output <file>` / `-o <file>` | stdout | Output file path. |
| `--format <fmt>` / `-f <fmt>` | `svg` | Output format: `svg` or `ascii`. |
| `--theme <name>` / `-t <name>` | (none → Mono Mode) | One of the 15 built-in themes. |
| `--bg <hex>` | `#FFFFFF` | Background color (Mono Mode). |
| `--fg <hex>` | `#27272A` | Foreground color (Mono Mode). |
| `--line <hex>` | (derived) | Edge / connector color. |
| `--accent <hex>` | (derived) | Arrow-head and highlight color. |
| `--muted <hex>` | (derived) | Secondary text / label color. |
| `--surface <hex>` | (derived) | Node fill-tint color. |
| `--border <hex>` | (derived) | Node stroke color. |
| `--font <name>` | `Inter` | Font family for SVG labels. |
| `--transparent` | off | Transparent background (SVG only). |
| `--use-ascii` | off | Pure ASCII (`+` `-` `|` `>`) instead of Unicode box-drawing (ASCII only). |
| `--padding-x <n>` | `5` | Horizontal node spacing (ASCII only). |
| `--padding-y <n>` | `5` | Vertical node spacing (ASCII only). |
| `--box-border-padding <n>` | `1` | Padding inside node boxes (ASCII only). |

### stdin fallback

<!-- Source: agent-skill-diagramming-flows-main/render.ts lines 39-56 -->

If `--input` is omitted entirely AND stdin is not a TTY (i.e. the shell
is piping something in), the wrapper reads Mermaid text from stdin into
a temp file and renders that. This is in addition to the explicit
`--input -` form, which has always worked:

```bash
# Either of these works:
echo 'graph LR; A --> B' | bin/amw-mermaid-render.sh --input - --format ascii
echo 'graph LR; A --> B' | bin/amw-mermaid-render.sh --format ascii
```

### Use newlines between the header and nodes, not semicolons

<!-- Source: agent-skill-diagramming-flows-main/SKILL.md line 20 -->

Mermaid's parser accepts `;` as a statement separator on single-line
flowcharts, but when you pipe multi-statement input through `echo`, the
shell sometimes strips or re-escapes the semicolons in ways that mangle
the parse tree. Prefer newlines:

```bash
# Reliable
printf 'graph LR\nA --> B\nB --> C\n' | bin/amw-mermaid-render.sh --format svg --out d.svg

# Flaky (works in some shells, fails in others)
echo 'graph LR; A --> B; B --> C' | bin/amw-mermaid-render.sh --format svg --out d.svg
```

### Render a file → SVG (themed)

```bash
bin/amw-mermaid-render.sh \
  --input diagram.mmd \
  --format svg \
  --theme tokyo-night \
  --out diagram.svg
```

### Render stdin → ASCII (Unicode)

```bash
echo 'graph LR; A --> B --> C' | \
  bin/amw-mermaid-render.sh --input - --format ascii
```

### Render stdin → pure ASCII for README

```bash
cat architecture.mmd | \
  bin/amw-mermaid-render.sh --input - --format ascii --use-ascii --out architecture.txt
```

### Custom 2-color palette (no built-in theme)

```bash
bin/amw-mermaid-render.sh \
  --input diagram.mmd \
  --format svg \
  --bg "#0f0f0f" \
  --fg "#e0e0e0" \
  --accent "#ff6b6b" \
  --out diagram.svg
```

### Transparent background

```bash
bin/amw-mermaid-render.sh \
  --input diagram.mmd \
  --format svg \
  --theme github-dark \
  --transparent \
  --out diagram.svg
```

### Batch render a directory (parallel workers)

<!-- Source: Pretty-mermaid-skills-main/scripts/batch.mjs (parseArgs + worker loop) -->

```bash
node external/mermaid-render/scripts/batch.mjs \
  --input-dir ./diagrams \
  --output-dir ./rendered \
  --format svg \
  --theme tokyo-night \
  --workers 4
```

`--workers N` defaults to **4**. For 10+ diagrams, bump it to `8` to
cut wall-clock time roughly in half on multi-core laptops. Upper bound
is the number of CPU cores — more workers than cores actually slows the
batch down because each `node` process has to re-load the
beautiful-mermaid library. (`batch.mjs` is not exposed through the
shell wrapper because it has a different arg shape. Invoke it directly
when you have 3+ diagrams to render at once. `batch.mjs` ships with the
vendored `external/mermaid-render/scripts/` — `/amw-doctor` verifies it
is present.)

## Supported diagram types

| Type | Header | Example |
|---|---|---|
| Flowchart | `graph TD` / `graph LR` / `graph BT` / `graph RL` / `flowchart ...` | `graph LR; A --> B` |
| State | `stateDiagram-v2` | `stateDiagram-v2\n[*] --> Active` |
| Sequence | `sequenceDiagram` | `sequenceDiagram\nAlice->>Bob: Hi` |
| Class | `classDiagram` | `classDiagram\nAnimal <|-- Dog` |
| ER | `erDiagram` | `erDiagram\nUSER ||--o{ ORDER : places` |

Templates for all 5 types live under `../../external/mermaid-render/examples/`. Copy one, edit, render.

## Non-negotiables (house rules)

1. **No external CDN references beyond the single Google Fonts @import
   for Inter.** The backend inlines everything else — styles, arrowheads,
   theme CSS variables. Do NOT post-process the SVG to add additional
   external stylesheets, scripts, or images. If the caller needs a fully
   CSP-locked SVG, strip the Google Fonts `@import url(...)` line (the one
   that points at `fonts.googleapis.com`) from the `<style>` block; the
   system font stack takes over.
2. **ASCII output must pass `../../bin/amw-validate-ascii.py` or warn loudly.**
   The wrapper enforces this automatically — if the validator flags
   alignment issues, the stderr message is visible to the caller. Do not
   silence that warning; if it triggers, the fix is to shorten or rename
   the Mermaid node labels until the validator is quiet.
3. **15 built-in themes are the total theme surface.** If the user asks
   for a custom color scheme, map it onto the 2-color or 7-color palette
   arguments (`--bg`, `--fg`, `--accent`, …). Do not add new named themes
   to this plugin — upstream owns the theme namespace.
4. **No substitute Mermaid backend.** This skill is the single Mermaid
   renderer in the plugin. If you are tempted to add `@mermaid-js/mermaid-cli`
   (requires Puppeteer + Chrome), `mermaid` npm (requires a DOM), or a
   WASM build, stop — the beautiful-mermaid library is headless, has zero
   runtime browser requirements, and is 50× smaller on disk.

## Runtime dependencies

- Node.js ≥ 18 — checked by `bin/amw-mermaid-render.sh` and by `/amw-doctor`.
- `external/mermaid-render/` directory present with `package.json` and `scripts/`.
- On first render, the wrapper calls `npm install` inside
  `external/mermaid-render/` to fetch `beautiful-mermaid@^0.1.3`. The
  resulting `node_modules/` is gitignored.

### Auto-install fallback (how it actually works)

<!-- Source: Pretty-mermaid-skills-main/scripts/render.mjs lines 11-37 (loadBeautifulMermaid) -->

The vendored `render.mjs` wraps its library load in a `loadBeautifulMermaid()`
helper that is resilient to a cold checkout of the plugin:

1. Try `import('beautiful-mermaid')` — fast path when `node_modules/` is already populated.
2. On `MODULE_NOT_FOUND`, silently run `execSync('npm install --no-fund --no-audit')` in `external/mermaid-render/` (120s timeout, stderr passthrough).
3. After install succeeds, import the package directly from `node_modules/beautiful-mermaid/dist/index.js` (belt-and-braces fallback; plain `import('beautiful-mermaid')` sometimes misses the just-installed copy on macOS).
4. Any failure in step 2 or 3 exits with code 1 and prints the manual-fix line (`cd external/mermaid-render && npm install`).

This means the first `bin/amw-mermaid-render.sh` invocation after `git clone`
can take ~20-60 seconds (npm install), and every subsequent run is
sub-second. `/amw-doctor` runs a dry render to pre-warm the install.

If `external/mermaid-render/` is missing, the wrapper exits with code 2
and tells the user to run `/amw-init`. See `/amw-init` step 7 for the
vendor-fetch instructions and `/amw-doctor` for the runtime probe.

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

**"Cannot find module 'beautiful-mermaid'"** — the auto-install inside
`external/mermaid-render/` failed. Run it manually:
`cd external/mermaid-render && npm install`.

**Empty SVG output** — invalid Mermaid syntax. Test at https://mermaid.live
before filing a bug against the renderer.

**Fonts not rendering** — the SVG inlines a `font-family` declaration;
if the target system lacks the font, the browser falls back. Use a
web-safe stack (`"Inter, system-ui, sans-serif"`) for broader reach, or
add `@font-face` in your host page.

**CJK / emoji breaking ASCII alignment** — expected. The Mermaid ASCII
renderer doesn't know those characters are double-width. Rename the
node labels or switch to SVG output.

## Examples

See the `## Usage` section above for worked shell invocation examples (SVG render, ASCII render, custom palette, transparent background, batch directory). Template files for all 5 supported diagram types live under `../../external/mermaid-render/examples/`.

## Technique selection

Walk this decision tree top-down to pick the right reference. If a branch does not match the user's intent, skip to the next. Every technique in the catalog is a leaf of this tree.

- Which aspect of `mermaid-render` is the user asking about?
  - **ascii** (3 techniques)
    - [TECH-ascii-markdown-integration](./references/TECH-ascii-markdown-integration.md) — Wrapping ASCII output for Markdown
    - [TECH-ascii-padding-options](./references/TECH-ascii-padding-options.md) — `paddingX` / `paddingY` / `boxBorderPadding`
    - [TECH-ascii-render-api](./references/TECH-ascii-render-api.md) — `renderMermaidAscii()` — Mermaid → ASCII / Unicode
  - **auto** (1 techniques)
    - [TECH-auto-install-dependency](./references/TECH-auto-install-dependency.md) — Auto-install `beautiful-mermaid` on first use
  - **batch** (1 techniques)
    - [TECH-batch-rendering](./references/TECH-batch-rendering.md) — Batch rendering — worker-pool directory mode
  - **built** (1 techniques)
    - [TECH-built-in-themes](./references/TECH-built-in-themes.md) — `THEMES[...]` — 15 pre-baked theme objects
  - **custom** (1 techniques)
    - [TECH-custom-colors-override](./references/TECH-custom-colors-override.md) — CLI color overrides — per-invocation theming
  - **enriched** (1 techniques)
    - [TECH-enriched-mode](./references/TECH-enriched-mode.md) — Enriched Mode — override specific derived tokens
  - **live** (1 techniques)
    - [TECH-live-theme-switch](./references/TECH-live-theme-switch.md) — Live theme switching — CSS custom properties
  - **mono** (1 techniques)
    - [TECH-mono-mode](./references/TECH-mono-mode.md) — Mono Mode — 2-color theme foundation
  - **shiki** (1 techniques)
    - [TECH-shiki-theme-import](./references/TECH-shiki-theme-import.md) — `fromShikiTheme()` — import any VS Code theme
  - **svg** (1 techniques)
    - [TECH-svg-render-api](./references/TECH-svg-render-api.md) — `renderMermaid()` — Mermaid → SVG
  - **terminal** (1 techniques)
    - [TECH-terminal-output-ansi](./references/TECH-terminal-output-ansi.md) — Adding ANSI colors to ASCII output
      > What it does · When to use · Pattern 1: Highlight node names · Pattern 2: Whole-diagram color wrap · Pattern 3: Per-node status colors · Gotchas · Cross-references
  - **theme** (1 techniques)
    - [TECH-theme-selection-guide](./references/TECH-theme-selection-guide.md) — Theme selection decision tree

## References

Every technique in this skill is documented as a single reference file under `./references/`. The orchestrator should read only the file whose TOC matches its current need.

- **[./references/TECH-ascii-markdown-integration.md](./references/TECH-ascii-markdown-integration.md)**
  - Description: Wrapping ASCII output for Markdown
  - TOC:
    - What it does
    - When to use
    - Pattern 1: plain fenced block
    - Pattern 2: inline compact diagram
    - Pattern 3: ASCII mode for email / plain text
    - Gotchas
    - Cross-references
- **[./references/TECH-ascii-padding-options.md](./references/TECH-ascii-padding-options.md)**
  - Description: `paddingX` / `paddingY` / `boxBorderPadding`
  - TOC:
    - What it does
    - When to use
    - Defaults
    - What each one does
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-ascii-render-api.md](./references/TECH-ascii-render-api.md)**
  - Description: `renderMermaidAscii()` — Mermaid → ASCII / Unicode
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-auto-install-dependency.md](./references/TECH-auto-install-dependency.md)**
  - Description: Auto-install `beautiful-mermaid` on first use
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example — setup.sh equivalent
    - Gotchas
    - Cross-references
- **[./references/TECH-batch-rendering.md](./references/TECH-batch-rendering.md)**
  - Description: Batch rendering — worker-pool directory mode
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-built-in-themes.md](./references/TECH-built-in-themes.md)**
  - Description: `THEMES[...]` — 15 pre-baked theme objects
  - TOC:
    - What it does
    - When to use
    - The full 15
    - Recommended defaults
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-custom-colors-override.md](./references/TECH-custom-colors-override.md)**
  - Description: CLI color overrides — per-invocation theming
  - TOC:
    - What it does
    - When to use
    - The seven override flags
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-enriched-mode.md](./references/TECH-enriched-mode.md)**
  - Description: Enriched Mode — override specific derived tokens
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-live-theme-switch.md](./references/TECH-live-theme-switch.md)**
  - Description: Live theme switching — CSS custom properties
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-mono-mode.md](./references/TECH-mono-mode.md)**
  - Description: Mono Mode — 2-color theme foundation
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-shiki-theme-import.md](./references/TECH-shiki-theme-import.md)**
  - Description: `fromShikiTheme()` — import any VS Code theme
  - TOC:
    - What it does
    - When to use
    - Shiki → diagram token mapping
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-svg-render-api.md](./references/TECH-svg-render-api.md)**
  - Description: `renderMermaid()` — Mermaid → SVG
  - TOC:
    - What it does
    - When to use
    - How it works
    - Minimal example
    - Gotchas
    - Cross-references
- **[./references/TECH-terminal-output-ansi.md](./references/TECH-terminal-output-ansi.md)**
  - Description: Adding ANSI colors to ASCII output
  - TOC:
    - What it does
    - When to use
    - Pattern 1: Highlight node names
    - Pattern 2: Whole-diagram color wrap
    - Pattern 3: Per-node status colors
    - Gotchas
    - Cross-references
- **[./references/TECH-theme-selection-guide.md](./references/TECH-theme-selection-guide.md)**
  - Description: Theme selection decision tree
  - TOC:
    - What it does
    - When to use
    - Decision tree
    - Context-to-theme cheat table
    - Minimal example
    - Gotchas
    - Cross-references

<!-- end of references -->

## Completion checklist

Before reporting a job using this skill as complete, verify every item below. FAIL on any item should trigger a remediation loop; do not deliver partial work.

- Inputs captured verbatim from the user (brief, URL, reference files) — no silent paraphrasing that changes meaning.
- At least one `TECH-*.md` file from `skills/amw-mermaid-render/references/` was consulted and is cited in the final report.
- Output passes the skill's own non-negotiables (see the `Non-negotiables` section below if present).
- No AI-slop per [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) (generic gradients, stock-photo hero, fake testimonials, lorem copy, CTA-hero-features-testimonials template).
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
- If the skill emits HTML/SVG/ASCII, the output was rendered/validated by the matching tool (`bin/amw-validate-ascii.py`, `bin/amw-html-export.py`, `bin/amw-svg-render.py`, etc.).
- Cross-skill hand-offs documented — if work routed through another skill, that skill's SKILL.md + TECH file are named in the report.
- User-facing filename is descriptive English (`Login Flow.html`, not `output.html`).

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — the actual work product (e.g. `.svg` or terminal-ASCII renderings of Mermaid source). The output path is determined by **project inference**, NOT hardcoded. See [[project-output-routing](../amw-design-principles/references/project-output-routing.md)](../amw-design-principles/references/project-output-routing.md) for the full detection rules. Summary of the priority order:
  > When to consult this doc · Detection order · User-supplied path · Project-type detection (inspect project root) · Existing design folder · Existing convention from Claude design skills · Generic fallback (no project type detected) · Last resort (nothing matched, no project context at all) · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references
   - User-supplied path (honor verbatim)
   - Framework convention (React/Vite/Next/Astro → `./src/...`; Flutter → `./lib/`; etc.)
   - Existing `./design/<subtype>/` folder if present
   - Generic fallback (`./design/diagrams/` created fresh)
   - Last-resort scratch: `/tmp/amw-mermaid-render-<slug>/`

   Every artifact file is listed with its path in the report (next item).

2. **Job-completion report** — a markdown file at:
   `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`

   The report must contain, in order:
   - **Inputs** — what the user provided + any auto-detected context
   - **Method** — which TECH references were consulted, which pipeline steps ran
   - **Artifacts** — bullet list, one per produced file, formatted as:
     `- <artifact-path> — <1-line description> — **How to use:** <usage tip> — **Next steps:** <suggested follow-up>`
   - **Checklist** — each item from the Completion checklist above, with PASS / FAIL / N/A
   - **Deviations** — any step skipped or changed, with rationale

   The `<8-char-hash>` is a short content-addressed hash of the report body (e.g. first 8 chars of SHA-256 of the inputs+artifacts list) for uniqueness.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'` (main-repo root, worktree-safe).

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the skill run is considered incomplete. The report path is distinct from `reports/audit/` (build-time audit artifacts) — `reports/webdesigner/` is for user-facing job outputs from this plugin.
