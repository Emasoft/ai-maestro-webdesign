---
name: amw-design-md-convert
description: "Convert a Variant 2 (community 9-section) DESIGN.md into the canonical Variant 1 (official @google/design.md YAML + 8 prose sections) format. Pure-Python — no remote calls, no API key. Runs bin/amw-design-md-convert-v2-to-v1.py. After conversion, the result is automatically lint-checked."
---

# /amw-design-md-convert

Translate a community 9-section DESIGN.md (the format used by VoltAgent's pre-paywall corpus) into the canonical Variant 1 format with YAML frontmatter and the 8 fixed-order prose sections. Variant 1 is the format expected by the official `@google/design.md` linter and by every plugin agent that consumes DESIGN.md.

## Arguments

`$ARGUMENTS` should contain at minimum an input path:

- `<path-to-variant2.md> [--out <path>] [--no-lint]`

Optional flags:

- `--out <path>` — output Variant 1 DESIGN.md path (default: `<input-basename>.v1.md` next to the input)
- `--no-lint` — skip the post-conversion lint pass (default: lint runs automatically)

If no input path is provided, ask: *"Which DESIGN.md file should I convert?"* and stop.

## Action

### 1. Confirm the input is Variant 2

Read the first ~50 lines. If the file starts with `---` (YAML frontmatter), it is already Variant 1 — surface a message and stop. If the file starts with `# Design System Inspired by ...` followed by `## 1. ...` numbered sections, it is Variant 2 — proceed.

### 2. Run the converter

```bash
python3 bin/amw-design-md-convert-v2-to-v1.py "<input>" "<output>"
```

The converter:

- Walks each Variant 2 section in order (1. Visual Theme → 2. Color Palette → 3. Typography → 4. Components → 5. Layout → 6. Depth → 7. Do's/Don'ts → 8. Responsive → 9. Agent Prompt Guide).
- Emits a Variant 1 frontmatter block (`colors`, `typography`, `rounded`, `spacing`, `components`).
- Emits the 8 Variant 1 prose sections in the canonical order: Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts.
- Drops Variant 2 sections that have no Variant 1 home (Section 8 Responsive Behavior and Section 9 Agent Prompt Guide become appendices in the prose if present).

### 3. Lint the output (default)

Unless `--no-lint` was passed:

```bash
bash bin/amw-design-md-lint.sh "<output>"
```

If lint fails, surface the error list and recommend `/amw-design-md-audit <output>` for a deeper diagnosis.

### 4. Surface the result

- Output path
- Lint status (PASS / PARTIAL)
- A summary of what was preserved, transformed, or dropped during conversion (e.g., "Variant 2 Section 9 'Agent Prompt Guide' merged into Variant 1 Overview as appendix")

## Non-negotiables

- **Conversion is forward-only (V2 → V1).** A V1 → V2 path is not implemented; the canonical direction is V2 → V1.
- **Idempotent.** Running the converter on a Variant 1 file is a no-op (file unchanged), with a warning surfaced.
- **Lint after convert.** A converted file is not guaranteed to pass lint — the V2 source may have token-reference patterns that don't translate cleanly. Always lint.

## Failure modes

- Input is already Variant 1 → surface `WARN: input is already Variant 1; nothing to convert` and stop.
- Variant 2 file is malformed (missing required sections, broken section numbering) → converter exits non-zero with the parse error; surface and stop.
- Lint fails after conversion → surface the lint errors and recommend `/amw-design-md-audit` for a deeper read.

## Cross-references

- [TECH-13-converting-variant2-to-1](skills/amw-design-md/references/TECH-13-converting-variant2-to-1.md)
- [community-9-section-spec](skills/amw-design-md/references/community-9-section-spec.md)
- [canonical-spec-google-alpha](skills/amw-design-md/references/canonical-spec-google-alpha.md)
- `bin/amw-design-md-convert-v2-to-v1.py`
- `bin/amw-design-md-lint.sh`
