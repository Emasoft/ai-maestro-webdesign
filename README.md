# ai-maestro-webdesign

A consolidated Claude Code plugin for web and UI design work. Replaces the habit of juggling a dozen single-purpose plugins with one orchestrated set of skills, commands, and shared scripts.

## Core idea — one orchestrator, many executors

The `amw-design-principles` skill is the **orchestrator**. Its three hard rules run first on every design task:

1. Gather design context (design system, brand tokens, references) before designing anything.
2. Always produce at least three variants (baseline → advanced → experimental), never a single guessed answer.
3. Reject the catalogued AI-slop patterns (generic gradients, fake testimonials, AI-drawn illustrations, etc.).

Every other skill in this plugin is an **executor**. They are triggered only by specific technical phrases, never by generic design vocabulary, so the orchestrator always wins first-activation and decides which executor to route to.

## Capabilities

**Input (capture context the orchestrator needs):**
- `amw-dev-browser` — sandboxed browser automation for screenshots, DOM inspection, scraping
- `amw-design-extract` — URL → design tokens (colors, fonts, spacing, shadows) via `designlang`
- `amw-ui-ux-reasoning` — fallback reasoning library (161 rules, 67 UI styles, 161 palettes) when no context exists
- `amw-ascii-sketch` — Claude proposes 3 ASCII wireframe variants before committing to HTML, so the user picks direction cheaply

**Process (structure the work):**
- `amw-ux-designer` — UX methodology (research → strategy → wireframe → visual → handoff)
- `amw-ux-flows` — PRD → use cases → Mermaid diagrams → clickable HTML wireframes
- `amw-ux-evaluator` — systematic UX evaluation (Position, Visual Weight, Spacing)

**Output (render the chosen direction):**
- `amw-ascii-to-svg` — ASCII box-and-arrow diagram → clean SVG
- `amw-ascii-to-html` — ASCII wireframe → responsive HTML using starter-components
- `amw-diagram-svg` — natural language → SVG diagram primitives
- `amw-diagram-editorial` — natural language → HTML+SVG editorial diagrams
- `amw-diagram-architecture` — free text → graph JSON / Mermaid / SVG / PNG
- `amw-svg-creator` — icons, logos, technical SVG, animations *(gated; not characters/scenes)*
- `amw-infographics` — data + brief → dense editorial HTML + PNG + PDF
- `amw-pretext-art` — kinetic typography, text effects, text on paths
- `amw-hyperframes-bridge` — HTML composition → MP4 video

**Reference (documentation loaded on demand):**
- `amw-shadcn-ui` — complete shadcn/ui documentation (50+ components)
- `amw-tailwind-4` — Tailwind CSS v4 docs and migration guide
- `amw-seo` — SEO and Core Web Vitals evaluation framework

**Cross-format diagram toolchain (8 new skills, 2026-04-22):**
- `amw-diagram-formats` — meta-skill: authoritative reference library (IR schema, conversion matrix, format specs, diff algorithm, validation dispatcher). Never emits diagrams; all diagram skills reference it.
- `amw-html-diagram` — author or edit HTML-rendered editorial/infographic-style diagrams
- `amw-svg-diagram` — author or edit standalone SVG diagrams (freeform or layered architecture)
- `amw-mermaid-diagram` — author or edit Mermaid source text for all 9 grammar types; delegates rendering to `amw-mermaid-render`
- `amw-diagram-convert` — cross-format conversion across the full 5-format matrix (ASCII/HTML/SVG/Mermaid → any; PNG is output-only)
- `amw-diagram-compare` — IR-level structural diff between two diagrams (source formats may differ)
- `amw-webpage-to-diagram` — extract a diagram from a URL or local HTML file. **Structural** mode: HTML5 landmarks → IR → ASCII/SVG/Mermaid. **Spatial** mode: rendered-DOM geometry → box-drawing ASCII wireframe (agent-facing plan-phase tool for cheap pre-design iteration)
- `amw-diagram-webpage-sync` — reverse leg: take an edited diagram and regenerate the target webpage from it

**React-component reference skills (5 new, MIT, 2026-05-24):**
- `amw-react-colorful` — `react-colorful` tiny dependency-free color-picker component (Hex/Rgba/Hsl pickers + HexColorInput)
- `amw-progressive-blur` — `progressive-blur` gradient backdrop blur for React (radial + linear)
- `amw-hypercomp` — `hypercomp` TypeScript image-processing API that compiles to SVG filters
- `amw-vecui` — `vecui` immutable vec2/rect math for JS-driven animated layouts
- `amw-react-promptify` — `react-promptify` async, promise-based custom prompt/dialog modals

## Shared `bin/` scripts

Scripts shared across skills live in `bin/` rather than being duplicated per-skill:

- `amw-svg-render.py` — render SVG → PNG for visual-verify loops (amw-svg-creator, amw-ascii-to-svg, amw-diagram-editorial)
- `amw-html-export.py` — render HTML → PNG/PDF via Playwright (amw-infographics, amw-hyperframes-bridge)
- `amw-preview-server.py` — local HTTP server for multi-variant live preview
- `amw-ascii-parse.py` — Unicode box-drawing → node/edge graph (amw-ascii-to-svg, amw-ascii-to-html)
- `amw-page-to-ascii-layout.py` — rendered-DOM geometry → box-drawing ASCII spatial wireframe (amw-webpage-to-diagram spatial mode; self-validates via amw-validate-ascii.py)
- `amw-designlang-wrapper.sh`, `amw-dev-browser-wrapper.sh` — plugin-standard arg wrappers over external CLIs

## Slash commands

**Install and diagnose:**

