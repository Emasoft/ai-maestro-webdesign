---
name: amw-diagram-formats
description: Authoritative spec for ASCII / HTML / SVG / Mermaid formats, IR schema, conversion matrix, validation dispatcher, modify/diff pipelines. Triggers on "diagram IR schema", "format detection", "conversion matrix", "IR-level diff", "Mermaid format spec". Does NOT trigger on diagram creation — routes to ascii-creator / svg-diagram / html-diagram. References-only — NEVER emits diagrams. Use when looking up IR schema or format specs. Trigger with "diagram IR schema".
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

## Reference index (summary)

| Concern | Reference file |
|---|---|
| ASCII / HTML / SVG / Mermaid / PNG format specs | [ascii](./references/ascii.md), [html](./references/html.md), [svg](./references/svg.md), [mermaid](./references/mermaid.md), [png](./references/png.md) |
| IR JSON schema in prose + examples | [ir-schema](./references/ir-schema.md) |
| N×N conversion matrix (PNG-input = `impossible`) | [conversion-matrix](./references/conversion-matrix.md) |
| Shared modify pipeline (detect → parse → IR-patch → re-render → re-validate) | [modify-flow](./references/modify-flow.md) |
| IR-level structural diff algorithm | [diff-algorithm](./references/diff-algorithm.md) |
| Format detection decision tree | [detect-format](./references/detect-format.md) |
| Unified validator output contract | [validation-dispatcher](./references/validation-dispatcher.md) |
| Machine-readable JSON Schema (draft-07) for the IR | `./schema.json` |
| Full consumer table + per-script TOCs + locked decisions | [skill-overview](./references/skill-overview.md) |

**See [skill-overview](./references/skill-overview.md) for the full reference index with per-file scope, consumer skills, and backing-script descriptions.**

## Backing scripts (cross-reference only)

These live in `bin/`, not in this skill. The skill documents them; it does not own them. See [skill-overview](./references/skill-overview.md) for the full per-script TOCs.

- `bin/amw-diagram-ir.py` — parse / emit / validate / diff the IR (see [ir-schema](./references/ir-schema.md)).
- `bin/amw-diagram-detect-format.sh` — sniffs format; see [detect-format](./references/detect-format.md).
- `bin/amw-validate-diagram.sh` — top-level validator dispatcher; see [validation-dispatcher](./references/validation-dispatcher.md).
- `bin/amw-validate-html-diagram.sh`, `bin/amw-validate-svg-diagram.sh`, `bin/amw-mermaid-lint.sh` — per-format validator wrappers (see the corresponding references/*.md).
- `bin/amw-validate-ascii.py` — ASCII validator; the contract lines up with the unified output format. See [SKILL](../amw-ascii-validator/SKILL.md).

## Locked decisions (do not re-litigate)

Full list with rationale: [skill-overview](./references/skill-overview.md) § Locked decisions.

Per user directive 2026-04-22 (summary):

- IR version is **diagram-ir version 1.0** — schema evolution requires an ADR + version bump.
- **PNG is OUTPUT-ONLY** — every PNG-as-SOURCE conversion cell is `impossible`.
- Mermaid backend is `mmdc` (no Kroki).
- SVG validator is `xmllint --noout`.
- HTML validator is `xmllint --html` + `tidy -e -q -errors` (when available).
- Round-trip path (for `/amw-create-webpage-from-diagram`) goes via IR → ASCII → HTML until a dedicated direct pipeline is justified.

## Instructions

1. Use this skill as a reference library only — it emits no artifacts and runs no transformations.
2. Locate the needed file using the Reference index table above: format spec, IR schema, conversion matrix, detect-format contract, validation dispatcher, modify-flow, or diff algorithm.
3. Reference files via relative paths (`../amw-diagram-formats/references/<name>.md`); never copy the prose inline into other skills.
4. Before performing any cross-format operation, check the conversion matrix at [conversion-matrix](references/conversion-matrix.md) for the correct cell type (`direct`, `via IR`, `via X`, `wrap`, or `impossible`).
5. Consult [skill-overview](./references/skill-overview.md) § Locked decisions for immutable rules established by user directive; do not override these decisions.

Consumers reference this library via relative paths (`../amw-diagram-formats/references/<name>.md`). Never copy the prose inline.

## Output

This skill produces no artifacts. It answers lookup questions against the references only and returns the content of the requested reference file.

## Examples

See the worked examples in the per-mode sub-sections above and in `references/`.

## Prerequisites

- **runtime_binaries:** none directly (this is a documentation skill). Consumer skills/scripts declare their own deps.
- **python_packages:** none.
- **cpan / npm:** none.

## Error Handling

On failure, the skill emits a non-zero exit code or returns a structured error in the response. Consumer skills handle errors per their own SKILL.md.

## Resources

For the full consumer table with cross-references, see [skill-overview](./references/skill-overview.md) § Consumer skill cross-reference.

- [SKILL](../amw-design-principles/SKILL.md) — orchestrator; routes generic design intent to executor skills.
- [SKILL](../amw-ascii-creator/SKILL.md) — primary ASCII authoring skill.
- [SKILL](../amw-ascii-validator/SKILL.md) — ASCII validator.
- [SKILL](../amw-ascii-sketch/SKILL.md) — plan-phase ASCII loop.
- [SKILL](../amw-ascii-to-html/SKILL.md), [SKILL](../amw-ascii-to-svg/SKILL.md) — direct ASCII conversion skills.

## Non-negotiables

- This skill NEVER emits diagrams, files, or artifacts. It answers lookup questions against the references only.
- Consumer skills and commands MUST cross-reference this library via relative paths (`../amw-diagram-formats/references/<name>.md`). They MUST NOT copy the prose inline.
- The IR schema version is SINGLE-VALUE. No "legacy" or "compat" variants live alongside the canonical IR schema version 1.0.
- PNG-as-source is `impossible` in every dispatch table. Do not add a "fallback OCR" or "re-interpret" path.
