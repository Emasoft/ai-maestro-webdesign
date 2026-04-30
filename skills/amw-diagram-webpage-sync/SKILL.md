---
name: amw-diagram-webpage-sync
description: Re-emit an existing webpage (`.html`) from an edited diagram source (ASCII / SVG / Mermaid). Chains diagram → IR → ASCII → HTML and overwrites the target page after moving the original to `.bak`. Surfaces a structural diff showing what changed. Triggers on narrow technical intents only — "edit the diagram in my webpage", "modify the webpage from this diagram", "sync this diagram back into my HTML", "/amw-modify-webpage-from-diagram". Does NOT claim generic design vocabulary. Refuses pages whose diagram is embedded as `<img src="*.png">` per plugin directive.
version: 0.1.0
---

# Diagram Webpage Sync — round-trip re-emitter

> **Orchestrated by:** `../amw-design-principles/SKILL.md`.
> **Modify pipeline (authoritative):** `../amw-diagram-formats/references/modify-flow.md`.
> **IR schema:** `../amw-diagram-formats/references/ir-schema.md`.
> **HTML format spec:** `../amw-diagram-formats/references/html.md`.

This skill owns the **reverse leg** of the webpage round-trip: a user has edited a diagram (ASCII / SVG / Mermaid), and wants the webpage regenerated from it. The MVP strategy is **full re-emission** — run the ascii-to-html pipeline end-to-end, back up the old `.html` to `.bak`, and show a structural diff of what changed.

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

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| PNG-embedded refusal | Original page has `<img src="*.png">` or `data:image/png;base64,...` as its diagram region | Provide the source artifact that produced the PNG (ASCII / HTML / SVG / Mermaid). This skill does NOT OCR. |
| Validator FAIL on re-emitted HTML | ascii-to-html produced malformed output (usually a bug in the token application) | Restore from `.bak` (automatic), surface the validator report verbatim. |
| User loses manual CSS | MVP re-emits the whole page | Document the MVP limit upfront (§ above). Point the user to the `.bak` for cherry-picking. Full DOM-surgical sync-back is on the Phase-2 roadmap. |
| IR-level diff empty but HTML-level diff non-empty | Token change or chrome change altered the output without changing structure | Normal — surface both diffs so the user knows the change is styling-only. |
| New diagram has more landmarks than old | User added structure (e.g. a new `<section>`) | Patch includes `add` operations; the re-emit covers them automatically. |

## Dependencies

```yaml
runtime_binaries:
  - python3   # >= 3.8
  - perl      # for bin/amw-validate-ascii.py (intermediate validation)

python_packages:
  - lxml              # OPTIONAL
  - beautifulsoup4    # OPTIONAL
```

## Non-negotiables

- **PNG-embedded refusal is absolute.** Any `<img src="*.png">` or `data:image/png;base64,...` in the diagram region → abort with the standard message. No OCR.
- **`.bak` is always created before overwrite.** On validation failure, the `.bak` is restored atomically — the user's original file is never destroyed.
- **MVP limit is surfaced, not silenced.** Every invocation prints the "full re-emission" disclaimer alongside the diff summary. Users who need surgical patching are pointed at `/amw-sketch` + `/amw-ascii-to-html` fresh.
- **The IR is the pivot.** Even ASCII→ASCII sync goes through IR so the diff summary works uniformly.
- Inherits the three hard rules from `../amw-design-principles/SKILL.md` via the `/amw-ascii-to-html` hand-off (tokens, variants on the greenfield path, AI-slop gate).

## Cross-references

- `../amw-diagram-formats/references/modify-flow.md` — shared 6-step pipeline (§7.1 documents the webpage-sync composition).
- `../amw-diagram-formats/references/ir-schema.md` — IR schema consumed.
- `../amw-diagram-formats/references/html.md` — HTML format spec used by the re-emit step.
- `../amw-ascii-to-html/SKILL.md` — terminal step of the re-emit pipeline.
- `../amw-webpage-to-diagram/SKILL.md` — forward-leg pair.
- `../../bin/amw-html-diff.py` — HTML structural diff (this skill's dedicated tool).
- `../../bin/amw-diagram-ir.py` — IR parse / emit / diff / validate CLI.
- `../../bin/amw-parse-html-diagram.py` — parses the old HTML page to IR.
- `../../bin/amw-validate-diagram.sh` — unified validator dispatcher.
- `../amw-design-principles/SKILL.md` — orchestrator.

## Related commands

- `/amw-modify-webpage-from-diagram` — primary entry point for this skill.
- `/amw-modify-diagram-of-webpage` — MVP round-trip: chains `webpage-to-diagram` + user-edit pause + this skill on `apply`.
- `/amw-create-webpage-from-diagram` — greenfield sibling.
