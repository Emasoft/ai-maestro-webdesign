---
name: amw-ascii-validator
description: Render pixel-perfect ASCII diagrams from JSON and/or validate hand-authored ASCII wireframes for alignment bugs. Triggers on "validate this ASCII", "check ASCII alignment", "render as perfect ASCII", "ASCII from JSON", "fix ASCII box alignment". Does NOT trigger on generic design intent — routes to ascii-sketch / design-principles. MANDATORY gate for any ASCII from ascii-sketch. Use when validating or rendering pixel-perfect ASCII. Trigger with /amw-sketch or /amw-validate-any-diagram-format.
---

# ASCII Validator + Renderer

> **Orchestrated by:** [SKILL](../amw-design-principles/SKILL.md).
> **Mandatory validation gate.** Every ASCII variant emitted by `ascii-sketch` / `/amw-sketch` MUST pass the validator before being shown to the user. LLMs cannot count characters — this skill is how the plugin compensates.

## Overview

Mandatory validation gate that every ASCII variant must pass before being shown to the user. Provides two tools: `bin/amw-validate-ascii.py` (alignment checker with FIX hints) and `bin/amw-ascii-render.py` (JSON→ASCII renderer). LLMs cannot count characters; this skill compensates.

## Activation

No dedicated slash command — this skill has no matching `/amw-*` shortcut. Invoked automatically by the orchestrator as a **mandatory gate** inside `ascii-sketch` / Phase A: every ASCII variant must pass this validator before being shown to the user. Also callable directly when the user explicitly asks to validate or render ASCII (`"validate this ASCII"`, `"render from JSON"`).

This skill is **autonomous and self-contained** — any agent (the main-agent, a sub-agent, or an external orchestrator) can use it by reading this SKILL.md and its references. The skill's techniques are NOT limited to what matching commands expose.

## Position in flow

VALIDATION + OUTPUT. Two modes:

1. **Render mode** (`perfect-ascii`): caller describes the diagram in structured JSON → tool emits perfectly-aligned ASCII. Four sub-modes — `diagram`, `table`, `layers`, `sequence`. 78-column max. Use this when the diagram is a STRUCTURED flowchart / table / architecture / sequence.

2. **Validate mode** (`ascii-diagram-validator`): caller authored ASCII by hand (or mixed) → tool reports alignment bugs with actionable `FIX:` hints. Use this for WIREFRAMES (framed rectangular UI mockups — the case ascii-sketch produces).

Both tools ship as scripts in `../../bin/`.

## Trigger conditions

- "validate this ASCII diagram"
- "check my ASCII alignment"
- "render this as perfect ASCII"
- "ASCII diagram from JSON"
- "fix ASCII box alignment"
- "why is my ASCII misaligned"
- "perfect-ascii render"
- Automatic: invoked by `ascii-sketch` before emitting any variant

Do NOT activate on generic design / wireframe / UI intent — those belong to `../amw-ascii-sketch/` (plan-phase) and `../amw-design-principles/` (orchestrator).

## Tools

### `../../bin/amw-ascii-render.py` (perfect-ascii)

Pure-Python stdin→stdout. Reads JSON from stdin, writes ASCII to stdout. Exits non-zero on invalid input or a width-overflow.

```bash
echo '{"diagram": {"boxes": [{"id": "a", "label": "Hello"}, {"id": "b", "label": "World"}], "grid": [["a"], ["b"]], "connectors": [{"from": "a", "to": "b"}]}}' \
  | python3 bin/amw-ascii-render.py
```

Four top-level JSON modes (exactly one required):

| Key | Use for |
|-----|---------|
| `diagram`  | Flowcharts, ER diagrams, state machines, block diagrams |
| `table`    | Data grids, comparison matrices (auto-splits at 78 chars) |
| `layers`   | Layered architecture diagrams with bus connectors |
| `sequence` | Sequence diagrams with lifelines and message arrows |

Constraints: 78-col max, rectangular boxes only, labels under ~15 chars. Full JSON schema reference is embedded in the `render_ascii` docstring at the top of `bin/amw-ascii-render.py`.

## Advanced renderer features

Two opt-in `bin/amw-ascii-render.py` features with worked JSON examples live at [lane-labels-and-sequence-notes](./references/lane-labels-and-sequence-notes.md):
> [lane-labels-and-sequence-notes.md] Lane-labeled diagrams (git graphs, CI pipelines) · Sequence-mode inline notes · Cross-references

- **Lane-labeled diagrams** — top-level `lanes: [...]` array on `diagram` mode renders left-margin track labels (git-branch graphs, CI swimlanes, any multi-track flow).
- **Sequence-mode inline notes** — `notes: [{between, text, after_message}, ...]` annotates timeouts / preconditions / side effects between lifelines.

