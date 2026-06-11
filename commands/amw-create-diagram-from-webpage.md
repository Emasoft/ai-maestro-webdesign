---
name: amw-create-diagram-from-webpage
description: "Shortcut for users who want to extract a structural diagram from a specific webpage or URL directly — emits ASCII (default), SVG, or Mermaid. An agent in Main-agent mode may also invoke skills/amw-webpage-to-diagram/ directly via the orchestrator, applying landmark detection and edge-extraction techniques the skill exposes beyond this command's parameters."
---

# /amw-create-diagram-from-webpage

Thin dispatcher over `skills/amw-webpage-to-diagram/`. Given a URL or local `.html` file, extracts the page's structural skeleton (HTML5 landmarks + internal anchors + inline SVGs), routes it through the diagram IR, and emits the result in the chosen target format.

## Arguments

```
/amw-create-diagram-from-webpage <url|path> [--to <ascii|svg|mermaid>] [--out <path>]
```

- `<url|path>` — **required.** Either an `http(s)://` URL or a local file path ending in `.html`/`.htm`.
- `--to <target>` — target format. One of `ascii` (default), `svg`, `mermaid`. HTML is a no-op and is rejected with a hint to use the input directly.
- `--out <path>` — output file path. Default: `<input-stem>.<target-ext>` in the user's working directory. `<input-stem>` is the URL's last path component (slugified) or the HTML basename.

## Dispatch

1. **Classify input.** URL (scheme `http(s)://`) → URL path; otherwise local file path → local path.
2. **PNG gate.** If input ends in `.png` OR (URL HEAD returns `Content-Type: image/*`) OR (local file magic is PNG) → exit 2 with `REFUSE: PNG-embedded diagram cannot be modified — provide the source artifact`.
3. **HTML-target shortcut.** If `--to html` → print a hint: *"Target format HTML is a no-op — the input already is HTML. Use `/amw-modify-webpage-from-diagram` if you want to modify it from a diagram."* Exit 0.
4. **Target default.** If `--to` is omitted → default to `ascii` (pair-able with `/amw-modify-diagram-of-webpage` for round-trip editing).
5. **Extract.** Invoke [SKILL](../skills/amw-webpage-to-diagram/SKILL.md) pipeline (steps 1–7): detect mime → refuse PNG → fetch HTML via `bin/amw-dev-browser-wrapper.sh` (URL) or read local → `bin/amw-dom-to-ir.py --in <html> --out /tmp/amw-page-<hash>.json --target-kind arch` → `bin/amw-diagram-ir.py emit --in <ir> --format <target> --out <out>` → `bin/amw-validate-diagram.sh <out>`.
6. **Report.** On PASS: print the output path and a one-line summary (nodes+edges count). On FAIL: leave the tentative output as `<out>.tentative` and surface the validator FIX hints verbatim.

## Output

- One file at `<out>`. Target-format validator must PASS before success is reported.
- Intermediate IR JSON is written to `/tmp/amw-page-<hash>.json` so the user can inspect or pipe it through `/amw-convert-any-diagram-format` for further conversions.

## Exit codes

| Exit | Meaning |
|---|---|
| 0 | Extraction + emission succeeded, target validates. |
| 1 | Fetch/parse error (URL unreachable, malformed HTML, validator FAIL). |
| 2 | PNG refusal OR unknown target format. |
| 3 | Missing runtime dep (run `/amw-doctor` / `/amw-init`). |

## Cross-references

- [SKILL](../skills/amw-webpage-to-diagram/SKILL.md) — primary backing skill.
- [html](../skills/amw-diagram-formats/references/html.md) — HTML format spec.
> [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22)
- [ir-schema](../skills/amw-diagram-formats/references/ir-schema.md) — IR schema produced.
> [ir-schema.md] Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Validation · Consumers
- `bin/amw-dom-to-ir.py`, `bin/amw-diagram-ir.py`, `bin/amw-validate-diagram.sh` — backing tools.
- `/amw-modify-diagram-of-webpage` — chains this command with a user-edit pause, then `/amw-modify-webpage-from-diagram` on apply.
- `/amw-convert-any-diagram-format` — use when you want further format conversion on the extracted IR.
