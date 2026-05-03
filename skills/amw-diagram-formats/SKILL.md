---
name: amw-diagram-formats
description: Look up the authoritative spec for ASCII / HTML / SVG / Mermaid diagram formats, the plugin's IR schema, the cross-format conversion matrix, the validation dispatcher, or the modify / diff pipelines. Triggers on narrow technical intents only — "what does the IR schema look like", "how does format detection work", "conversion matrix for ASCII to SVG", "IR-level diff algorithm", "validation dispatcher contract", "Mermaid format spec". Does NOT trigger on generic design / diagram creation intent — those belong to ascii-creator / svg-diagram / html-diagram / mermaid-diagram. This is a references-only meta-skill; it NEVER emits diagrams itself. Use when looking up the IR schema, format specs, conversion matrix, or validation contracts for diagrams. No slash-command trigger — this skill is consumed by other skills via file-read only (e.g., amw-diagram-convert reads the IR schema from this skill's references/ before dispatching its conversion).
version: 0.1.0
---

# Diagram Formats — shared reference library

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Consumer scope:** every other diagram skill and every `wd-*-diagram*` command pulls its format / IR / conversion / validation rules from this meta-skill. Do NOT re-author these specs inside the consumer skills — they cross-reference this library.

## Overview

Shared reference library for all diagram format specifications in the plugin. Owns the canonical prose and machine-readable schema for ASCII / HTML / SVG / Mermaid / PNG format specs, the plugin IR (Intermediate Representation) schema, the N×N conversion matrix, the detect → parse → IR-patch → re-render → re-validate pipeline, the IR-level structural diff algorithm, and the unified validator output contract. This is a documentation meta-skill — it NEVER emits diagrams.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. It is a **reference-only meta-skill** that is never invoked directly by users. Every other diagram skill and every `wd-*-diagram*` command reads its format specs, IR schema, and conversion rules from here. The `design-principles` orchestrator routes here only when a user explicitly asks about format internals (`"what's the IR schema"`, `"conversion matrix"`).


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Older direct-emitter cluster vs newer thin-dispatcher cluster

The plugin ships diagram authoring on two parallel surfaces:

| Layer | Skills | LOC (~combined) | When to read |
|---|---|---|---|
| Newer thin dispatchers (entry points) | `amw-html-diagram`, `amw-svg-diagram` | ~204 | When routing via `/amw-create-or-modify-html-diagram` / `/amw-create-or-modify-svg-diagram` slash commands; when authoring through the IR-pivot path |
| Older direct emitters (implementation) | `amw-diagram-editorial`, `amw-diagram-svg`, `amw-diagram-architecture` | ~1207 | When authoring deeply (custom HTML or SVG layout); the dispatchers internally delegate here |

The thin dispatchers are the **public entry surface**. They handle command-mode dispatch, format-detection routing, and IR-pivot conversion. They internally delegate the actual emission to the older direct-emitter skills.

**When in doubt, route via the dispatcher.** When authoring deeply (e.g., needing a non-default HTML layout, custom Mermaid grammar, freeform SVG arrangement), read the underlying older skill directly.

A future consolidation may fold the older 3 skills' SKILL.md bodies into the dispatcher's `references/` and reduce the surface from 6 skills to 3, but the current bilayered architecture is intentional: the dispatchers are stable contract surfaces and the emitters are heavier implementation that benefits from being callable as standalone skills via slash commands (`/amw-create-or-modify-architecture-diagram` etc.).

## Position in flow

REFERENCE ONLY. This skill owns the canonical prose + machine-readable schema for every diagram-format concern in the plugin:

- Format-specific specs (syntax, validation rules, emit pipelines).
- The plugin's IR (Intermediate Representation) — the pivot format for cross-format conversion.
- The N×N conversion matrix across `ascii | html | svg | mermaid | png`.
- The shared detect → parse → IR-patch → re-render → re-validate pipeline used by every `wd-create-or-modify-*-diagram` command.
- The IR-level structural diff algorithm used by `/amw-compare-diagrams`.
- The unified validator output contract: `PASS | FAIL: <line>: <message> [FIX: <hint>]`.

When a consumer skill or command needs any of these, it references this library rather than duplicating the spec inline. If the spec changes, only files under `skills/amw-diagram-formats/references/` change — every consumer picks up the update via cross-reference.

## Trigger conditions

