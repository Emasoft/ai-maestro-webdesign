# amw-diagram-formats — skill-overview reference

## Table of Contents

- [Reference index — full table](#reference-index--full-table)
- [Backing scripts (cross-reference only)](#backing-scripts-cross-reference-only)
- [Locked decisions (do not re-litigate)](#locked-decisions-do-not-re-litigate)
- [Consumer skill cross-reference](#consumer-skill-cross-reference)
- [Non-negotiables](#non-negotiables)

Detailed reference index, backing scripts, locked decisions, and resources for the `amw-diagram-formats` meta-skill. The main SKILL.md keeps only the high-level entry points; this file is the authoritative source for the per-file scope and per-script TOC.

## Reference index — full table

Every entry below is an authoritative, hand-maintained source. Consumer skills and commands MUST cross-reference these paths, not re-author the content.

| File | Scope | Consumers |
|---|---|---|
| [ascii](./ascii.md) | ASCII format spec — syntax, parse, emit, validate, techniques. Authored by the sibling `format-refs` agent. | `ascii-creator`, `ascii-validator`, `ascii-sketch`, `ascii-to-html`, `ascii-to-svg`, `/amw-ascii-to-html`, `/amw-ascii-to-svg` |
| [html](./html.md) | HTML+inline-SVG format spec — starter-components, AI-slop gate, Tweaks invariants, React/Babel pins, ARIA/a11y. Authored by the sibling `format-refs` agent. | `html-diagram`, `diagram-editorial`, `infographics`, `/amw-create-or-modify-html-diagram` |
| [svg](./svg.md) | Standalone SVG format spec — primitives, viewport, text, cairosvg path. Authored by the sibling `format-refs` agent. | `svg-diagram`, `svg-creator`, `diagram-svg`, `diagram-architecture`, `/amw-create-or-modify-svg-diagram` |
| [mermaid](./mermaid.md) | Mermaid grammar subset, themes, mmdc flags, SVG/PNG/ASCII output paths. Authored by the sibling `format-refs` agent. | `mermaid-diagram`, `mermaid-render`, `diagram-architecture`, `/amw-create-or-modify-mermaid-diagram` |
| [png](./png.md) | PNG as OUTPUT TARGET only — rasterize pipelines per source format. PNG as SOURCE is `impossible` per user directive. Authored by the sibling `format-refs` agent. | `excalidraw-illustrations`, `infographics`, `hyperframes-bridge`, `/amw-create-excalidraw-like-diagram-png` |
| [ir-schema](./ir-schema.md) | IR JSON schema in prose + examples + lossy-conversion table per format. | `diagram-ir.py`, every `wd-*-diagram*` command, every parser in `bin/` |
| [conversion-matrix](./conversion-matrix.md) | Canonical N×N table. PNG-input cells = `impossible`. Every dispatch rule for `/amw-convert-any-diagram-format`. | `diagram-convert`, `/amw-convert-any-diagram-format`, `/amw-create-webpage-from-diagram` |
| [modify-flow](./modify-flow.md) | Shared detect → parse → IR-patch → re-render → re-validate pipeline. | All 4 `wd-create-or-modify-*-diagram` commands; `diagram-webpage-sync` |
| [diff-algorithm](./diff-algorithm.md) | IR-level structural diff algorithm (node-id match, edge set diff, markdown report). | `diagram-compare`, `/amw-compare-diagrams`, `bin/amw-diagram-ir.py --diff` |
| [detect-format](./detect-format.md) | Format detection decision tree (magic lines, extensions, content sniffing). | `bin/amw-diagram-detect-format.sh`, every dispatcher |
| [validation-dispatcher](./validation-dispatcher.md) | Unified `PASS \| FAIL: <line>: <message> [FIX: <hint>]` output contract. | `ascii-validator`, `/amw-validate-any-diagram-format`, every per-format validator wrapper |
| `../schema.json` | Machine-readable JSON Schema (draft-07) for the IR. Consumed by `bin/amw-diagram-ir.py`. | `bin/amw-diagram-ir.py validate`, any JSON-schema-aware tooling |

## Backing scripts (cross-reference only)

These live in `bin/`, not in this skill. The skill documents them; it does not own them.

- `bin/amw-diagram-ir.py` — parse / emit / validate / diff the IR (see [ir-schema](./ir-schema.md)).
- `bin/amw-diagram-detect-format.sh` — sniffs format; see [detect-format](./detect-format.md).
- `bin/amw-validate-diagram.sh` — top-level validator dispatcher; see [validation-dispatcher](./validation-dispatcher.md).
- `bin/amw-validate-html-diagram.sh`, `bin/amw-validate-svg-diagram.sh`, `bin/amw-mermaid-lint.sh` — per-format validator wrappers (see the corresponding references/*.md).
- `bin/amw-validate-ascii.py` — ASCII validators; the contract lines up with the unified output format. See [../../amw-ascii-validator/SKILL.md](../../amw-ascii-validator/SKILL.md).

## Locked decisions (do not re-litigate)

Per user directive 2026-04-22:

- **IR version is diagram-ir version 1.0 (schema ID `<diagram-ir/1.0>`).** Schema evolution requires an ADR and a bump — NOT in scope for Phase 0.
- **PNG is OUTPUT-ONLY.** Every PNG-as-SOURCE conversion cell is `impossible`; the validator dispatcher refuses PNG inputs with a fixed message.
- **Mermaid backend is `mmdc`** (no Kroki).
- **SVG validator is `xmllint --noout`** (no `svg-validator` npm wrapper).
- **HTML validator is `xmllint --html` + `tidy -e -q -errors`** (when available).
- **Round-trip path** (for `/amw-create-webpage-from-diagram`) goes via IR → ASCII → HTML until a dedicated direct pipeline is justified.
- **Task 4d (selector-aware webpage ↔ diagram sync)** is MVP read-only — extract only; sync-back is future work.

## Consumer skill cross-reference

The following skills consume this library via relative path references:

- [../../amw-design-principles/SKILL.md](../../amw-design-principles/SKILL.md) — orchestrator; routes generic design intent to executor skills.
- [../../amw-ascii-creator/SKILL.md](../../amw-ascii-creator/SKILL.md) — primary ASCII authoring skill; pulls `ascii.md` + `modify-flow.md`.
- [../../amw-ascii-validator/SKILL.md](../../amw-ascii-validator/SKILL.md) — ASCII validator; pulls `validation-dispatcher.md`.
- [../../amw-ascii-sketch/SKILL.md](../../amw-ascii-sketch/SKILL.md) — plan-phase ASCII loop; pulls `ascii.md`.
- [../../amw-ascii-to-html/SKILL.md](../../amw-ascii-to-html/SKILL.md), [../../amw-ascii-to-svg/SKILL.md](../../amw-ascii-to-svg/SKILL.md) — direct ASCII conversion skills.

## Non-negotiables

- This meta-skill NEVER emits diagrams, files, or artifacts. It answers lookup questions against the references only.
- Consumer skills and commands MUST cross-reference this library via relative paths (`../amw-diagram-formats/references/<name>.md`). They MUST NOT copy the prose inline.
- The IR schema version is SINGLE-VALUE. No "legacy" or "compat" variants live alongside the canonical IR schema version 1.0.
- PNG-as-source is `impossible` in every dispatch table. Do not add a "fallback OCR" or "re-interpret" path.
