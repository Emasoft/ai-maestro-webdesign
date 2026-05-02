# Pivot formats — the three modular intermediates

The plugin's modularity (any agent can pick up an artifact at any pipeline stage) rests on **three standardized pivot formats**. Every other skill is a parser, emitter, or transformer that reads or writes one of these three. This is what lets agents recombine recipes freely instead of getting locked into a single skill chain.

This document is the canonical inventory. When adding a fourth pivot, register it here.

---

## 1. ASCII (chat-native plan-phase pivot)

**Schema:** plain text, validated by `bin/amw-validate-ascii.py` (Python). Maximum 78 columns, ASCII-7 (no wide characters, no emojis), aligned box edges (`│ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼` for unicode-rounded variant; `+ - |` for classic). The renderer companion is `bin/amw-ascii-render.py` (JSON → ASCII, four modes: diagram / table / layers / sequence).

**Producers:**
- `amw-ascii-sketch` (3-variant plan-phase loop)
- `amw-ascii-creator` (single-artifact author)
- `amw-text-visual-{arch,state,workflows,cheatsheets,retro}` (5 archetype skills)
- `amw-box-diagram` (rounded-corner pipeline charts)
- `amw-ascii-diagrams-reference` (CHI'24 archetype reference library)

**Consumers:**
- `amw-ascii-to-html` (ASCII → responsive HTML — primary downstream)
- `amw-ascii-to-svg` (DEPRECATED — superseded by `amw-diagram-convert`)
- `amw-diagram-convert` (cross-format dispatch via the IR pivot)
- Any agent that needs a low-fi mockup as input to Phase B

**Why ASCII as a pivot:**
- Cost — ~1% of the tokens HTML iteration would consume; lets users iterate 10+ revisions cheaply
- Synchronous — chat-only during the loop, no file writes, no `amw-dev-browser` round-trips
- Lossless — the validator's pixel-perfect alignment guarantee means downstream HTML conversion never reinterprets the structure

**Mandatory gate:** every ASCII emitted by any skill MUST pass `bin/amw-validate-ascii.py` before being shown to the user. The validator catches what LLMs cannot count: column drift, nested-box corner misalignment, vertical pipe drift, wide-char leak, forbidden chars (`▼ ▲ ⟶ ⇒`).

---

## 2. DESIGN.md (design-system pivot)

**Schema:** Variant 1 (canonical, `@google/design.md`) — YAML frontmatter + 8 mandatory sections. Validated by `bin/amw-design-md-lint.sh` (lint gate) and `bin/amw-design-md-contrast.py` (WCAG-AA pair-level contrast on every color pair).

**Producers:**
- `amw-design-md-author-agent` (interactive 5-Q author from a brief)
- `amw-design-md-extractor-agent` (URL → DESIGN.md via `bin/amw-design-md-from-url.sh`; Tailwind config → DESIGN.md via `bin/amw-design-md-from-tailwind.mjs`; codebase scan → DESIGN.md via `bin/amw-design-md-from-codebase.py`)
- `amw-component-library-architect-agent` (token authoring + variant matrix)
- `amw-design-extract` (looser-format URL → token JSON; can be promoted to DESIGN.md by the extractor agent)

**Consumers:**
- `amw-wireframe-builder-agent` (consumes tokens for HTML rendering)
- `amw-design-md-emit-companions.py` (derives `tokens.css` / `tokens.json` / `component-inventory.md` / `usage-prompt.md` from DESIGN.md)
- `amw-component-library-architect-agent` (round-trip: also a producer)
- Style Dictionary / Figma-tokens export pipelines (downstream of `emit-companions`)

**Why DESIGN.md as a pivot:**
- Single source of truth — design tokens live ONCE in DESIGN.md; every consumer derives its representation (CSS variables, JSON, Figma format) from the same source
- Auditable — `amw-design-md-auditor-agent` runs a 5-pass audit (structural / drift / a11y / completeness / consistency); the lint gate catches drift before it propagates
- Tooled — `@google/design.md` provides linting + diffing; the plugin extends with WCAG contrast and Tailwind extraction

---

## 3. Diagram IR (`diagram-ir/1.0`) (cross-format diagram pivot)

**Schema:** JSON schema documented in `skills/amw-diagram-formats/references/ir-schema.md`. Common-denominator graph representation: nodes (with layout hints, style), edges (with labels, arrowheads), and clusters (for layered architecture). Validated by `bin/amw-diagram-ir.py --validate`.

**Producers (parsers — emit IR):**
- `bin/amw-parse-html-diagram.py` (HTML diagram → IR)
- `bin/amw-parse-svg-diagram.py` (SVG diagram → IR)
- `bin/amw-parse-mermaid-diagram.py` (Mermaid → IR)
- `bin/amw-dom-to-ir.py` (HTML DOM landmarks → IR; for `amw-webpage-to-diagram`)
- `bin/amw-diagram-ir.py` (ASCII → IR via the renderer)

**Consumers (emitters — consume IR):**
- ASCII emitter (within `amw-diagram-ir.py`)
- HTML emitter (consumed by `amw-html-diagram`)
- SVG emitter (consumed by `amw-svg-diagram`, `amw-diagram-svg`, `amw-diagram-architecture`)
- Mermaid emitter (consumed by `amw-mermaid-diagram`, then rendered via `amw-mermaid-render`)

**PNG is output-only** — there is no `bin/amw-parse-png-diagram.py`. Any skill that would need to read a PNG refuses the request and explains why.

**Why IR as a pivot:**
- Decouples N parsers from N emitters: `N + N` implementations instead of `N²` cross-format converters
- Lets `amw-diagram-compare` do structural diffs across formats (the diff is at the IR level, so comparing an ASCII diagram to a Mermaid diagram is sensible)
- Lets `amw-diagram-webpage-sync` round-trip: edited diagram → IR → re-emit target webpage with structural changes preserved

---

## How agents pick the right pivot

The pipeline-stage → pivot mapping is:

| Pipeline stage | Pivot used | Why |
|---|---|---|
| Survey (extract design tokens from URL) | DESIGN.md | Standardizes token shape so wireframe-builder doesn't need URL-specific code paths |
| Concepts (low-fi sketches) | ASCII | Cheap, chat-native, lossless under the validator gate |
| Design / Style (component tokens) | DESIGN.md | One source of truth, derives CSS / JSON / Figma format on demand |
| Mockup / Render (any diagram) | Diagram IR | Cross-format conversion + structural diff + webpage round-trip |
| Prototype (working HTML) | DESIGN.md tokens consumed by HTML | Single token bundle drives every rendered surface |
| Implementation | DESIGN.md tokens exported via emit-companions | Style Dictionary / Figma tokens are mechanical derivations |
| Testing | (no pivot — `amw-dev-browser` is the input primitive) | Browser is observation, not authoring |

When writing a new skill, ask: which pivot does it produce or consume? If neither, the skill is probably either a leaf (terminal output, like `amw-hyperframes-bridge` for MP4) or a dispatcher (routes to other skills, like `amw-html-diagram`). If it's neither leaf nor dispatcher AND doesn't fit the three pivots, you're probably about to invent a fourth pivot — register it here first, and confirm with the orchestrator that it's worth the modularity cost.

---

## Adding a fourth pivot

A pivot earns its place only if it would otherwise force `N²` integrations. Before adding a fourth:

1. **Count the integrations** — list every producer and every consumer of the candidate format. If the cardinality is `M producers × N consumers ≤ M + N`, you don't need a pivot; just write the direct integrations.
2. **Standardize the schema** — write a `references/<format>-schema.md` and a `bin/amw-<format>-validate.py` (or equivalent). Without a schema, the pivot is just "another format."
3. **Provide both directions** — write at least one producer AND one consumer. A producer-only pivot is a dead end; a consumer-only pivot is unreachable.
4. **Update this document** — add the pivot to the table above with its schema, producers, consumers, and "why it's a pivot."
5. **Update the orchestrator's SKILL.md** to mention the new pivot in the modular-architecture section.

Pivot proliferation is a smell. Three is the right number for a multi-skill orchestrator-shaped plugin of this size; a fourth pivot should be a deliberate decision, not an accident.
