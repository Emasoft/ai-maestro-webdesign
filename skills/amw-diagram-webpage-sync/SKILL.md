---
name: amw-diagram-webpage-sync
description: Re-emit an existing webpage (`.html`) from an edited diagram source (ASCII / SVG / Mermaid). Chains diagram → IR → ASCII → HTML, overwrites the page (originals to `.bak`), surfaces a diff. Triggers on "edit diagram in my webpage", "modify webpage from this diagram", "sync diagram into my HTML". Does NOT claim generic design vocabulary. Refuses raster-image-tag diagrams. Use when syncing a diagram back into a webpage. Trigger with /amw-modify-webpage-from-diagram.
version: 0.1.0
---

# Diagram Webpage Sync — round-trip re-emitter

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Modify pipeline (authoritative):** [modify-flow](../amw-diagram-formats/references/modify-flow.md).
> [modify-flow.md] The pipeline · Create vs modify dispatch · Step-by-step detail · Work directory and file naming · Per-format guidance · Conversion is a modify-flow variant · Composition with round-trip skills · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
> **IR schema:** [ir-schema](../amw-diagram-formats/references/ir-schema.md).
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers
> **HTML format spec:** [html](../amw-diagram-formats/references/html.md).
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher

This skill owns the **reverse leg** of the webpage round-trip: a user has edited a diagram (ASCII / SVG / Mermaid), and wants the webpage regenerated from it. The MVP strategy is **full re-emission** — run the ascii-to-html pipeline end-to-end, back up the old `.html` to `.bak`, and show a structural diff of what changed.

## Overview

Re-emits an existing webpage from an edited diagram source (ASCII / SVG / Mermaid). Chains diagram → IR → ASCII → HTML via a 7-step pipeline, backs up the original `.html` to `.bak` before overwriting, and surfaces both an IR-level structural diff and an HTML-level diff of what changed. PNG-embedded diagram regions are refused by plugin directive.

## Instructions

1. Read the target webpage and reject if the primary diagram region is a PNG (`<img src="*.png">` or `data:image/png;base64,...`).
2. Parse the current page to IR with `bin/amw-parse-html-diagram.py`; parse the new diagram to IR with `bin/amw-diagram-ir.py parse`.
3. Compute the structural diff with `bin/amw-diagram-ir.py diff` and surface the add/remove/move operations as a Markdown summary before overwriting.
4. Apply the patch via full re-emission: ASCII → `/amw-ascii-to-html`; SVG/Mermaid → emit intermediate ASCII first via IR, then `/amw-ascii-to-html`.
5. Run `bin/amw-html-diff.py` to produce the HTML-level structural diff; save the original to `<webpage>.bak` atomically before overwriting.
6. Validate with `bin/amw-validate-diagram.sh`; on PASS announce the `.bak` path and both diff summaries; on FAIL restore from `.bak` and exit 1.
7. See the `## Pipeline (7 steps)` section below for the authoritative execution sequence.

See the `## Pipeline (7 steps)` section below for the authoritative execution sequence.

## MVP limits (explicit, per plugin directive 2026-04-22)

**Full DOM-surgical patching (keeping the original styling / scripts / non-diagram content intact while only swapping the diagram region) is DEFERRED to a future phase.** The MVP re-emits the entire page from the diagram + design-principles tokens. If the user has made manual post-generation edits to the original HTML (custom CSS, handwritten copy outside the diagram, third-party script integrations), those edits WILL be lost during re-emission — they remain in the `.bak` file only.

Users who have significant manual CSS should instead use `/amw-sketch` + `/amw-ascii-to-html` fresh, and graft the diagram region into their existing page by hand.

## Activation

Callable directly via the `/amw-modify-webpage-from-diagram` command (user shortcut for users who have an edited diagram and want to sync it back into an existing webpage), or invoked by the `design-principles` orchestrator during **Phase B** as the reverse leg of the webpage round-trip. An agent in Main-agent mode may also invoke this skill directly via the orchestrator without going through the command.


This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

**INPUT + OUTPUT.** Input side: an existing `.html` page + a new / edited diagram source. Output side: the rewritten `.html` + a structural-diff report. Paired with `webpage-to-diagram` for the two-half round-trip exposed by `/amw-modify-diagram-of-webpage`.

## Trigger conditions

- "edit the diagram in my webpage" / "modify the webpage from this diagram"
- "sync this diagram back into `<html-file>`"
- "re-emit the page from the updated ASCII"
- "/amw-modify-webpage-from-diagram `<html>` `<diagram>`"

Do NOT activate on:
- "create a webpage from a diagram" — `/amw-create-webpage-from-diagram` owns greenfield generation.
- "extract the diagram from my webpage" — `../amw-webpage-to-diagram/` owns the forward leg.
- Generic design vocabulary — the orchestrator's job.

## Pipeline (7 steps)

1. **Read target.** Open the existing `<webpage.html>`. Reject if not a regular file. Reject if the primary diagram region is a `<img src="*.png">` or a `data:image/png;base64,...` — print the standard PNG refusal: *"REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact (ASCII / HTML / SVG / Mermaid)."*
2. **Parse current page to IR.** Call `bin/amw-parse-html-diagram.py --in <webpage.html> --out /tmp/amw-sync-<hash>-old-ir.json`. The result is the IR view of what's currently on the page (landmarks + inline SVG if any).
3. **Parse the new diagram to IR.** `bin/amw-diagram-ir.py parse --in <new-diagram> --out /tmp/amw-sync-<hash>-new-ir.json`. The diagram can be ASCII / SVG / Mermaid (HTML is rejected — source and target would collide; use `/amw-ascii-to-html` with the new ASCII instead).
4. **Compute structural diff.** Run `bin/amw-diagram-ir.py diff --a old-ir.json --b new-ir.json --out /tmp/amw-sync-<hash>-patch.json`. Surface the add/remove/move operations to the user as a Markdown summary before overwriting.
5. **Apply patch = full re-emission (MVP).** Instead of DOM-surgical patching, re-run the standard ascii-to-html pipeline:
   - If the diagram source is ASCII → pass directly to `/amw-ascii-to-html <new-diagram>`.
   - If SVG or Mermaid → emit intermediate ASCII via `bin/amw-diagram-ir.py emit --format ascii` on the NEW diagram's IR, then hand off to `/amw-ascii-to-html`.
   - Before overwrite, move the original to `<webpage>.bak` (atomic rename). Write the fresh HTML at the original path.