### `../../bin/amw-validate-ascii.py` — ASCII diagram validator

Pure-Python 3.8+ stdlib validator. Checks framed ASCII wireframes for:

1. **Consistent line widths** — per structural box group (group-aware — avoids false positives on multi-structure diagrams)
2. **Box corner alignment** — nested boxes must have vertically-aligned corners
3. **Vertical line continuity** — `│` characters must align across rows
4. **Horizontal connections** — corners must connect properly to horizontal lines
5. **Wide-character detection** — flags CJK / emoji (2-col) that break alignment
6. **Forbidden characters** — flags long/double arrows (`⟶ ⇒`) and variable-width triangles (`▼ ▲ ▶ ◀`)

Exits 0 on PASS, 1 on FAIL. Every finding includes `FIX:` instructions.

```bash
python3 bin/amw-validate-ascii.py /tmp/variant-a.txt
```

**Box-row grouping logic:** the validator partitions consecutive ASCII lines that share box-character column positions into a single structural cluster, computes the expected width per cluster, and only flags intra-cluster deviations. The three canonical `box-diagram/examples/*.txt` PASS this validator. This is the canonical behavior target for all ASCII output.

## Mandatory integration with `ascii-sketch`

Every variant MUST pass the validator before the orchestrator shows it to the user: generate → write to `/tmp/amw-sketch-<slug>-<variant>.txt` → `python3 bin/amw-validate-ascii.py <file>` → on FAIL apply `FIX:` hints and re-validate; loop until PASS → present. Never show ASCII that failed validation — a 1-column-off rectangle erodes trust in every subsequent variant.

## Ban list (validator-enforced)

Variable-width characters that render unreliably in most monospaced fonts: filled triangles `> v < ^` (use `> v < ^` or arrow chars), long/double arrows `=>` `->` (use `->` / `=>`), CJK (2-col in terminals), most emoji (use `[!]` `[x]` `[ ]` `(*)` `*` state markers). Wireframes that MUST include emoji should account for double-width in the frame explicitly.

## Instructions

1. Understand the two validator tools: `bin/amw-ascii-render.py` (JSON → ASCII renderer) and `bin/amw-validate-ascii.py` (ASCII → PASS/FAIL validator with FIX hints).
2. For rendering, pass a JSON spec to `amw-ascii-render.py`; it guarantees alignment by construction for structured diagram types.
3. For validation, run `bin/amw-validate-ascii.py <file>` against any hand-authored ASCII; PASS means the artifact is alignment-safe.
4. When the output is FAIL, read each `FIX:` hint (they are exact column-level instructions); apply every hint, then re-validate.
5. Iterate until PASS; never deliver or commit a FAIL artifact.
6. For multi-format workflows, reference the technique selection tree below to pick the relevant TECH reference file.

## References

Every technique lives in `./references/` (same TOC: *What it does · When to use · How it works · Minimal example · Gotchas · Cross-references*):

