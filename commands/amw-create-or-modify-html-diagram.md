---
name: amw-create-or-modify-html-diagram
description: "Shortcut for users who know they want an HTML diagram (editorial or infographic) created or modified directly — dispatches to html-diagram skill or modify-flow with validation gate. An agent in Main-agent mode may also invoke skills/amw-html-diagram/ directly via the orchestrator after Phase A approval, applying diagram-editorial and infographics techniques beyond what this command's --style flag exposes."
---

# /amw-create-or-modify-html-diagram

Thin dispatcher over `skills/amw-html-diagram/` (create path) and [modify-flow](../skills/amw-diagram-formats/references/modify-flow.md) (modify path). Emits exactly one self-contained `.html` file (inline CSS + inline SVG, no external build).
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references

## Dispatch

1. **Detect input shape** from `$ARGUMENTS`:
   - Path ending in `.html` / `.htm` AND `test -f "$ARGUMENTS"` AND `bin/amw-diagram-detect-format.sh "$ARGUMENTS"` reports `html` → **modify flow**.
   - Natural-language brief ("HTML architecture diagram", "infographic of Q3 metrics") → **create flow**.
   - Empty `$ARGUMENTS` → ask the user for a brief OR an existing file path.

2. **Route:**
   - Create path → [SKILL](../skills/amw-html-diagram/SKILL.md) pipeline steps 1 + 3 + 4 + 5 (skips step 2 parse). Further sub-dispatch by `--style`: `editorial` → `skills/amw-diagram-editorial/` (13 archetypes, default); `infographic` → `skills/amw-infographics/` (dense HTML/PNG/PDF).
   - Modify path → shared 6-step pipeline at [modify-flow](../skills/amw-diagram-formats/references/modify-flow.md): detect → `bin/amw-parse-html-diagram.py` → IR-patch → `bin/amw-diagram-ir.py emit --format html` → `bin/amw-validate-html-diagram.sh`. Retry budget = 3. Atomic move on PASS.
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references

3. **Optional flags:**
   - `--type flowchart|sequence|state|ER|timeline|swimlane|quadrant|tree|layer|venn|funnel|pyramid|nested` — force one of the 13 editorial archetypes (create path with `--style editorial` only).
   - `--style editorial|infographic` — pick the create-path backend.
   - `--brand <tokens-path>` — load design tokens from a prior `/amw-extract-style` report.

4. **Output contract:** exactly one `.html` file at the user's working directory with a descriptive Title-Case filename. `bin/amw-validate-html-diagram.sh` PASS AND AI-slop-avoid checklist PASS are both non-skippable gates — a FAIL aborts with hints verbatim and leaves the original file (if any) untouched.

## Cross-references

- [SKILL](../skills/amw-html-diagram/SKILL.md) — create + modify dispatcher.
- [html](../skills/amw-diagram-formats/references/html.md) — authoritative HTML format spec + 100-technique catalog.
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- [modify-flow](../skills/amw-diagram-formats/references/modify-flow.md) — shared modify pipeline.
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references
- [SKILL](../skills/amw-diagram-editorial/SKILL.md) — create-path backend (editorial).
- [SKILL](../skills/amw-infographics/SKILL.md) — create-path backend (infographic).
- [ai-slop-avoid](../skills/amw-design-principles/ai-slop-avoid.md) — final output-ban gate.
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)
- `bin/amw-validate-html-diagram.sh`, `bin/amw-parse-html-diagram.py`, `bin/amw-diagram-ir.py` — backing tools.
- `/amw-preview` — natural next step to open the emitted `.html`.