- "what's the IR schema / IR version / IR fields"
- "IR schema version 1.0 spec" / "diagram-ir version 1.0"
- "how does format detection decide between ascii and mermaid"
- "conversion matrix — ASCII to SVG / HTML to PNG / PNG as source"
- "validator output format / PASS-FAIL contract / FIX hint format"
- "modify-flow steps / detect-parse-patch-emit-validate"
- "structural IR diff algorithm / ir-diff patch ops"
- "authoritative spec for ASCII / HTML / SVG / Mermaid / PNG in this plugin"

Do NOT activate for:

- Creating or modifying a specific diagram (→ `../amw-ascii-creator/`, `../amw-svg-diagram/`, `../amw-html-diagram/`, `../amw-mermaid-diagram/`)
- Converting formats (→ `../amw-diagram-convert/` + `/amw-convert-any-diagram-format`)
- Validating a specific file (→ `../amw-ascii-validator/` + `/amw-validate-any-diagram-format`)
- Comparing diagrams (→ `../amw-diagram-compare/` + `/amw-compare-diagrams`)

This skill answers *"what is the spec"* — the others DO things based on that spec.

## Reference index

Every entry below is an authoritative, hand-maintained source. Consumer skills and commands MUST cross-reference these paths, not re-author the content.

| File | Scope | Consumers |
|---|---|---|
| [ascii](./references/ascii.md) | ASCII format spec — syntax, parse, emit, validate, techniques. Authored by the sibling `format-refs` agent. | `ascii-creator`, `ascii-validator`, `ascii-sketch`, `ascii-to-html`, `ascii-to-svg`, `/amw-ascii-to-html`, `/amw-ascii-to-svg` |
| [html](./references/html.md) | HTML+inline-SVG format spec — starter-components, AI-slop gate, Tweaks invariants, React/Babel pins, ARIA/a11y. Authored by the sibling `format-refs` agent. | `html-diagram`, `diagram-editorial`, `infographics`, `/amw-create-or-modify-html-diagram` |
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
| [svg](./references/svg.md) | Standalone SVG format spec — primitives, viewport, text, cairosvg path. Authored by the sibling `format-refs` agent. | `svg-diagram`, `svg-creator`, `diagram-svg`, `diagram-architecture`, `/amw-create-or-modify-svg-diagram` |
> [svg.md] Format definition · Structural primitives (diagram-grade usage) · Viewport rules · Text rendering rules · Rasterization path · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · SKILL · SKILL · SKILL · SKILL · SKILL · advanced-techniques · `../../bin/amw-svg-render.py` — render-verify-finish loop (`render` / `finish` / `status` / `reset`) · ir-schema · conversion-matrix · png · validation-dispatcher
| [mermaid](./references/mermaid.md) | Mermaid grammar subset, themes, mmdc flags, SVG/PNG/ASCII output paths. Authored by the sibling `format-refs` agent. | `mermaid-diagram`, `mermaid-render`, `diagram-architecture`, `/amw-create-or-modify-mermaid-diagram` |
> [mermaid.md] Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
| [png](./references/png.md) | PNG as OUTPUT TARGET only — rasterize pipelines per source format. PNG as SOURCE is `impossible` per user directive. Authored by the sibling `format-refs` agent. | `excalidraw-illustrations`, `infographics`, `hyperframes-bridge`, `/amw-create-excalidraw-like-diagram-png` |
> [png.md] PNG is OUTPUT-ONLY — why · 1 Refusal messages (verbatim) · Rasterization pipelines (per source format → PNG) · 1 SVG → PNG (via cairosvg) · 2 HTML → PNG (via Playwright screenshot) · 3 ASCII → PNG (two-step: ASCII → SVG → PNG) · 4 Mermaid → PNG (direct via `mmdc -t png` OR via SVG) · 5 Hand-drawn-style PNG (via `excalidraw-illustrations`) · Refusal path implementation · 1 `bin/amw-diagram-detect-format.sh` · 2 `bin/amw-validate-diagram.sh` — PNG branch · 3 Conversion dispatcher · Per-source technique catalog · S1 — bin/amw-svg-render.py + cairosvg · S2 — bin/amw-html-export.py + Playwright · S3 — bin/amw-mermaid-render.sh + beautiful-mermaid + mmdc · S4 — Hand-drawn (excalidraw-illustrations) · PNG as INPUT is refused — the full story · 1 Format detection (`bin/amw-diagram-detect-format.sh`) · 2 Per-command refusal · 3 No OCR, no vision-model retry · Failure modes · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG via Playwright screenshot · `../../bin/amw-svg-render.py` — SVG → PNG via cairosvg · `../../bin/amw-mermaid-render.sh` — Mermaid → SVG then → PNG · `../../bin/amw-validate-diagram.sh` (planned; Task 0c) — unified validator dispatcher, PNG branch = hardcoded refusal · conversion-matrix · …(+1)
| [ir-schema](./references/ir-schema.md) | IR JSON schema in prose + examples + lossy-conversion table per format. | `diagram-ir.py`, every `wd-*-diagram*` command, every parser in `bin/` |
| [conversion-matrix](./references/conversion-matrix.md) | Canonical N×N table. PNG-input cells = `impossible`. Every dispatch rule for `/amw-convert-any-diagram-format`. | `diagram-convert`, `/amw-convert-any-diagram-format`, `/amw-create-webpage-from-diagram` |
| [modify-flow](./references/modify-flow.md) | Shared detect → parse → IR-patch → re-render → re-validate pipeline. | All 4 `wd-create-or-modify-*-diagram` commands; `diagram-webpage-sync` |
| [diff-algorithm](./references/diff-algorithm.md) | IR-level structural diff algorithm (node-id match, edge set diff, markdown report). | `diagram-compare`, `/amw-compare-diagrams`, `bin/amw-diagram-ir.py --diff` |
> [diff-algorithm.md] Inputs · Output: ordered list of patch ops · Node / edge matching · Deep object equality for `change-*` · Markdown report format · Id normalization (caller preprocessing) · Exit codes (CLI) · Known limitations · Visual mode (optional, future) · Related references
| [detect-format](./references/detect-format.md) | Format detection decision tree (magic lines, extensions, content sniffing). | `bin/amw-diagram-detect-format.sh`, every dispatcher |
| [validation-dispatcher](./references/validation-dispatcher.md) | Unified `PASS \| FAIL: <line>: <message> [FIX: <hint>]` output contract. | `ascii-validator`, `/amw-validate-any-diagram-format`, every per-format validator wrapper |
| `./schema.json` | Machine-readable JSON Schema (draft-07) for the IR. Consumed by `bin/amw-diagram-ir.py`. | `bin/amw-diagram-ir.py validate`, any JSON-schema-aware tooling |

