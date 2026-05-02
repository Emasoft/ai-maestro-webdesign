---
name: amw-create-or-modify-svg-diagram
description: "Shortcut for users who know they want a standalone SVG diagram created or modified directly — freeform or layered-architecture, with svg-render.py render-verify gate. An agent in Main-agent mode may also invoke skills/amw-svg-diagram/ directly via the orchestrator after Phase A approval, applying sub-dispatch and styling techniques the skill exposes beyond this command's --kind flag."
---

# /amw-create-or-modify-svg-diagram

Thin dispatcher over `skills/amw-svg-diagram/` (create path) and [modify-flow](skills/amw-diagram-formats/references/modify-flow.md) (modify path). Emits exactly one standalone `.svg` file (well-formed XML, self-contained, no remote resources).

## Dispatch

1. **Detect input shape** from `$ARGUMENTS`:
   - Path ending in `.svg` AND `test -f "$ARGUMENTS"` AND `bin/amw-diagram-detect-format.sh "$ARGUMENTS"` reports `svg` → **modify flow**.
   - Natural-language brief ("SVG flowchart of login", "layered architecture SVG of web/api/db") → **create flow**.
   - Empty `$ARGUMENTS` → ask the user for a brief OR an existing file path.

2. **Route:**
   - Create path → [SKILL](skills/amw-svg-diagram/SKILL.md) pipeline. Further sub-dispatch by `--kind`: `arch` → `skills/amw-diagram-architecture/` (layered); default `freeform` → `skills/amw-diagram-svg/` (node-and-edge).
   - Modify path → shared 6-step pipeline at [modify-flow](skills/amw-diagram-formats/references/modify-flow.md): detect → `bin/amw-parse-svg-diagram.py` → IR-patch → `bin/amw-diagram-ir.py emit --format svg` → `bin/amw-validate-svg-diagram.sh` + `bin/amw-svg-render.py render/finish`. Retry budget = 3. Atomic move on PASS.

3. **Optional flags:**
   - `--kind arch|freeform` — pick the create-path backend.
   - `--png` — after SVG save, also rasterize via `bin/amw-svg-render.py` / cairosvg to a companion `.png`.

4. **Output contract:** exactly one `.svg` file at the user's working directory with a descriptive Title-Case filename. `bin/amw-validate-svg-diagram.sh` PASS AND render-verify PASS are both non-skippable gates — a FAIL aborts with hints verbatim and leaves the original file (if any) untouched.

## Cross-references

- [SKILL](skills/amw-svg-diagram/SKILL.md) — create + modify dispatcher.
- [svg](skills/amw-diagram-formats/references/svg.md) — authoritative SVG format spec + 54-technique catalog.
- [modify-flow](skills/amw-diagram-formats/references/modify-flow.md) — shared modify pipeline.
- [SKILL](skills/amw-svg-creator/SKILL.md) — GATED icons / logos / patterns (NOT a dispatch target here).
- [SKILL](skills/amw-diagram-svg/SKILL.md) — create-path backend (freeform).
- [SKILL](skills/amw-diagram-architecture/SKILL.md) — create-path backend (layered arch).
- [SKILL](skills/amw-ascii-to-svg/SKILL.md) — upstream when input is ASCII.
- `bin/amw-validate-svg-diagram.sh`, `bin/amw-parse-svg-diagram.py`, `bin/amw-diagram-ir.py`, `bin/amw-svg-render.py` — backing tools.
- `/amw-preview` — optional next step for preview.