| Command | Purpose |
|---|---|
| `/amw-init` | Install all runtime dependencies (dev-browser, Playwright, CairoSVG, Bun, ffmpeg) |
| `/amw-doctor` | Report which dependencies are missing |

**Plan phase (ASCII-first):**

| Command | Purpose |
|---|---|
| `/amw-sketch <intent>` | 3 ASCII wireframe variants, cheap, no HTML written |
| `/amw-extract-style <url>` | Live URL → design tokens via dev-browser + design-extract |
| `/amw-preview [file.html]` | Open HTML in dev-browser, take screenshot |
| `/amw-eval [file.html]` | Run ux-evaluator against current design |

**Authoring per format:**

| Command | Purpose |
|---|---|
| `/amw-ascii-to-svg <input>` | Parse ASCII diagram → render clean SVG |
| `/amw-ascii-to-html <input>` | Parse ASCII wireframe → render responsive HTML |
| `/amw-create-or-modify-ascii-diagram` | Create or edit an ASCII diagram (flowchart / table / arch / sequence) |
| `/amw-create-or-modify-html-diagram` | Create or edit an HTML-rendered editorial/infographic diagram |
| `/amw-create-or-modify-svg-diagram` | Create or edit a standalone SVG diagram |
| `/amw-create-or-modify-mermaid-diagram` | Create or edit Mermaid source text (all 9 grammar types) |
| `/amw-create-excalidraw-like-diagram-png` | Hand-drawn Excalidraw-style PNG via Gemini API (gated: `$GEMINI_API_KEY`) |

**Cross-format operations:**

| Command | Purpose |
|---|---|
| `/amw-convert-any-diagram-format` | Convert a diagram between any two formats (ASCII/HTML/SVG/Mermaid → any; PNG output-only) |
| `/amw-validate-any-diagram-format` | Validate any diagram file against its format spec |
| `/amw-compare-diagrams` | IR-level structural diff between two diagrams (formats may differ) |

**Webpage round-trip:**

| Command | Purpose |
|---|---|
| `/amw-create-diagram-from-webpage` | Extract a structural diagram from a URL or local HTML file |
| `/amw-create-webpage-from-diagram` | Generate a new webpage from a diagram (ASCII/SVG/Mermaid) |
| `/amw-modify-webpage-from-diagram` | Regenerate an existing webpage from an edited diagram |
| `/amw-modify-diagram-of-webpage` | Full round-trip: extract diagram, edit it, sync changes back into the page |

## Quick start

```bash
# 1. Install the plugin (once the marketplace is live)
/plugin install ai-maestro-webdesign@Emasoft/ai-maestro-plugins

# 2. Install runtime dependencies
/amw-init

# 3. Verify environment
/amw-doctor

# 4. Try the sketch workflow
/amw-sketch dashboard for a devtools team
```

## Non-goals

- **No Chrome DevTools MCP, no Playwright MCP for interactive automation.** `amw-dev-browser` is the only browser-automation primitive for input workflows. The rendering skills still use Playwright/Puppeteer internally for their output pipelines — that is output emission, not interactive automation.
- **No AI-drawn character illustrations.** `amw-svg-creator` is gated to icons, logos, technical diagrams, patterns, and animations. Character and scene illustration goes through real-asset or placeholder workflows instead — see the orchestrator's AI-slop rule #3.
- **No Framer Motion or GSAP for animation.** Starter components use a 50-LOC timeline engine; Popmotion is the only approved library fallback.
- **No automated test suite.** Verification is behavioral — each phase has acceptance scenarios.

## Build status

This plugin is being built in small, verified phases. Current state is recorded in `CLAUDE.md` and in `docs_dev/` build logs.

## License

MIT. Each integrated skill preserves its original LICENSE file under `skills/amw-<name>/LICENSE`.

## Acknowledgments

This plugin is MIT-licensed and contains no proprietary or commercial code. It builds on the following open-source work:

**Vendored rendering backend** — `external/mermaid-render/` is owned first-party MIT code that wraps:

- [beautiful-mermaid](https://www.npmjs.com/package/beautiful-mermaid) (MIT) — the Mermaid → themed-SVG / ASCII rendering engine.
- [@dagrejs/dagre](https://github.com/dagrejs/dagre) (MIT) — directed-graph layout (transitive dependency of beautiful-mermaid).
- Its wrapper scripts derive from three upstream MIT-licensed Claude-skill repositories (beautiful-mermaid, pretty-mermaid, agent-skill-diagramming-flows); see `external/mermaid-render/LICENSE`.

**Other vendored / adapted material** retains its upstream license:

- `external/hyperframes/` — vendored git submodule; **hyperframes' own code is Apache-2.0** (see `external/hyperframes/LICENSE`). **Transitive-dependency disclosure:** its `@hyperframes/player` package depends on **GSAP** (`gsap@3.15.0` — free *core* only; **no** paid `@gsap/*` club plugins), because a hyperframes composition *is* a paused GSAP timeline. GSAP is distributed under GreenSock's own "no-charge" license — free of charge, but **not** an OSI-approved open-source license like MIT/Apache (confirm the exact `gsap@3.15.0` terms pre-publish). GSAP appears **only** in the HTML→MP4 video path; webpage output still follows the plugin's no-GSAP rule, and the bridge itself adds no GSAP dependency. Whether this free-but-non-OSI dependency is acceptable for shipping is a **pre-publish licensing decision** (see below).
- `skills/amw-shadcn-ui/docs/` — shadcn/ui reference docs imported verbatim from <https://ui.shadcn.com/>.
- Per-skill originals preserved under `skills/amw-<name>/LICENSE`.

> A complete license inventory and full attribution roll-up is a pre-publish task (tracked separately); this section is the verified core, not the final compilation.
