---
name: amw-diagram-formats
description: Look up the authoritative spec for ASCII / HTML / SVG / Mermaid diagram formats, the plugin's IR schema, the cross-format conversion matrix, the validation dispatcher, or the modify / diff pipelines. Triggers on narrow technical intents only — "what does the IR schema look like", "how does format detection work", "conversion matrix for ASCII to SVG", "IR-level diff algorithm", "validation dispatcher contract", "Mermaid format spec". Does NOT trigger on generic design / diagram creation intent — those belong to ascii-creator / svg-diagram / html-diagram / mermaid-diagram. This is a references-only meta-skill; it NEVER emits diagrams itself.
version: 0.1.0
---

# Diagram Formats — shared reference library

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> **Consumer scope:** every other diagram skill and every `wd-*-diagram*` command pulls its format / IR / conversion / validation rules from this meta-skill. Do NOT re-author these specs inside the consumer skills — they cross-reference this library.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. It is a **reference-only meta-skill** that is never invoked directly by users. Every other diagram skill and every `wd-*-diagram*` command reads its format specs, IR schema, and conversion rules from here. The `design-principles` orchestrator routes here only when a user explicitly asks about format internals (`"what's the IR schema"`, `"conversion matrix"`).


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

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
- "diagram-ir/1.0 spec"
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
| `./references/ascii.md` | ASCII format spec — syntax, parse, emit, validate, techniques. Authored by the sibling `format-refs` agent. | `ascii-creator`, `ascii-validator`, `ascii-sketch`, `ascii-to-html`, `ascii-to-svg`, `/amw-ascii-to-html`, `/amw-ascii-to-svg` |
| `./references/html.md` | HTML+inline-SVG format spec — starter-components, AI-slop gate, Tweaks invariants, React/Babel pins, ARIA/a11y. Authored by the sibling `format-refs` agent. | `html-diagram`, `diagram-editorial`, `infographics`, `/amw-create-or-modify-html-diagram` |
| `./references/svg.md` | Standalone SVG format spec — primitives, viewport, text, cairosvg path. Authored by the sibling `format-refs` agent. | `svg-diagram`, `svg-creator`, `diagram-svg`, `diagram-architecture`, `/amw-create-or-modify-svg-diagram` |
| `./references/mermaid.md` | Mermaid grammar subset, themes, mmdc flags, SVG/PNG/ASCII output paths. Authored by the sibling `format-refs` agent. | `mermaid-diagram`, `mermaid-render`, `diagram-architecture`, `/amw-create-or-modify-mermaid-diagram` |
| `./references/png.md` | PNG as OUTPUT TARGET only — rasterize pipelines per source format. PNG as SOURCE is `impossible` per user directive. Authored by the sibling `format-refs` agent. | `excalidraw-illustrations`, `infographics`, `hyperframes-bridge`, `/amw-create-excalidraw-like-diagram-png` |
| `./references/ir-schema.md` | IR JSON schema in prose + examples + lossy-conversion table per format. | `diagram-ir.py`, every `wd-*-diagram*` command, every parser in `bin/` |
| `./references/conversion-matrix.md` | Canonical N×N table. PNG-input cells = `impossible`. Every dispatch rule for `/amw-convert-any-diagram-format`. | `diagram-convert`, `/amw-convert-any-diagram-format`, `/amw-create-webpage-from-diagram` |
| `./references/modify-flow.md` | Shared detect → parse → IR-patch → re-render → re-validate pipeline. | All 4 `wd-create-or-modify-*-diagram` commands; `diagram-webpage-sync` |
| `./references/diff-algorithm.md` | IR-level structural diff algorithm (node-id match, edge set diff, markdown report). | `diagram-compare`, `/amw-compare-diagrams`, `bin/amw-diagram-ir-diff.py` |
| `./references/detect-format.md` | Format detection decision tree (magic lines, extensions, content sniffing). | `bin/amw-diagram-detect-format.sh`, every dispatcher |
| `./references/validation-dispatcher.md` | Unified `PASS \| FAIL: <line>: <message> [FIX: <hint>]` output contract. | `ascii-validator`, `/amw-validate-any-diagram-format`, every per-format validator wrapper |
| `./schema.json` | Machine-readable JSON Schema (draft-07) for the IR. Consumed by `bin/amw-diagram-ir.py`. | `bin/amw-diagram-ir.py validate`, any JSON-schema-aware tooling |

## Backing scripts (cross-reference only)

These live in `bin/`, not in this skill. The skill documents them; it does not own them.

- `bin/amw-diagram-ir.py` — parse / emit / validate / diff the IR (see `./references/ir-schema.md`).
- `bin/amw-diagram-detect-format.sh` — sniffs format; see `./references/detect-format.md`.
- `bin/amw-validate-diagram.sh` — top-level validator dispatcher; see `./references/validation-dispatcher.md`.
- `bin/amw-validate-html-diagram.sh`, `bin/amw-validate-svg-diagram.sh`, `bin/amw-mermaid-lint.sh` — per-format validator wrappers (see the corresponding references/*.md).
- `bin/amw-validate-ascii.py`, `bin/amw-validate-ascii.py` — ASCII validators; the contract lines up with the unified output format. See `../amw-ascii-validator/SKILL.md`.

## Locked decisions (do not re-litigate)

Per user directive 2026-04-22:

- **IR version is `diagram-ir/1.0`.** Schema evolution requires an ADR and a bump — NOT in scope for Phase 0.
- **PNG is OUTPUT-ONLY.** Every PNG-as-SOURCE conversion cell is `impossible`; the validator dispatcher refuses PNG inputs with a fixed message.
- **Mermaid backend is `mmdc`** (no Kroki).
- **SVG validator is `xmllint --noout`** (no `svg-validator` npm wrapper).
- **HTML validator is `xmllint --html` + `tidy -e -q -errors`** (when available).
- **Round-trip path** (for `/amw-create-webpage-from-diagram`) goes via IR → ASCII → HTML until a dedicated direct pipeline is justified.
- **Task 4d (selector-aware webpage ↔ diagram sync)** is MVP read-only — extract only; sync-back is future work.

## Dependencies

- **runtime_binaries:** none directly (this is a documentation skill). Consumer skills/scripts declare their own deps.
- **python_packages:** none.
- **cpan / npm:** none.

## Cross-references

- `../amw-design-principles/SKILL.md` — orchestrator; routes generic design intent to executor skills.
- `../amw-ascii-creator/SKILL.md` — primary ASCII authoring skill; pulls `./references/ascii.md` + `./references/modify-flow.md`.
- `../amw-ascii-validator/SKILL.md` — ASCII validator; pulls `./references/validation-dispatcher.md`.
- `../amw-ascii-sketch/SKILL.md` — plan-phase ASCII loop; pulls `./references/ascii.md`.
- `../amw-ascii-to-html/SKILL.md`, `../amw-ascii-to-svg/SKILL.md` — direct ASCII conversion skills.

## Non-negotiables

- This skill NEVER emits diagrams, files, or artifacts. It answers lookup questions against the references only.
- Consumer skills and commands MUST cross-reference this library via relative paths (`../amw-diagram-formats/references/<name>.md`). They MUST NOT copy the prose inline.
- The IR schema version is SINGLE-VALUE. No "legacy" or "compat" variants live alongside the canonical `diagram-ir/1.0`.
- PNG-as-source is `impossible` in every dispatch table. Do not add a "fallback OCR" or "re-interpret" path.
