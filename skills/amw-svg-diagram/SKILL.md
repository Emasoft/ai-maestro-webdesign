---
name: amw-svg-diagram
description: Author OR edit a standalone SVG diagram — freeform node-and-edge, layered architecture, or structural flow. Triggers on "create SVG diagram", "modify SVG diagram", "edit .svg diagram", "render structure as SVG". Does NOT claim generic design / illustration / logo vocabulary — routes to design-principles / svg-creator. Dispatcher over diagram-svg (freeform) + diagram-architecture (layered). Use when authoring an SVG diagram. Trigger with /amw-create-or-modify-svg-diagram.
version: 0.1.0
---

# SVG Diagram — thin authoring + modify dispatcher

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Format spec (authoritative):** [svg](../amw-diagram-formats/references/svg.md).
> **Modify pipeline (authoritative):** [modify-flow](../amw-diagram-formats/references/modify-flow.md).

This skill does not redefine SVG primitives / viewport rules / text centering / cairosvg rasterization / the 54-technique filter cookbook — every one of those lives once in [svg](../amw-diagram-formats/references/svg.md). The skill's job is to DISPATCH between `diagram-svg` (freeform node-and-edge) and `diagram-architecture` (layered tiered arch) for creation, and to run the shared modify-flow when the input is an existing `.svg`.

## Overview

Thin dispatcher for standalone SVG diagram authoring + modification. Accepts a NL brief (create path) or an existing `.svg` (modify path). Routes create requests to `amw-diagram-svg` (freeform) or `amw-diagram-architecture` (layered) per `--kind freeform|arch`. Runs the shared 5-step modify-flow (parse → IR → patch → re-render → validate) for modify requests. Emits exactly one well-formed `.svg` per invocation. Does NOT produce icons, logos, or illustrations — those go to `amw-svg-creator`.

## Instructions

1. Detect whether the input is a natural-language brief (create path) or an existing `.svg` file (modify path).
2. For create path: choose `--kind freeform` (node-and-edge dispatch to `amw-diagram-svg`) or `--kind arch` (layered tiered dispatch to `amw-diagram-architecture`) based on the brief; use 1000×1000 viewBox with four-group structure (`defs`, `zones`, `nodes`, `labels`).
3. For modify path: parse the existing `.svg` to IR with `bin/amw-parse-svg-diagram.py`; apply the requested edit to node/edge labels or structure in the IR.
4. Re-render from IR to SVG via `bin/amw-diagram-ir.py emit --format svg`.
5. Validate with `bin/amw-validate-svg-diagram.sh` (well-formed XML + SVG namespace check); a FAIL aborts and leaves the original file untouched (retry budget = 3).

See `## Pipeline (5 steps — matches shared modify-flow)` below.

## Activation

Callable directly via the `/amw-create-or-modify-svg-diagram` command, or invoked by the `design-principles` orchestrator during **Phase B** when the approved deliverable is a standalone SVG diagram. An agent in Main-agent mode may also invoke this skill directly. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

OUTPUT (terminal). Emits exactly one standalone `.svg` file. Downstream of `design-principles` orchestration. Upstream of `bin/amw-svg-render.py` (PNG preview) and `/amw-convert-any-diagram-format`.

## Trigger conditions

- "create an SVG diagram" / "build an SVG diagram of <subject>"
- "render this structure as SVG"
- "SVG architecture diagram / flowchart of <subject>"
- "modify this SVG diagram" / "edit the SVG at `<path>`" / "update `<something>.svg>`"
- "/amw-create-or-modify-svg-diagram <brief-or-path>"

Do NOT activate on:
- Generic "create an icon" / "design a logo" / "SVG pattern" — those are `../amw-svg-creator/` territory (which is GATED to icons/logos/technical SVG anyway).
- Converting an existing diagram to SVG (`/amw-convert-any-diagram-format --to svg`).
- Validating an SVG file only (`/amw-validate-any-diagram-format`).

## Component detection table (excerpt)

