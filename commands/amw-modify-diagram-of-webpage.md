---
name: amw-modify-diagram-of-webpage
description: "Shortcut for users who want to extract, edit, and re-emit a diagram from an existing webpage directly — full round-trip in two phases. An agent in Main-agent mode may also invoke the webpage-to-diagram + diagram-webpage-sync pipeline via the orchestrator after Phase A approval, applying additional sync and surgical techniques the skills expose."
---

# /amw-modify-diagram-of-webpage

**Two-phase command.** Phase 1: extract the diagram from the webpage and save it in the target format. Phase 2: on user `apply`, re-run the modify-webpage-from-diagram command with the edited diagram.

This MVP is **read-only** on phase 1 and a **full re-emit** on phase 2. No new backing skill — the extract leg reuses `skills/amw-webpage-to-diagram/`, and the re-emit leg reuses `skills/amw-diagram-webpage-sync/` via `/amw-modify-webpage-from-diagram`.

## Arguments

```
/amw-modify-diagram-of-webpage <webpage-path-or-url>
    [--target-format <ascii|svg|mermaid>]
    [--out-diagram <path>]
    [--out-webpage <path>]
```

- `<webpage-path-or-url>` — **required.** A URL (`http(s)://`) or a local `.html` file.
- `--target-format` — diagram format to extract. `ascii` (default), `svg`, or `mermaid`. `html` is rejected as a no-op.
- `--out-diagram <path>` — where to save the extracted diagram. Default: `<webpage-stem>.<ext>` in the user's working directory (`<ext>` = `.ascii` for ascii / `.svg` / `.mmd`).
- `--out-webpage <path>` — output path for the re-emitted webpage (phase 2). Default: overwrite `<webpage>` (local only — URL inputs REQUIRE `--out-webpage`).

## MVP limits (explicit, per plugin directive 2026-04-22)

- **This MVP re-emits the full webpage on `apply`.** Full DOM-surgical sync-back (preserving original CSS / JS / non-diagram content) is **DEFERRED** to a future phase. If you rely on manual styling outside the diagram region, prefer `/amw-sketch` + `/amw-ascii-to-html` fresh.
- **PNG-embedded diagrams are refused** at both ends of the round-trip:
  - Phase 1: if the webpage's diagram region is `<img src="*.png">` or `data:image/png;base64,...`, extraction is refused with `REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact`.
  - Phase 2: the same refusal re-applies from `/amw-modify-webpage-from-diagram`.
- **URL inputs require `--out-webpage`** for phase 2 — we can't overwrite a remote page. Local file inputs default to overwriting the original (with automatic `.bak`).

## Pipeline

### Phase 1 — Extract

1. **PNG gate.** If `<webpage-path-or-url>` is a PNG file or the URL returns `Content-Type: image/*`, exit 2 with the standard PNG refusal.
2. **Dispatch to `/amw-create-diagram-from-webpage`** with the requested target format:
   ```
   /amw-create-diagram-from-webpage <webpage> --to <target-format> --out <out-diagram>
   ```
   This chains `skills/amw-webpage-to-diagram/SKILL.md`: detect mime → refuse PNG → fetch HTML via `bin/amw-dev-browser-wrapper.sh` → `bin/amw-dom-to-ir.py` → `bin/amw-diagram-ir.py emit --format <target>` → `bin/amw-validate-diagram.sh`.
3. **Save** to `<out-diagram>`. Announce the path and the IR summary (nodes + edges count).
4. **PAUSE.** Surface:
   > *"Diagram saved to `<out-diagram>`. Edit it in your preferred tool (ASCII editor, Inkscape for SVG, or any Mermaid live editor). When you're done, say `apply` to re-emit the webpage from the edited diagram."*
   The skill does NOT auto-watch the file, does NOT auto-refresh. The user has to explicitly say `apply` or re-invoke the command with `--apply`.

### Phase 2 — Apply

1. **Re-detect** the diagram format at `<out-diagram>` (user may have saved in a different format).
2. **PNG-embedded gate (re-check).** If the user opened the webpage and the diagram region is now PNG-embedded (shouldn't happen but defensive), refuse.
3. **Dispatch to `/amw-modify-webpage-from-diagram`:**
   ```
   /amw-modify-webpage-from-diagram <webpage> <out-diagram> --out <out-webpage>
   ```
   The re-emit leg handles backup to `.bak`, IR-level diff, full re-emission via `/amw-ascii-to-html`, HTML-level diff via `bin/amw-html-diff.py`, and the final validation.
4. **Report** both diffs (IR-level and HTML-level) + the `.bak` location.

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | Phase 1 saved the diagram OR Phase 2 re-emitted the webpage successfully. |
| 1 | Fetch / parse / validate FAIL. |
| 2 | PNG refusal (either phase), bad input format, missing file, or URL input without `--out-webpage` for Phase 2. |
| 3 | Missing runtime dep (run `/amw-doctor` / `/amw-init`). |

## Cross-references

- `skills/amw-webpage-to-diagram/SKILL.md` — Phase 1 backing skill.
- `skills/amw-diagram-webpage-sync/SKILL.md` — Phase 2 backing skill.
- `skills/amw-diagram-formats/references/modify-flow.md` — §7.2 documents this composition.
- `/amw-create-diagram-from-webpage` — Phase 1 command.
- `/amw-modify-webpage-from-diagram` — Phase 2 command.
- `bin/amw-dom-to-ir.py`, `bin/amw-diagram-ir.py`, `bin/amw-html-diff.py`, `bin/amw-validate-diagram.sh` — backing tools.
- `/amw-sketch` + `/amw-ascii-to-html` — alternative when manual styling preservation matters.