## Backing scripts (cross-reference only)

These live in `bin/`, not in this skill. The skill documents them; it does not own them.

- `bin/amw-diagram-ir.py` — parse / emit / validate / diff the IR (see [ir-schema](./references/ir-schema.md)).
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- `bin/amw-diagram-detect-format.sh` — sniffs format; see [detect-format](./references/detect-format.md).
  > Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this
- `bin/amw-validate-diagram.sh` — top-level validator dispatcher; see [validation-dispatcher](./references/validation-dispatcher.md).
  > Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · 1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback) · 2 SVG — `bin/amw-validate-svg-diagram.sh` · 3 HTML — `bin/amw-validate-html-diagram.sh` · 4 Mermaid — `bin/amw-mermaid-lint.sh` · Caller integration patterns · 1 Post-create gate · 2 Post-convert gate · 3 Modify-flow loop · 4 Multi-format mode (ascii-validator) · Known limitations (Phase 0) · Related references
- `bin/amw-validate-html-diagram.sh`, `bin/amw-validate-svg-diagram.sh`, `bin/amw-mermaid-lint.sh` — per-format validator wrappers (see the corresponding references/*.md).
- `bin/amw-validate-ascii.py`, `bin/amw-validate-ascii.py` — ASCII validators; the contract lines up with the unified output format. See [SKILL](../amw-ascii-validator/SKILL.md).

## Locked decisions (do not re-litigate)

Per user directive 2026-04-22:

- **IR version is diagram-ir version 1.0 (schema ID `<diagram-ir/1.0>`).** Schema evolution requires an ADR and a bump — NOT in scope for Phase 0.
- **PNG is OUTPUT-ONLY.** Every PNG-as-SOURCE conversion cell is `impossible`; the validator dispatcher refuses PNG inputs with a fixed message.
- **Mermaid backend is `mmdc`** (no Kroki).
- **SVG validator is `xmllint --noout`** (no `svg-validator` npm wrapper).
- **HTML validator is `xmllint --html` + `tidy -e -q -errors`** (when available).
- **Round-trip path** (for `/amw-create-webpage-from-diagram`) goes via IR → ASCII → HTML until a dedicated direct pipeline is justified.
- **Task 4d (selector-aware webpage ↔ diagram sync)** is MVP read-only — extract only; sync-back is future work.

## Instructions

1. Use this skill as a reference library only — it emits no artifacts and runs no transformations.
2. Locate the needed file using the Reference index table: format spec, IR schema, conversion matrix, detect-format contract, validation dispatcher, modify-flow, or diff algorithm.
3. Reference files via relative paths (`../amw-diagram-formats/references/<name>.md`); never copy the prose inline into other skills.
4. Before performing any cross-format operation, check the conversion matrix at [conversion-matrix](references/conversion-matrix.md) for the correct cell type (`direct`, `via IR`, `via X`, `wrap`, or `impossible`).
  > Full N×N table · Cell semantics · PNG-as-source refusal (mandatory) · PNG-as-target pipelines (all supported) · Dispatch algorithm · Per-cell implementation notes · Tools index (required backends) · Related references · ascii · html · svg · mermaid · png
5. Consult `<references/locked-decisions.md>` for immutable rules established by user directive; do not override these decisions.

Consumers reference this library via relative paths (`../amw-diagram-formats/references/<name>.md`). Never copy the prose inline. Use the Reference index table to find the right file for each concern (format spec, IR schema, conversion matrix, etc.). See `## Locked decisions` for immutable rules established by user directive.

## Output

This skill produces no artifacts. It answers lookup questions against the references only and returns the content of the requested reference file.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Prerequisites

- **runtime_binaries:** none directly (this is a documentation skill). Consumer skills/scripts declare their own deps.
- **python_packages:** none.
- **cpan / npm:** none.

## Error Handling

On failure, the skill emits a non-zero exit code or returns a structured error in the response. Consumer skills handle errors per their own SKILL.md.

## Resources

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator; routes generic design intent to executor skills.
- [SKILL](../amw-ascii-creator/SKILL.md) — primary ASCII authoring skill; pulls [ascii](./references/ascii.md) + [modify-flow](./references/modify-flow.md).
  > [ascii.md] Format definition · Dimensional constraints · Parse rules · Emission rules · Validation rules · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · SKILL · SKILL · SKILL · SKILL · SKILL · SKILL · `../../text-visual-{workflows,arch,state,cheatsheets,retro}/SKILL.md` — specialized ASCII archetypes · `../../bin/amw-ascii-parse.py` — tokenizer (IR input) · `../../bin/amw-ascii-render.py` — renderer (4 JSON modes) · `../../bin/amw-validate-ascii.py` — validator (Perl, mandatory gate) · `../../bin/amw-validate-ascii.py` — validator (Python mirror) · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
  > [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [SKILL](../amw-ascii-validator/SKILL.md) — ASCII validator; pulls [validation-dispatcher](./references/validation-dispatcher.md).
  > [validation-dispatcher.md] Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · Caller integration patterns · Known limitations (Phase 0) · Related references
- [SKILL](../amw-ascii-sketch/SKILL.md) — plan-phase ASCII loop; pulls [ascii](./references/ascii.md).
  > [ascii.md] Format definition · Dimensional constraints · Parse rules · Emission rules · Validation rules · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · SKILL · SKILL · SKILL · SKILL · SKILL · SKILL · `../../text-visual-{workflows,arch,state,cheatsheets,retro}/SKILL.md` — specialized ASCII archetypes · `../../bin/amw-ascii-parse.py` — tokenizer (IR input) · `../../bin/amw-ascii-render.py` — renderer (4 JSON modes) · `../../bin/amw-validate-ascii.py` — validator (Perl, mandatory gate) · `../../bin/amw-validate-ascii.py` — validator (Python mirror) · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
- [SKILL](../amw-ascii-to-html/SKILL.md), [SKILL](../amw-ascii-to-svg/SKILL.md) — direct ASCII conversion skills.

## Non-negotiables

- This skill NEVER emits diagrams, files, or artifacts. It answers lookup questions against the references only.
- Consumer skills and commands MUST cross-reference this library via relative paths (`../amw-diagram-formats/references/<name>.md`). They MUST NOT copy the prose inline.
- The IR schema version is SINGLE-VALUE. No "legacy" or "compat" variants live alongside the canonical IR schema version 1.0.
- PNG-as-source is `impossible` in every dispatch table. Do not add a "fallback OCR" or "re-interpret" path.
