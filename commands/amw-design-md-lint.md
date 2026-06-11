---
name: amw-design-md-lint
description: "Validate a DESIGN.md against the official @google/design.md spec — frontmatter shape, section order, token-reference resolution, type rules. Runs bin/amw-design-md-lint.sh (which wraps `npx @google/design.md lint`) plus bin/amw-design-md-validate.py for offline pure-Python validation. Used as the gate before Phase B kicks in."
---

# /amw-design-md-lint

Lint a DESIGN.md against the canonical Variant 1 spec. Two-pass:

1. **Official linter** (`npx @google/design.md lint`) — wraps the Bun-based reference implementation. Catches frontmatter shape, section order, token reference resolution, and type rule violations.
2. **Offline validator** (`bin/amw-design-md-validate.py`) — pure-Python pass for when `npx` is unavailable. Validates frontmatter + section order + token-reference resolution.

## Arguments

`$ARGUMENTS` should contain a DESIGN.md path (default: `./DESIGN.md`):

- `<path-to-DESIGN.md> [--offline]`

If `--offline` is passed, skip the `npx` linter and only run the Python validator. Use when the network is unavailable or `npx` is not on PATH.

## Action

### 1. Run the official linter

```bash
bash bin/amw-design-md-lint.sh "<path>"
```

The wrapper invokes `npx @google/design.md lint <path>` and parses output into `PASS` / `FAIL: <line>: <severity>: <msg>` lines. Exit code 0 = PASS.

### 2. Run the offline validator (always)

```bash
python3 bin/amw-design-md-validate.py "<path>"
```

The validator is a structural check: frontmatter at line 1, section order matches canonical, every `{path.to.token}` reference resolves, dimensions use `px|em|rem`, fontWeight is 100–900.

### 3. Aggregate

Combine both outputs into a single report:

- **P0 (BLOCKER)** — frontmatter malformed, required key missing, section out of order, duplicate section heading, unresolved token reference.
- **P1 (MAJOR)** — invalid type for a value (color not `#RRGGBB`, dimension missing unit, fontWeight out of range).
- **P2 (MINOR / WARN)** — recommended-token name mismatch, contrast warning (if `--contrast` was passed), CJK-typography rule violations (if applicable).

### 4. Exit behavior

- Both passes report PASS → exit 0, surface `PASS` line.
- Either pass reports a P0 → exit non-zero with the consolidated error list. The caller should treat this as a blocker before Phase B.
- Only P2 warnings → exit 0, but surface warnings as the lint report.

## Non-negotiables

- **Lint failure halts Phase B.** A DESIGN.md that fails lint cannot be passed to wireframe-builder, accessibility-auditor, or any downstream agent. Either fix the file or stop.
- **Both passes run by default.** They catch overlapping but non-identical issues — npx catches official-spec semantics, Python catches structural breakage that survives parser leniency.
- **Never auto-fix silently.** Auto-fix is the author/extractor agents' job, not the lint command.

## Failure modes

- `npx` unavailable → fall back to Python-only with a warning. Recommend `npm install -g npx` or pass `--offline`.
- File not found → exit non-zero with `FAIL: <path>: file not found`.
- File is not Variant 1 (no YAML frontmatter, looks like Variant 2 community format) → exit non-zero with `FAIL: <path>: appears to be Variant 2 community 9-section. Use /amw-design-md-convert to convert to Variant 1 first.`

## Cross-references

- [TECH-11-validation-and-lint](../skills/amw-design-md/references/TECH-11-validation-and-lint.md)
> [TECH-11-validation-and-lint.md] What it does · The three validators · Official linter (`bin/amw-design-md-lint.sh`) · Pure-Python offline validator (`bin/amw-design-md-validate.py`) · Contrast checker (`bin/amw-design-md-contrast.py`) · Standard validation chain · Lint failure → recovery · Diff between two DESIGN.md files · CI integration suggestion (out-of-scope but documented) · Cross-references
- [TECH-14-validation-failure-recovery](../skills/amw-design-md/references/TECH-14-validation-failure-recovery.md)
> [TECH-14-validation-failure-recovery.md] What it does · Recovery flowchart · Failure categories · Structural failures (S* — P0, must fix before delivery) · Token-quality failures (T* — P1, must fix before final delivery) · Reference failures (R* — P0) · Accessibility failures (A* — P0 for body text, P1 for others) · Content-integrity failures (C* — P2, warn only) · Iteration cap · What recovery does NOT do · Manual recovery flow for users · Cross-references
- `bin/amw-design-md-lint.sh`
- `bin/amw-design-md-validate.py`
- `bin/amw-design-md-contrast.py` (separate command — see `/amw-design-md-audit`)
