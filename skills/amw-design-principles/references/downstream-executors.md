# Downstream executor sub-skills — full routing table

Authoritative routing reference for the `amw-design-principles` orchestrator. The orchestrator invokes one of these sub-skills only when its specific technical trigger applies. Each sub-skill is independent and self-contained; the orchestrator passes context but never re-derives sub-skill rules.

## Input — gather context for Rule 1

| Sub-skill | Use when |
|---|---|
| `../amw-dev-browser/` | Need to screenshot, inspect DOM, or interact with a live page. Plugin's ONLY browser-automation primitive for input. |
| `../amw-design-extract/` | User points at a reference URL and wants its colors, fonts, spacing, and tokens extracted. Wraps `designlang`. |
| `../amw-ui-ux-reasoning/` | Last-resort fallback when the user has no design system and no reference — 161 reasoning rules + 67 styles + 161 palettes + 57 font pairings. |

Slash commands: `/amw-extract-style <url>` combines dev-browser + design-extract.

## Plan phase — satisfy Rule 2 in ASCII

| Sub-skill | Use when |
|---|---|
| `../amw-ascii-sketch/` | **Default for any webpage design.** Runs the ASCII iteration loop (3 variants → feedback → revision → ... → explicit satisfaction). |
| `../amw-ux-flows/` | Product already has a PRD and the user wants user-case extraction → Mermaid diagrams → clickable HTML wireframes. |
| `../amw-ux-designer/` | Need the full UX methodology — research, personas, IA, prototyping, handoff. |

Slash command: `/amw-sketch <intent>`.

## Output — render the approved direction

| Sub-skill | Use when |
|---|---|
| `../amw-ascii-creator/` | User already knows what they want — produce ONE validated perfect-ASCII artifact (flowchart, table, sequence, layered arch, or framed wireframe) in a single invocation. Mode A uses bin/amw-ascii-render.py; Mode B hand-authors and runs bin/amw-validate-ascii.py. |
| `../amw-ascii-validator/` | Validate hand-authored ASCII OR render perfect ASCII from structured JSON — the toolchain that enforces alignment across every ASCII emitter in this plugin. |
| `../amw-ascii-to-html/` | User approved an ASCII wireframe → generate responsive HTML using design-principles tokens + starter-components chrome. Consumes output from ascii-sketch (plan-phase) OR ascii-creator (single-artifact). |
| `../amw-ascii-to-svg/` | User has an ASCII box-and-arrow diagram → render clean SVG. Consumes output from ascii-creator Mode A. |
| `../amw-diagram-svg/` | Natural-language request → SVG diagram primitives. |
| `../amw-diagram-editorial/` | Editorial-quality HTML+SVG diagrams (13 types: architecture, flowchart, sequence, ER, timeline, etc.). |
| `../amw-diagram-architecture/` | Free-text system description → graph JSON / Mermaid / SVG / PNG. |
| `../amw-svg-creator/` | **Gated.** Icons, logos, technical SVG, patterns, animations. NOT characters or scenes. |
| `../amw-infographics/` | Data + brief → dense editorial HTML + PNG + PDF (175-design library). |
| `../amw-pretext/` | Pretext-driven typography, measurement, layout, obstacle routing, shrink-wrap, virtualized tables, kinetic text, calligrams, ASCII-on-canvas, and 3D text — ~78 techniques catalogued in `references/TECH-NN-*.md`. NOT a general typography system — orchestrator keeps "make the type nice" here. |
| `../amw-hyperframes-bridge/` | HTML composition → MP4 video. |
| `../amw-mermaid-render/` | Mermaid text → SVG or Unicode ASCII. Themed output, 15+ themes. Consumes structured Mermaid syntax; emits a self-contained SVG or a validator-passing ASCII block. |
| `../amw-box-diagram/` | Clean Unicode rounded-corner box diagrams for pipelines, fan-out/fan-in, workflow charts, layered stacks. Richer typography than plain ASCII; always validator-passing. |
| `../amw-excalidraw-illustrations/` | **Gated.** Hand-drawn Excalidraw-style conceptual illustrations via Gemini API. Educational/slides use only; requires `$GEMINI_API_KEY` and user-confirmed cost per call. Exception to the ai-slop ban on AI-drawn illustrations because scope is constrained (sketchy, white-bg, concept-diagram shape). |
| `../amw-html-diagram/` | Author or edit an HTML-rendered editorial/infographic-style diagram. Narrow trigger: "create HTML diagram", "modify HTML diagram at …", "/amw-create-or-modify-html-diagram". Thin dispatcher over `diagram-editorial` and `infographics`. |
| `../amw-svg-diagram/` | Author or edit a standalone SVG diagram. Narrow trigger: "create SVG diagram", "modify SVG diagram at …", "/amw-create-or-modify-svg-diagram". Thin dispatcher over `diagram-svg` and `diagram-architecture`. |
| `../amw-mermaid-diagram/` | Author or edit Mermaid source text (9 grammar types). Narrow trigger: "create Mermaid diagram", "modify Mermaid at …", "/amw-create-or-modify-mermaid-diagram". Rendering is delegated to `mermaid-render`. |
| `../amw-diagram-convert/` | Cross-format diagram conversion across the 5-format matrix (ASCII/HTML/SVG/Mermaid → any; PNG is output-only). Narrow trigger: "convert this diagram to X", "/amw-convert-any-diagram-format". |
| `../amw-diagram-compare/` | IR-level structural diff between two diagrams (formats may differ). Narrow trigger: "compare these diagrams", "diff two flowcharts", "/amw-compare-diagrams". |
| `../amw-webpage-to-diagram/` | Extract the structural diagram of a webpage (URL or local `.html`) and emit ASCII/SVG/Mermaid. Narrow trigger: "extract diagram from webpage", "diagram this URL", "/amw-create-diagram-from-webpage". |
| `../amw-diagram-webpage-sync/` | Re-emit an existing webpage from an edited diagram source. Narrow trigger: "sync this diagram back into my HTML", "/amw-modify-webpage-from-diagram". |

