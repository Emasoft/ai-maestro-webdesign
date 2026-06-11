---
name: amw-create-or-modify-ascii-diagram
description: "Shortcut for users who know they want a single ASCII diagram created or modified directly — dispatches to ascii-creator (Mode A/B) or the shared modify-flow, with mandatory bin/amw-validate-ascii.py gate. An agent in Main-agent mode may also invoke skills/amw-ascii-creator/ directly via the orchestrator after Phase A approval, applying the full range of diagram types and authoring modes the skill exposes."
---

# /amw-create-or-modify-ascii-diagram

Thin dispatcher over `skills/amw-ascii-creator/` (create path) and [modify-flow](../skills/amw-diagram-formats/references/modify-flow.md) (modify path). Both paths share the same mandatory validation gate — `bin/amw-validate-ascii.py` — before any file is written to the user's working directory.
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references

## Dispatch

1. **Detect input shape** from `$ARGUMENTS`:
   - Path ending in `.txt` / `.ascii` / `.md` AND `test -f "$ARGUMENTS"` AND `bin/amw-diagram-detect-format.sh "$ARGUMENTS"` reports `ascii` → **modify flow**.
   - Inline ASCII paste (triple-backtick block or raw ASCII in args) → `ascii-creator` Mode B (freeform — already-drafted wireframe, finalize + validate + save).
   - Natural-language brief ("ASCII flowchart of login", "dashboard wireframe 78-col") → `ascii-creator` Mode A (structured) or Mode B (freeform), selected by the skill's classifier.
   - Empty `$ARGUMENTS` → ask the user for a brief OR an existing file path.

2. **Route:**
   - Create path → invoke [SKILL](../skills/amw-ascii-creator/SKILL.md) (Mode A or Mode B per the skill's classifier). See that SKILL.md for the full workflow.
   - Modify path → run the 6-step pipeline at [modify-flow](../skills/amw-diagram-formats/references/modify-flow.md) (detect → parse → IR-patch → emit → re-validate). Retry budget = 3. Atomic move on PASS.
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references

3. **Optional flags:**
   - `--mode diagram|table|layers|sequence|wireframe` — override `ascii-creator`'s auto-classifier (Mode A sub-mode or force Mode B `wireframe`).
   - `--style classic|unicode-rounded` — override the glyph set (see `ascii-creator` "Style presets").

4. **Output contract:** exactly one `.txt` file at the user's working directory with a descriptive Title-Case filename. Validator-PASS is non-skippable — a FAIL aborts with the `FIX:` hints verbatim and leaves the original file (if any) untouched.

## Cross-references

- [SKILL](../skills/amw-ascii-creator/SKILL.md) — authoring flow (Mode A / Mode B).
- [modify-flow](../skills/amw-diagram-formats/references/modify-flow.md) — shared modify pipeline (authoritative).
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references
- [ascii](../skills/amw-diagram-formats/references/ascii.md) — ASCII format spec + 95-technique catalog.
> [ascii.md] Format definition · Dimensional constraints · Parse rules · Emission rules · Validation rules · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- `bin/amw-validate-ascii.py` — mandatory validation gate.
- `bin/amw-diagram-ir.py` — IR parse / emit (modify flow steps 2 + 5).
- `bin/amw-diagram-detect-format.sh` — format sniffer (modify dispatch).
- `/amw-ascii-to-html` — natural next step when the user wants HTML.
- `/amw-ascii-to-svg` — natural next step when the user wants SVG.