Full node-shape + edge + viewport + filter + animation catalog lives in [svg](../amw-diagram-formats/references/svg.md) §2 + §8 (54 techniques). The 8 rows below are the most common dispatch cues — consult the ref for the rest.

| SVG construct | IR node/edge kind | Ref |
|---|---|---|
| `<rect rx="20" ry="20">` | `node{shape:rect, kind:process, corner:rounded}` | [svg](../amw-diagram-formats/references/svg.md) TECH-SV-15 |
| `<ellipse> + <rect> + <ellipse>` (cylinder stack) | `node{kind:database}` | ref TECH-SV-16 |
| `<circle>` | `node{kind:actor}` | ref TECH-SV-17 |
| `<polygon>` 4-point diamond | `node{kind:decision}` | ref TECH-SV-18 |
| `<rect stroke-dasharray="8 4">` | `node{kind:external-system}` | ref TECH-SV-19 |
| `<line marker-end="url(#arrow)">` | `edge{style:solid, head:triangle}` | ref TECH-SV-20 |
| `<line stroke-dasharray="8 4">` | `edge{style:dashed}` (async) | ref §2.2 |
| `<g id="zone-*">` wrapping `<rect>` layer bg | layered arch zone (`layout:layered`) | ref TECH-SV-37 |

## Pipeline (5 steps — matches shared modify-flow)

1. **Detect** source shape. If `$ARGUMENTS` is a path to an existing `.svg` → **modify path**. If it's a brief → **create path** (further dispatch by `--kind`: `arch` → `../amw-diagram-architecture/`, default `freeform` → `../amw-diagram-svg/`).
2. **Parse** (modify path only) via `bin/amw-parse-svg-diagram.py` → IR (schema: [ir-schema](../amw-diagram-formats/references/ir-schema.md)). Geometric interpretation: rects → nodes, lines/paths+markers → edges. Create path skips this step.
3. **IR operation:**
   - Create path → generate IR from the brief, route to [SKILL](../amw-diagram-svg/SKILL.md) (freeform) or [SKILL](../amw-diagram-architecture/SKILL.md) (layered arch), let the producer emit.
   - Modify path → apply the user's requested edit to the IR (text substitution on `nodes[*].label` for MVP; structural operations once Phase 1 parsers land — see [modify-flow](../amw-diagram-formats/references/modify-flow.md) §5.3).
4. **Re-render** via `bin/amw-diagram-ir.py emit --format svg` (wraps the chosen producer for create path; emits the patched IR back to SVG for modify path). The renderer reads from [svg](../amw-diagram-formats/references/svg.md) §1-§4 (primitives, viewport, text).
5. **Re-validate** via `bin/amw-validate-svg-diagram.sh` (wraps `xmllint --noout --nonet` + SVG-namespace check + no-remote-resource grep; unified PASS/FAIL contract per [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md)). Followed by **render-verify**: `bin/amw-svg-render.py render <file>` emits a PNG preview; Claude visually inspects before `bin/amw-svg-render.py finish` finalises. A FAIL aborts and leaves the original file untouched. Retry budget = 3.

## Output

