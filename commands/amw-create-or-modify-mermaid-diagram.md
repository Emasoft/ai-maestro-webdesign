---
name: amw-create-or-modify-mermaid-diagram
description: "Shortcut for users who know they want a Mermaid source file created or modified directly — all 9 grammar types supported, with mandatory bin/amw-mermaid-lint.sh gate. An agent in Main-agent mode may also invoke skills/amw-mermaid-diagram/ directly via the orchestrator after Phase A approval, applying the full grammar selection and annotation techniques the skill exposes beyond this command."
---

# /amw-create-or-modify-mermaid-diagram

Thin dispatcher over `skills/amw-mermaid-diagram/` (create + modify — SOURCE authoring) and `skills/amw-diagram-formats/references/modify-flow.md` (shared modify pipeline). Emits exactly one `.mmd` (Mermaid source) file. Rendering to SVG/PNG/ASCII is delegated to `skills/amw-mermaid-render/` via `bin/amw-mermaid-render.sh` — NOT emitted by this command.

## Dispatch

1. **Detect input shape** from `$ARGUMENTS`:
   - Path ending in `.mmd` / `.mermaid` AND `test -f "$ARGUMENTS"` AND `bin/amw-diagram-detect-format.sh "$ARGUMENTS"` reports `mermaid` → **modify flow**.
   - Content (inline paste or fenced ` ```mermaid ` block) starts with a Mermaid grammar header (`flowchart|graph|sequenceDiagram|stateDiagram|stateDiagram-v2|classDiagram|erDiagram|gantt|pie|journey|mindmap|quadrantChart|gitGraph|C4Context`) → **modify flow** (treat as an existing source to edit).
   - Natural-language brief ("Mermaid flowchart of login", "sequence diagram of the OAuth handshake") → **create flow**.
   - Empty `$ARGUMENTS` → ask the user for a brief OR an existing file path.

2. **Route:**
   - Create path → `skills/amw-mermaid-diagram/SKILL.md` pipeline. Grammar type is selected from brief cues (flowchart default for "flow"/"process"; sequenceDiagram for "request/response"/"handshake"; erDiagram for "schema"; etc — see `skills/amw-diagram-formats/references/mermaid.md` §2).
   - Modify path → shared 6-step pipeline at `skills/amw-diagram-formats/references/modify-flow.md`: detect → `bin/amw-parse-mermaid-diagram.py` → IR-patch → `bin/amw-diagram-ir.py emit --format mermaid` → `bin/amw-mermaid-lint.sh`. Retry budget = 3. Atomic move on PASS.

3. **Optional flags:**
   - `--type flowchart|sequence|state|class|er|gantt|pie|journey|mindmap` — force the grammar type (create path only).
   - `--direction TD|TB|LR|BT|RL` — flowchart/graph direction suffix (create path, flowchart only). Default: `LR`.
   - `--render svg|png|ascii` — after source save, delegate to `bin/amw-mermaid-render.sh` for a companion rendered artifact.

4. **Output contract:** exactly one `.mmd` source file at the user's working directory with a descriptive Title-Case filename. `bin/amw-mermaid-lint.sh` PASS is non-skippable — a FAIL aborts with hints verbatim and leaves the original file (if any) untouched.

## Cross-references

- `skills/amw-mermaid-diagram/SKILL.md` — create + modify (source authoring).
- `skills/amw-mermaid-render/SKILL.md` — rendering skill (source → SVG/PNG/ASCII). THIS COMMAND DELEGATES RENDERING; it does not emit rendered output itself.
- `skills/amw-diagram-formats/references/mermaid.md` — authoritative Mermaid format spec + 40-technique catalog.
- `skills/amw-diagram-formats/references/modify-flow.md` — shared modify pipeline.
- `bin/amw-mermaid-lint.sh`, `bin/amw-parse-mermaid-diagram.py`, `bin/amw-diagram-ir.py`, `bin/amw-mermaid-render.sh` — backing tools.
- `/amw-convert-any-diagram-format` — natural next step if user wants the Mermaid source rendered to a different format.