6. **Run html-diff.** Call `bin/amw-html-diff.py --before <webpage>.bak --after <webpage> --out /tmp/amw-sync-<hash>-html-patch.json`. This reports what structurally changed at the HTML level (landmarks added / removed / reordered, headings renamed, inline SVGs added / removed). Pass this summary to the user alongside the IR-level patch from step 4.
7. **Validate + announce.** `bin/amw-validate-diagram.sh <webpage>` (HTML branch). On PASS, announce the `.bak` location, the IR-level summary, and the HTML-level summary. On FAIL: restore from `.bak` (atomic move back), surface the validator FIX hints, exit 1.

## Error Handling

| Symptom | Cause | Fix |
|---|---|---|
| PNG-embedded refusal | Original page has `<img src="*.png">` or `data:image/png;base64,...` as its diagram region | Provide the source artifact that produced the PNG (ASCII / HTML / SVG / Mermaid). This skill does NOT OCR. |
| Validator FAIL on re-emitted HTML | ascii-to-html produced malformed output (usually a bug in the token application) | Restore from `.bak` (automatic), surface the validator report verbatim. |
| User loses manual CSS | MVP re-emits the whole page | Document the MVP limit upfront (§ above). Point the user to the `.bak` for cherry-picking. Full DOM-surgical sync-back is on the Phase-2 roadmap. |
| IR-level diff empty but HTML-level diff non-empty | Token change or chrome change altered the output without changing structure | Normal — surface both diffs so the user knows the change is styling-only. |
| New diagram has more landmarks than old | User added structure (e.g. a new `<section>`) | Patch includes `add` operations; the re-emit covers them automatically. |

## Prerequisites

```yaml
runtime_binaries:
  - python3   # >= 3.8
  - perl      # for bin/amw-validate-ascii.py (intermediate validation)

python_packages:
  - lxml              # OPTIONAL
  - beautifulsoup4    # OPTIONAL
```

## Output

Produces a rewritten `.html` at the original path plus a `.bak` backup of the original. Surfaces both an IR-level structural diff (nodes/edges added/removed/changed) and an HTML-level diff showing structural changes at the landmark level. On validation failure, restores from `.bak` automatically.

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Non-negotiables

- **PNG-embedded refusal is absolute.** Any `<img src="*.png">` or `data:image/png;base64,...` in the diagram region → abort with the standard message. No OCR.
- **`.bak` is always created before overwrite.** On validation failure, the `.bak` is restored atomically — the user's original file is never destroyed.
- **MVP limit is surfaced, not silenced.** Every invocation prints the "full re-emission" disclaimer alongside the diff summary. Users who need surgical patching are pointed at `/amw-sketch` + `/amw-ascii-to-html` fresh.
- **The IR is the pivot.** Even ASCII→ASCII sync goes through IR so the diff summary works uniformly.
- Inherits the three hard rules from [SKILL](../amw-design-principles/SKILL.md) via the `/amw-ascii-to-html` hand-off (tokens, variants on the greenfield path, AI-slop gate).

## Resources

- [modify-flow](../amw-diagram-formats/references/modify-flow.md) — shared 6-step pipeline (§7.1 documents the webpage-sync composition).
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [ir-schema](../amw-diagram-formats/references/ir-schema.md) — IR schema consumed.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
- [html](../amw-diagram-formats/references/html.md) — HTML format spec used by the re-emit step.
  > Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
  > Format definition · 1 File structure (baseline) · 2 Semantic-HTML requirements · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · 1 Listener-before-announce · 2 Partial-keys only · 3 Valid JSON EDITMODE block · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · S1 — design-principles starter-components (canonical chrome) · S2 — ai-slop-avoid (output-ban gate) · S3 — ui-ux-pro-max-skill (industry patterns) · S4 — ux-designer + accessibility · S5 — create-infographics (editorial density) · S6 — diagram-design-editorial (self-contained HTML+SVG) · S7 — ascii-creator mirror (pattern recognition) · S8 — CHI'24 ASCII classics (mockup → HTML skeleton) · S9 — ascii-parse.py (in-repo tokenizer hooks) · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · …(+9)
- [SKILL](../amw-ascii-to-html/SKILL.md) — terminal step of the re-emit pipeline.
- [SKILL](../amw-webpage-to-diagram/SKILL.md) — forward-leg pair.
- `../../bin/amw-html-diff.py` — HTML structural diff (this skill's dedicated tool).
- `../../bin/amw-diagram-ir.py` — IR parse / emit / diff / validate CLI.
- `../../bin/amw-parse-html-diagram.py` — parses the old HTML page to IR.
- `../../bin/amw-validate-diagram.sh` — unified validator dispatcher.
- [SKILL](../amw-design-principles/SKILL.md) — orchestrator.

## Related commands

- `/amw-modify-webpage-from-diagram` — primary entry point for this skill.
- `/amw-modify-diagram-of-webpage` — MVP round-trip: chains `webpage-to-diagram` + user-edit pause + this skill on `apply`.
- `/amw-create-webpage-from-diagram` — greenfield sibling.