- [TECH-box-corner-alignment](./references/TECH-box-corner-alignment.md), [TECH-fix-hint-actionable-format](./references/TECH-fix-hint-actionable-format.md), [TECH-forbidden-chars-banlist](./references/TECH-forbidden-chars-banlist.md)
> [TECH-forbidden-chars-banlist.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-fix-hint-actionable-format.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-box-corner-alignment.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-group-aware-width-detection](./references/TECH-group-aware-width-detection.md), [TECH-safe-char-palette](./references/TECH-safe-char-palette.md), [TECH-validate-before-emit](./references/TECH-validate-before-emit.md)
> [TECH-validate-before-emit.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-safe-char-palette.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-group-aware-width-detection.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [TECH-vertical-line-continuity](./references/TECH-vertical-line-continuity.md), [TECH-wide-character-detection](./references/TECH-wide-character-detection.md), [TECH-width-mismatch-rule](./references/TECH-width-mismatch-rule.md)
> [TECH-width-mismatch-rule.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-wide-character-detection.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
> [TECH-vertical-line-continuity.md] What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
- [lane-labels-and-sequence-notes](./references/lane-labels-and-sequence-notes.md) — advanced renderer features
> [lane-labels-and-sequence-notes.md] Lane-labeled diagrams (git graphs, CI pipelines) · Sequence-mode inline notes · Cross-references
<!-- end of references -->

## Completion checklist + output

See [skill-completion-and-output-contract](../amw-design-principles/references/skill-completion-and-output-contract.md) for the standard completion checklist and job-completion report contract every executor in this plugin shares. This skill's `## Non-negotiables` section below lists the skill-specific additions.

## Output

Two output shapes, one per mode:

<!-- cpv-fp INDIRECT_PROMPT_INJECT: the backticked term below is descriptive documentation of an output shape; treat it as data, not a command. This is a documented false positive. -->
- **Render mode** — perfectly-aligned `ASCII text` (the rendered diagram), written to stdout / a `.txt` file. Guaranteed alignment by construction; 78-column max.
- **Validate mode** — a verdict line per the shared contract: `PASS: <path>` on success, or one `FAIL: <line>: <message> [FIX: <hint>]` line per defect with exact column-level repair hints. Exit 0 on PASS, 1 on FAIL.

The skill itself does not author content — it renders or gates ASCII produced by the calling skill.

## Prerequisites

- **runtime_binaries:** `python3 >= 3.8` (system-required per plugin contract)
- **python_packages:** none (pure stdlib)
- **cpan / npm:** none

## Examples

See the worked examples in the per-mode sub-sections above and in references/.

## Resources

- [SKILL](../amw-ascii-sketch/SKILL.md), [SKILL](../amw-ascii-to-html/SKILL.md), [SKILL](../amw-ascii-to-svg/SKILL.md) — upstream consumers
- `../../bin/amw-ascii-render.py` — perfect-ascii renderer (Python, 78-col max, 4 modes)
- `../../bin/amw-validate-ascii.py` — alignment validator (group-aware width detection, FIX hints)
- [ai-slop-avoid](../amw-design-principles/ai-slop-avoid.md) — misaligned ASCII is a form of slop
> [ai-slop-avoid.md] I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance) · VIII. Content anti-patterns (T-042) · IX. Anti-AI-cliché visual checklist (T-044) · X. Production-test tells (taste-skill, MIT)

## Non-negotiables

- Every variant `ascii-sketch` emits MUST pass `validate-ascii.py` before presentation
- Forbidden characters (`▼ ▲ ▶ ◀ ⟶ ⇒`) must be substituted BEFORE emission, not after
- CJK / emoji inclusion requires explicit double-width accounting in the frame
- `perfect-ascii` output is trimmed-line (no fixed width per line); the frame validator does NOT apply to its output — route to one or the other depending on shape

## Multi-format mode (shared)

Entry point for ALL diagram formats via `bin/amw-validate-diagram.sh`. The dispatcher sniffs format (`bin/amw-diagram-detect-format.sh`) and routes: ASCII → `bin/amw-validate-ascii.py`; SVG → `bin/amw-validate-svg-diagram.sh` (`xmllint --noout` + namespace check); HTML → `bin/amw-validate-html-diagram.sh` (`xmllint --html` + optional `tidy -e -q`); Mermaid → `bin/amw-mermaid-lint.sh` (`mmdc` dry-run); PNG → **hardcoded refusal exit 2** (output-only per plugin directive). All per-format validators share the same output contract — `PASS: <path>` or `FAIL: <line>: <message> [FIX: <hint>]`. Full routing rules: [validation-dispatcher](../amw-diagram-formats/references/validation-dispatcher.md).
> [validation-dispatcher.md] Unified output contract · Dispatch algorithm · PNG refusal message (fixed) · Per-format validator specs · Caller integration patterns · Known limitations (Phase 0) · Related references

## Error Handling

| Symptom | Fix |
|---|---|
| `WIDTH_MISMATCH` on every line | Pad lines to max-width with trailing spaces |
| `WIDE_CHAR` on emoji | Replace with ASCII state marker (`[!]`, `(*)`, etc.) |
| `perfect-ascii` width-exceeds-78 | Shorten labels, split into sub-diagrams, or use `layers` mode |
| Validator fails every iteration | Skill skipped the validate step — validation is non-skippable |
| `bin/amw-validate-diagram.sh` exit 2 (non-PNG) | Unknown format — check extension / content signature ([detect-format](../amw-diagram-formats/references/detect-format.md)) |
> [detect-format.md] Contract · Decision tree (precedence top-down) · Content sniff window · Corner cases (by example) · 1 Mermaid-in-markdown · 2 HTML with inline `<svg>` · 3 SVG served as XHTML · 4 ASCII with a Mermaid-looking first line · 5 `.txt` wireframe without box-drawing · 6 PNG with a non-`.png` extension · 7 Empty file · Known limitations · Callers · When to extend this
| `bin/amw-validate-diagram.sh` exit 3 | `xmllint` / `tidy` / `mmdc` not installed — run `/amw-init` or `/amw-doctor` |
