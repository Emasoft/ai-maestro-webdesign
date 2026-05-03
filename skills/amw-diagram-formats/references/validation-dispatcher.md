## Table of Contents

- [1. Unified output contract](#1-unified-output-contract)
- [2. Dispatch algorithm](#2-dispatch-algorithm)
- [3. PNG refusal message (fixed)](#3-png-refusal-message-fixed)
- [4. Per-format validator specs](#4-per-format-validator-specs)
- [5. Caller integration patterns](#5-caller-integration-patterns)
- [6. Known limitations (Phase 0)](#6-known-limitations-phase-0)
- [7. Related references](#7-related-references)


# Validation dispatcher — `bin/amw-validate-diagram.sh`

**Authoritative spec for how the plugin validates ANY diagram**, regardless of format. Consumers: `/amw-validate-any-diagram-format`, every `wd-create-or-modify-*-diagram` command (post-emit gate), every conversion (post-conversion gate), and `ascii-validator/SKILL.md` (multi-format mode).

The dispatcher is `bin/amw-validate-diagram.sh`. It routes to one of the per-format validators below, then normalizes their output to a single contract.

## 1. Unified output contract

Every validator (ASCII, SVG, HTML, Mermaid) MUST conform to the following line-based output format:

```
PASS: <path>
```

OR (one line per finding; zero or more lines; exit 1 when non-empty):

```
FAIL: <line>: <message> [FIX: <hint>]
```

- `PASS` is emitted exactly once on success, with the full input path. Exit code `0`.
- `FAIL` lines each carry a **line number** (integer; `0` when no line info is available), a **message** (single line; the validator's own wording), and an optional `[FIX: <hint>]` suffix telling the caller how to fix the specific finding.
- PNG inputs are refused (not FAILed) with exit code `2` and a fixed message — see §3.
- Unknown / unrecognized inputs exit code `2` with an `UNKNOWN: ...` line.
- Tool-missing situations exit code `3`.

Exit code summary:

| Code | Meaning |
|---|---|
| 0 | PASS |
| 1 | FAIL (one or more findings) |
| 2 | PNG refusal OR unknown format |
| 3 | CLI misuse / missing tool |

## 2. Dispatch algorithm

```
1. validate-diagram.sh receives a path.
2. Call bin/amw-diagram-detect-format.sh <path> -> fmt.
3. Route:
     fmt == "ascii"    -> exec python3 bin/amw-validate-ascii.py <path>
                          (fall back: python3 bin/amw-validate-ascii.py <path>)
     fmt == "svg"      -> exec bin/amw-validate-svg-diagram.sh <path>
     fmt == "html"     -> exec bin/amw-validate-html-diagram.sh <path>
     fmt == "mermaid"  -> exec bin/amw-mermaid-lint.sh <path>
     fmt == "png"      -> print REFUSE message (§3); exit 2.
     fmt == "unknown"  -> print UNKNOWN message; exit 2.
```

The dispatcher uses `exec` so the per-validator's exit code propagates directly — no wrapping, no re-emission, no subshell overhead. Callers get the per-format validator's stdout / stderr verbatim.

## 3. PNG refusal message (fixed)

```
REFUSE: PNG is output-only by plugin directive; validate the source artifact instead.
        Provide the ASCII / HTML / SVG / Mermaid source that produced this PNG.
```

Exit code `2`. This message is reproduced verbatim by:

- `bin/amw-validate-diagram.sh` (top-level).
- `/amw-validate-any-diagram-format` (slash command).
- Any `wd-create-or-modify-*-diagram` command that rejects a PNG modify-target.

Do not localize, do not rephrase — the message is a grep anchor for downstream tooling.

## 4. Per-format validator specs

### 4.1 ASCII — `bin/amw-validate-ascii.py` (primary) and `bin/amw-validate-ascii.py` (fallback)

Already specified in [SKILL](../../amw-ascii-validator/SKILL.md). Relevant for this dispatcher:

- Checks: consistent widths, box corner alignment, vertical line continuity, horizontal connections, wide-character detection, forbidden characters.
- Exits 0 on PASS, 1 on FAIL.
- Output: already conforms to the unified contract — the Perl validator emits `PASS: file` or `FAIL: line N: <msg> [FIX: ...]`.
- Fallback: `bin/amw-validate-ascii.py` has identical CLI surface + identical exit codes + identical `FIX:` hint format. Use when Perl is unavailable (Windows, minimal containers).

### 4.2 SVG — `bin/amw-validate-svg-diagram.sh`

Wraps:

1. `xmllint --noout --nonet <path>` — XML well-formedness.
2. First-500-byte grep for `xmlns="http://www.w3.org/2000/svg"` — required namespace declaration.

Findings emitted by xmllint are re-formatted from its native `<path>:<line>: <msg>` format into `FAIL: <line>: <msg> [FIX: fix XML well-formedness (check tags/attrs/quoting)]`.

Missing namespace emits: `FAIL: 1: SVG namespace declaration missing in first 500 bytes [FIX: add xmlns="http://www.w3.org/2000/svg" to the root <svg> element]`.

### 4.3 HTML — `bin/amw-validate-html-diagram.sh`

Wraps:

1. `xmllint --html --noout --nonet <path>` — HTML well-formedness (lenient, HTML4-era parser; still catches unbalanced tags and malformed attrs).
2. `tidy -e -q -errors <path>` — optional. Emits warnings AND errors; the wrapper promotes both to `FAIL` lines so they're visible. If `tidy` is missing from PATH, this step is silently skipped (the wrapper still runs xmllint).

xmllint findings use the same re-format as SVG (§4.2). Tidy findings (line N column M - Error/Warning: <msg>) are re-formatted to `FAIL: <line>: tidy <msg> [FIX: ...]`.

Note: `xmllint --html` tolerates some HTML5-only constructs poorly (e.g. `<main>`). The wrapper does not filter these — the user should either fix the document to be HTML4-clean or rely on `tidy` for HTML5-aware linting. `/amw-doctor` checks whether `tidy` is installed.

### 4.4 Mermaid — `bin/amw-mermaid-lint.sh`

Wraps `mmdc -i <path> -o /tmp/<hash>.svg -q`. Exit 0 + non-empty SVG = PASS. Otherwise we parse stderr for `Error` / `SyntaxError` / `Parse error on line N:` patterns and emit up to **3 FAIL lines** (noisy mmdc outputs are truncated for sanity).

Each FAIL line: `FAIL: <line>: <mmdc message> [FIX: fix Mermaid grammar (diagram type / node syntax / arrow style)]`.

Banners / deprecation warnings / Puppeteer chatter are filtered out — they appear on stderr in many mmdc installs but are not diagnostic.

## 5. Caller integration patterns

### 5.1 Post-create gate

Every authoring skill runs the dispatcher as a LAST STEP before declaring success. Pseudo:

```bash
bin/amw-validate-diagram.sh "$OUTPUT_PATH"
code=$?
case "$code" in
  0) echo "OK: $OUTPUT_PATH passes validation." ;;
  1) echo "VALIDATION FAILED — see above. Apply FIX: hints and re-emit."; exit 1 ;;
  2) echo "Wrong format / PNG refusal."; exit 2 ;;
  3) echo "Validator tool missing — run /amw-doctor / /amw-init."; exit 3 ;;
esac
```

### 5.2 Post-convert gate

`/amw-convert-any-diagram-format` runs the dispatcher on the TARGET output. Conversion does not succeed unless the target format validates cleanly.

### 5.3 Modify-flow loop

[modify-flow](./modify-flow.md) specifies a validate step after the re-render. The dispatcher's output is the sole signal used to decide loop termination — if exit 0, done; if exit 1, re-patch and re-emit.

### 5.4 Multi-format mode (ascii-validator)

[SKILL](../../amw-ascii-validator/SKILL.md) carries a `## Multi-format mode` paragraph pointing at this file. The ASCII validator remains the primary interface for ASCII-only flows (ascii-sketch, `/amw-sketch`); this dispatcher is the entry point when the format is not yet known.

## 6. Known limitations (Phase 0)

- **HTML validation** is lenient — `xmllint --html` accepts many invalid-HTML5 constructs. `tidy` catches most of them but not all. Perfection-mode HTML validation would need a full HTML5 parser (e.g. `html-validate` npm) — deferred to Phase 2 if needed.
- **Mermaid parse error line numbers** are best-effort — mmdc's error messages sometimes lack a line number or refer to an internal AST position. The wrapper degrades gracefully to `FAIL: 0: <raw mmdc message>` when no line is available.
- **SVG semantic validation** (e.g. invalid path data, invalid color keywords, out-of-viewport elements) is NOT done. Only XML well-formedness + namespace. Brands that need stricter SVG checks should add their own validator and prepend it to the dispatch list.
- **No cross-format validation** — e.g. "this HTML's inline SVG has invalid path data" is a two-step check (validate the HTML first, extract the SVG, validate it separately). The dispatcher does not orchestrate this; callers that need it compose manually.

## 7. Related references

- [detect-format](./detect-format.md) — the sniffer whose output this dispatcher routes on.
  > Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this
- [ascii](./ascii.md) / [html](./html.md) / [svg](./svg.md) / [mermaid](./mermaid.md) — per-format specs (authored by the sibling `format-refs` agent).
  > [html.md] Format definition · Starter-components mapping · Tweaks protocol invariants (HARD RULES) · React / Babel pin rules · AI-slop-avoid gate (12-item checklist) · ARIA / keyboard / a11y patterns · CSS custom properties (Tweaks-compatible) · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · ai-slop-avoid · `../../amw-design-principles/starter-components/*` — all 9 canonical chrome components · color-system · typography-system · SKILL · SKILL · SKILL · SKILL · SKILL · `../../bin/amw-html-export.py` — HTML → PNG/PDF rasterizer (Playwright) · `../../bin/amw-ascii-parse.py` — ASCII → layout JSON consumed by HTML emitter · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
  > [svg.md] Format definition · Structural primitives (diagram-grade usage) · Viewport rules · Text rendering rules · Rasterization path · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · SKILL · SKILL · SKILL · SKILL · SKILL · advanced-techniques · `../../bin/amw-svg-render.py` — render-verify-finish loop (`render` / `finish` / `status` / `reset`) · ir-schema · conversion-matrix · png · validation-dispatcher
  > [mermaid.md] Format definition · Supported grammars · Themes · mmdc CLI flags (17 total) · Output paths · Validation · Per-source breakdown of the technique catalog · Technique catalog · Failure modes · Anti-patterns · SKILL · SKILL · SKILL · `../../external/mermaid-render/` — vendored beautiful-mermaid backend · `../../bin/amw-mermaid-render.sh` — shell wrapper (SVG / PNG / ASCII) · `../../bin/amw-mermaid-lint.sh` (planned; Task 0c) — validator wrapper (`mmdc` dry-run) · `../../bin/amw-validate-ascii.py` — warn-only gate on ASCII rendering · ir-schema · conversion-matrix · validation-dispatcher
  > Format definition · Dimensional constraints · Parse rules · Emission rules · Validation rules · Per-source breakdown of the technique catalog · Technique catalog · Migration note (2026-04-22) · SKILL · SKILL · SKILL · SKILL · SKILL · SKILL · `../../text-visual-{workflows,arch,state,cheatsheets,retro}/SKILL.md` — specialized ASCII archetypes · `../../bin/amw-ascii-parse.py` — tokenizer (IR input) · `../../bin/amw-ascii-render.py` — renderer (4 JSON modes) · `../../bin/amw-validate-ascii.py` — validator (Perl, mandatory gate) · `../../bin/amw-validate-ascii.py` — validator (Python mirror) · ir-schema · conversion-matrix · modify-flow · validation-dispatcher
  > Format definition · 1 Character repertoire · 2 Forbidden characters (validator rejects) · 3 State / status markers · Dimensional constraints · Parse rules · Emission rules · 1 Four JSON modes · 2 Key renderer invariants · Validation rules · 1 Checks · 2 Validation is MANDATORY before delivery · Per-source breakdown of the technique catalog · Technique catalog · S1 — box-diagram-master (gold examples) · S2 — ascii-diagrams-skill (CHI'24 refs, 7 files) · S3 — cc-plugin-text-visualizations (5 skills) · S4 — perfect-ascii (renderer) · S5 — diagram-skill styles (ASCII-STYLES.md) · S6 — baybee-diagram (SVG patterns with ASCII equivalents) · S7 — diagram-design-editorial (editorial) · S8 — Structural pairing rules (enforced by validator) · S9 — Cross-cutting style rules · Migration note (2026-04-22) · SKILL · SKILL · SKILL · SKILL · SKILL · SKILL · …(+9)
- [modify-flow](./modify-flow.md) — pipeline that closes the loop with this dispatcher.
  > The pipeline · Create vs modify dispatch · Step-by-step detail · Step 1 — Detect · Step 2 — Parse to IR · Step 3 — Patch · Step 4 — (loop point) · Step 5 — Emit · Step 6 — Re-validate · Work directory and file naming · Per-format guidance · 1 ASCII modify (MVP structural) · 2 HTML modify (MVP raw-source; Phase 1 structural) · 3 SVG modify (MVP raw-source; Phase 1 structural) · 4 Mermaid modify (MVP raw-source; Phase 1 structural) · Conversion is a modify-flow variant · Composition with round-trip skills · 1 `diagram-webpage-sync` (`/amw-modify-webpage-from-diagram`) · 2 `webpage-to-diagram` (`/amw-modify-diagram-of-webpage`) · Related references · `/amw-create-or-modify-ascii-diagram` → backed by `ascii-creator` · `/amw-create-or-modify-html-diagram` → backed by `html-diagram` · `/amw-create-or-modify-svg-diagram` → backed by `svg-diagram` · `/amw-create-or-modify-mermaid-diagram` → backed by `mermaid-diagram` · `diagram-webpage-sync` / `/amw-modify-webpage-from-diagram` · `webpage-to-diagram` / `/amw-modify-diagram-of-webpage`
- [ir-schema](./ir-schema.md) — note that IR validation is separate (use `bin/amw-diagram-ir.py validate`) — this document is about validating **rendered artifacts**, not IR JSON.
  > Top-level shape · `nodes` · Well-known annotations · Raw-source fast path (MVP) · Lossy-conversion matrix · Versioning policy · Example IRs · Minimal flowchart (3 nodes, 2 edges) · Sequence (two actors, one message + note) · Architecture (3 layers) · Raw-source stub (MVP HTML → IR) · Validation · Consumers
