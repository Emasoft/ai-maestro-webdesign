---
name: amw-create-webpage-from-diagram
description: "Shortcut for users who have an existing diagram (ASCII/SVG/Mermaid) and want to build a webpage from it directly — chains IR conversion + ascii-to-html. An agent in Main-agent mode may also invoke the diagram-webpage-sync pipeline via the orchestrator, applying responsive design and token-application techniques beyond what this command covers."
---

# /amw-create-webpage-from-diagram

Thin wrapper — no new backing skill. Chains `bin/amw-diagram-detect-format.sh` + (optionally) `bin/amw-diagram-ir.py parse|emit` + `/amw-ascii-to-html` to turn any diagram source into a responsive single-file HTML page.

## Arguments

```
/amw-create-webpage-from-diagram <diagram-path> [--out <html-path>]
```

- `<diagram-path>` — **required.** Path to a diagram file in ASCII / SVG / Mermaid format. PNG is refused (see below).
- `--out <path>` — output `.html` path. Default: `<diagram-stem>.html` in the same directory.

## Dispatch

1. **Detect source format.** Run `bin/amw-diagram-detect-format.sh <diagram-path>` → `src_fmt`.
2. **PNG refusal.** If `src_fmt == "png"` → exit 2 with `REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact (ASCII / HTML / SVG / Mermaid)`.
3. **HTML shortcut.** If `src_fmt == "html"` → print hint: *"Source is already HTML. Use `/amw-modify-webpage-from-diagram` to modify it, or open it directly."* Exit 0.
4. **Convert to ASCII (if needed).**
   - If `src_fmt == "ascii"` → skip conversion; pass `<diagram-path>` directly to `/amw-ascii-to-html`.
   - Else (`svg`, `mermaid`) → run the two-step IR chain:
     ```
     bin/amw-diagram-ir.py parse  --in <diagram-path> --out /tmp/amw-mkpage-<hash>-ir.json
     bin/amw-diagram-ir.py emit   --in /tmp/amw-mkpage-<hash>-ir.json --format ascii --out /tmp/amw-mkpage-<hash>.ascii
     ```
     Validate the intermediate ASCII with `bin/amw-validate-ascii.py /tmp/amw-mkpage-<hash>.ascii`. FAIL → abort and surface the validator FIX hints.
5. **Hand off to `/amw-ascii-to-html`.** Invoke `/amw-ascii-to-html <ascii-path>` with the (original or converted) ASCII. That command handles the tokens prompt, chrome selection, Tweaks block, React/Babel pins, and AI-slop gate. The final `.html` is written to `<--out>` if supplied, otherwise the default `/amw-ascii-to-html` output path.
6. **Report.** On success: print both the intermediate ASCII path (for user inspection) and the final `.html` path. Also print the known-lossiness note (§ below).

## Known lossiness (diagram → IR → ASCII → HTML chain)

Per [ir-schema](skills/amw-diagram-formats/references/ir-schema.md) §5 lossy-conversion table, the round-trip through IR loses styling information that the ASCII renderer can't represent:

| Source format | Lost on the diagram-path-to-webpage trip |
|---|---|
| **SVG** | `<filter>` chains, multi-stop gradients beyond the primary palette, embedded fonts, clip-paths, masks, patterns. The ASCII intermediate is monochrome and text-only, so any visual styling is regenerated from the user's design tokens at the `/amw-ascii-to-html` step. |
| **Mermaid** | Config directives (`%%{init: ...}%%`), theme variables, interaction `click`/`linkStyle` rules, `classDef` styles. These are reconstructed via the `/amw-ascii-to-html` token application step. |
| **ASCII** | No IR round-trip — passthrough. The only loss is the one documented in `modify-flow.md` §5.1 (hand-authored ASCII that doesn't parse cleanly falls through to raw-source stub). |

For pixel-perfect retention of SVG/Mermaid styling, **do not use this chain** — instead use `/amw-convert-any-diagram-format --to html` (which wraps the SVG in a minimal HTML stub rather than rebuilding it from ASCII).

## Satisfaction gate inheritance

`/amw-ascii-to-html` enforces the satisfaction-token gate at the final step (`yes`, `ship it`, `convert it`, `that's the one`, `perfect`, `done`). This command inherits that gate — if the intermediate ASCII is not approved, the HTML is NOT written.

When running non-interactively (batch mode), invoke `/amw-ascii-to-html` directly with the ASCII path as the sole argument — the command treats a directly-supplied ASCII path as pre-approved (the user MUST have already inspected the diagram and confirmed).

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | Conversion + HTML emission succeeded. |
| 1 | Conversion step or final HTML validation FAIL. |
| 2 | PNG refusal, HTML shortcut hit, or unknown source format. |
| 3 | Missing runtime dep (run `/amw-doctor` / `/amw-init`). |

## Cross-references

- [SKILL](skills/amw-ascii-to-html/SKILL.md) — final HTML emission step.
- [ir-schema](skills/amw-diagram-formats/references/ir-schema.md) — lossy-conversion table.
- [conversion-matrix](skills/amw-diagram-formats/references/conversion-matrix.md) — canonical N×N routing rules.
- `bin/amw-diagram-detect-format.sh`, `bin/amw-diagram-ir.py`, `bin/amw-validate-ascii.py` — backing tools.
- `/amw-ascii-to-html` — terminal step.
- `/amw-convert-any-diagram-format` — alternative when SVG→HTML direct-wrap is desired (no re-ASCII round-trip).
- `/amw-modify-webpage-from-diagram` — pair command for editing an existing webpage from a new diagram.