One standalone `.svg` file per invocation (well-formed XML, `xmlns="http://www.w3.org/2000/svg"`, no external resources). Accompanied by a PNG preview generated by `bin/amw-svg-render.py`. Output path follows project-inference rules from [project-output-routing](../amw-design-principles/references/project-output-routing.md).

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8`, `xmllint` (libxml2) — both checked by `/amw-doctor`.
- **python_packages:** `cairosvg` (for `bin/amw-svg-render.py` rasterization), `lxml` (`bin/amw-parse-svg-diagram.py`).
- **npm:** none.
- **Shared scripts:** `bin/amw-parse-svg-diagram.py`, `bin/amw-diagram-ir.py`, `bin/amw-validate-svg-diagram.sh`, `bin/amw-svg-render.py` (render / finish / status / reset).

## Examples

**Concrete example — author a freeform SVG diagram:**

- **Input:** "Show the request flow between a browser, an API gateway, and three microservices, with arrows labeled by transport (HTTPS, gRPC)."
- **Operation:** parse the brief to IR (nodes + edges + transport annotations) via `bin/amw-diagram-ir.py`. Emit standalone SVG with measured node boxes, oklch color tokens from the orchestrator's color-system reference (see [color-system](../amw-design-principles/color-system.md)), and aria-labels on every shape. Validate via `bin/amw-validate-svg-diagram.sh` (checks viewBox, font stack, no forbidden primitives). Render via `bin/amw-svg-render.py`.
- **Output:** `request-flow.svg` (self-contained, no external deps, raster-friendly via cairosvg).

**Concrete example — modify an existing layered architecture diagram:**

- **Input:** `existing-architecture.svg` plus the patch instruction "rename the cache layer from 'Memcached' to 'Redis' and add a fourth layer 'Object storage' below the database".
- **Operation:** detect → parse to IR → patch nodes → emit → re-validate (the 6-step modify-flow). Keep the existing visual language (oklch palette, font sizes, viewBox).
- **Output:** updated `existing-architecture.svg` with the renamed layer and the new bottom layer added; passes validation and renders identically except for the changes.

See [SKILL](../amw-diagram-svg/SKILL.md) for freeform node-and-edge examples and [SKILL](../amw-diagram-architecture/SKILL.md) for layered architecture examples.

## Resources

- [svg](../amw-diagram-formats/references/svg.md) — authoritative SVG format spec + 54-technique catalog.
- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — authoritative 6-step modify pipeline.
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema consumed by `bin/amw-diagram-ir.py`.
- [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md) — unified validator output contract.
- [SKILL](../amw-svg-creator/SKILL.md) — GATED SVG producer (icons / logos / patterns / animations). NOT this skill's dispatch target — this skill is for structural diagrams only.
- [SKILL](../amw-diagram-svg/SKILL.md) — create-path backend for `--kind freeform`.
- [SKILL](../amw-diagram-architecture/SKILL.md) — create-path backend for `--kind arch` (layered).
- [SKILL](../amw-ascii-to-svg/SKILL.md) — upstream when input is ASCII (ASCII → SVG path).
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Non-negotiables

- Exactly one standalone `.svg` per invocation. Well-formed XML. `xmlns="http://www.w3.org/2000/svg"` on the root. ([svg](../amw-diagram-formats/references/svg.md) §1.1)
- No `<script>` in SVG output. No `<foreignObject>` with HTML. No remote `<image href="http...">`. ([svg](../amw-diagram-formats/references/svg.md) §1.3)
- Every emitted `.svg` passes `bin/amw-validate-svg-diagram.sh` AND render-verify (`bin/amw-svg-render.py render → finish` guard). A FAIL aborts; the original file is untouched.
- Minimum 120-unit spacing on the active axis, 40-unit margin reserve — labels > 20 chars truncate with `...`. ([svg](../amw-diagram-formats/references/svg.md) TECH-SV-21 + TECH-SV-22)
- Animated SVGs carry the `@media (prefers-reduced-motion: reduce)` guard. ([svg](../amw-diagram-formats/references/svg.md) TECH-SV-25)
- Do NOT re-author the SVG spec inside this skill — reference [svg](../amw-diagram-formats/references/svg.md). If a rule is wrong, fix it there.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| `bin/amw-validate-svg-diagram.sh` FAIL | Unclosed tag, stray `&`, missing `xmlns`, `<script>` present | Return the validator report verbatim; do not guess-repair. |
| `bin/amw-svg-render.py` refuses `finish` | `render` step was never called | Run `bin/amw-svg-render.py render <file>` first; visually inspect the PNG. |
| `cairosvg` blank output | Content outside viewBox, unsupported filter | Reposition inside viewBox; simplify filters per [svg](../amw-diagram-formats/references/svg.md) §5.2. |
| Modify path hits retry budget 3 FAILs | Patch conflicts with existing SVG structure | Surface validator findings; ask the user to refine the edit. |
| Parser returns empty IR (modify path) | SVG has no detectable diagram primitives (raw artwork) | Raw-source stub per `modify-flow.md` §5.3; warn that structural patching is unavailable. |