Slash commands: `/amw-ascii-to-html`, `/amw-ascii-to-svg`, `/amw-create-or-modify-ascii-diagram`, `/amw-create-or-modify-html-diagram`, `/amw-create-or-modify-svg-diagram`, `/amw-create-or-modify-mermaid-diagram`, `/amw-create-excalidraw-like-diagram-png`, `/amw-convert-any-diagram-format`, `/amw-validate-any-diagram-format`, `/amw-compare-diagrams`, `/amw-create-diagram-from-webpage`, `/amw-create-webpage-from-diagram`, `/amw-modify-webpage-from-diagram`, `/amw-modify-diagram-of-webpage`.

## Text visualization — ASCII artifacts for PRs, ADRs, terminals, and chat

These executors are distinct from the `diagram-*` skills above: they produce **monospaced ASCII only**, designed to paste unmodified into GitHub PRs, issue comments, Slack, Notion, READMEs, ADRs, and terminal output. They are not renderers to SVG or HTML — if the user wants pixels, run one of these first to approve the ASCII, then hand off to `../amw-ascii-to-svg/` or `../amw-ascii-to-html/`. Every artifact these skills emit passes `../../bin/amw-validate-ascii.py` before delivery (LLMs cannot count monospace columns reliably — the validator is how the plugin compensates).

| Sub-skill | Use when |
|---|---|
| `../amw-text-visual-workflows/` | Multi-step workflow as ASCII flowchart, timeline, or swimlane (PR lifecycle, launch plan, triage ops). |
| `../amw-text-visual-arch/` | Layered ASCII architecture diagram (context / container / component) for terminals, PRs, ADRs. |
| `../amw-text-visual-state/` | ASCII state machine for user journey, retention loop, issue lifecycle, experiment status. |
| `../amw-text-visual-cheatsheets/` | ASCII CLI command panel with macOS/Linux and Windows columns side by side. |
| `../amw-text-visual-retro/` | ASCII retrospective grid, milestone timeline, or heatmap for retros, post-mortems, experiment readouts. |

These skills do NOT ship dedicated slash commands (text-visual output overlaps heavily with `/amw-sketch` and `/amw-ascii-to-svg`; a separate command would confuse routing). Invoke via direct skill activation (narrow trigger phrases listed in each skill's description) or via `/amw-sketch` when in the plan phase.

## Validation + reference

| Sub-skill | Use when |
|---|---|
| `../amw-ux-evaluator/` | Systematic UX scoring (Position / Visual Weight / Spacing) on a finished page. |
| `../amw-seo/` | Performance / Core Web Vitals evaluation framework. |
| `../amw-shadcn-ui/` | Need to emit copy-paste shadcn/ui components. |
| `../amw-tailwind-4/` | Tailwind v4 config / migration questions. |
| `../amw-ascii-diagrams-reference/` | Reference library of validated ASCII archetypes (flowcharts, state-machines, trees, data-structures, network-topology, sequences-tables, graphs-annotations) distilled from the CHI'24 paper on 2,156 real diagrams in Linux/Chromium/LLVM/TensorFlow. Consulted by ascii-sketch / ascii-creator / text-visual-* when selecting a canonical pattern. |
| `../amw-diagram-formats/` | **Meta-skill (cross-reference, not executor).** Authoritative specs for every diagram-format concern: format specs (ASCII/HTML/SVG/Mermaid), the IR schema (diagram-ir version 1.0), the N×N conversion matrix, the format-detection contract, the validate-dispatcher, the modify-flow pipeline, and the IR-level diff algorithm. All diagram-authoring and diagram-conversion skills import their rules from here — do NOT re-author these specs in the consumer skills. Never triggers independently; consulted implicitly whenever a diagram skill needs a spec. |
| [project-output-routing](./project-output-routing.md) | Detection rules for project-inferred artifact output paths. Every sub-skill references this before writing artifacts instead of hardcoding `/tmp/amw-<skill>/`. Consult when the user has not specified an output path. |
| [pivot-formats](./pivot-formats.md) | The plugin's three modular pivot formats (ASCII / DESIGN.md / Diagram-IR), the producers and consumers of each, and how agents pick the right pivot for each pipeline stage. Read before adding a new skill that produces or consumes structured intermediate output. |

Slash commands: `/amw-eval`, `/amw-preview`, `/amw-doctor`, `/amw-init`.

## Tier-4 specialists (on-demand, Phase B only)

`amw-form-designer-agent`, `amw-email-designer-agent`, `amw-motion-designer-agent`, and `amw-component-library-architect-agent` are spawned by `ai-maestro-webdesign-main-agent` when the brief surfaces form / email / motion / token-system intent. They have no veto power and produce specs or exports consumed by Tier-3 producers. They are agents, not skills — invoke them via Task delegation, not skill activation. Full roster and delegation rules live in the plugin's `agents/ai-maestro-webdesign-main-agent.md` and [two-mode-workflow](./two-mode-workflow.md).
