---
name: TECH-11-validation-and-lint
category: validation
source: design.md-main/packages/cli (npx @google/design.md), bin/amw-design-md-validate.py, bin/amw-design-md-contrast.py
also-in: TECH-01-yaml-frontmatter.md, TECH-14-validation-failure-recovery.md
status: stable
---

# TECH: Validation and lint

## Table of Contents

- [What it does](#what-it-does)
- [The three validators](#the-three-validators)
  - [1. Official linter (`bin/amw-design-md-lint.sh`)](#1-official-linter-binamw-design-md-lintsh)
  - [2. Pure-Python offline validator (`bin/amw-design-md-validate.py`)](#2-pure-python-offline-validator-binamw-design-md-validatepy)
  - [3. Contrast checker (`bin/amw-design-md-contrast.py`)](#3-contrast-checker-binamw-design-md-contrastpy)
- [Standard validation chain](#standard-validation-chain)
- [Lint failure → recovery](#lint-failure-recovery)
- [Diff between two DESIGN.md files](#diff-between-two-designmd-files)
- [CI integration suggestion (out-of-scope but documented)](#ci-integration-suggestion-out-of-scope-but-documented)
- [Cross-references](#cross-references)

## What it does

Documents the three validation tools the plugin runs on every authored or extracted DESIGN.md before delivery. All three must pass cleanly (or have failures explicitly accepted in the agent's `warnings`) before the file is considered final.

## The three validators

### 1. Official linter (`bin/amw-design-md-lint.sh`)

Wrapper around `npx @google/design.md lint <file>`. Pure-Node, no API key, no remote calls. The official linter implements the rules from [canonical-spec-google-alpha](canonical-spec-google-alpha.md):
> [canonical-spec-google-alpha.md] File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references

- Frontmatter starts at line 1 with `---`.
- YAML between delimiters is well-formed.
- Section headings follow canonical order (V1 only).
- No duplicate section heading.
- `colors.*` values are valid hex.
- `Dimension` values use px/em/rem.
- `fontWeight` values are integers 100-900.
- Token references match `\{[a-zA-Z0-9._-]+\}` and resolve.
- Component-property composite refs allowed only inside `components.*`.
- WCAG-AA contrast warnings (informational; not errors).

Usage:
```bash
bash <plugin-root>/bin/amw-design-md-lint.sh /path/to/DESIGN.md
echo $?   # 0 = pass, 1 = lint errors, 2 = invocation error
```

Output is JSON when `--json` flag passed, plain text otherwise.

**Variant 1 only.** The official linter does NOT understand Variant 2 (community 9-section format).

### 2. Pure-Python offline validator (`bin/amw-design-md-validate.py`)

For environments without `npx` / `node`, or for Variant 2 files. Implements a subset of the official linter's checks plus Variant 2 rules.

Usage:
```bash
python3 <plugin-root>/bin/amw-design-md-validate.py /path/to/DESIGN.md
python3 <plugin-root>/bin/amw-design-md-validate.py /path/to/DESIGN.md --variant 2
python3 <plugin-root>/bin/amw-design-md-validate.py /path/to/DESIGN.md --check-references
```

Args:
- `--variant 1|2|auto` — which spec to validate against (default auto-detect)
- `--check-references` — resolve all `{path.to.token}` references; report unresolved
- `--json` — output structured JSON instead of plain text

The pure-Python validator is intentionally **strict**: it accepts only the canonical formats. Custom extensions (top-level frontmatter keys not in the spec, custom sections beyond the canonical 8 / 9) are reported as warnings.

### 3. Contrast checker (`bin/amw-design-md-contrast.py`)

Computes WCAG-AA contrast ratios on every plausible color pair declared in the file. Pure-Python, no external deps.

Usage:
```bash
python3 <plugin-root>/bin/amw-design-md-contrast.py /path/to/DESIGN.md
python3 <plugin-root>/bin/amw-design-md-contrast.py /path/to/DESIGN.md --json
python3 <plugin-root>/bin/amw-design-md-contrast.py /path/to/DESIGN.md --threshold 4.5
```

The script:
1. Parses YAML frontmatter and extracts all `colors.*` tokens.
2. Identifies pairs by naming convention:
   - `X` + `on-X` (canonical pair)
   - `X` + `X-foreground` (shadcn pair)
   - `X` + `text-on-X` (custom pair)
   - All-vs-all if no naming pairs detected (verbose).
3. Computes contrast ratio per pair using the WCAG luminance formula.
4. Categorizes:
   - `≥7.0` → AAA
   - `4.5-7.0` → AA
   - `3.0-4.5` → AA-large only
   - `<3.0` → FAIL

Output:
```
primary (#1a1c1e) vs on-primary (#f7f5f2) = 14.21:1 (AAA) ✓
secondary (#6c7278) vs on-surface (#1a1c1e) = 4.86:1 (AA) ✓
text-secondary (#a0a8b0) vs surface (#ffffff) = 2.98:1 (FAIL — large only)
```

## Standard validation chain

The plugin's author and extractor agents run all three before declaring done:

```bash
bash bin/amw-design-md-lint.sh DESIGN.md && \
python3 bin/amw-design-md-validate.py DESIGN.md && \
python3 bin/amw-design-md-contrast.py DESIGN.md
```

Hard rule: any non-zero exit halts delivery. The agent returns `status=partial` or `status=failed` with the failures as `blocking_issues`.

Soft warnings (contrast failures only, no structural failures): the agent returns `status=ok` with the contrast issues in `warnings`. The user decides whether to accept.

## Lint failure → recovery

Common lint failures and their fixes:

| Lint message | Cause | Fix |
|---|---|---|
| `Frontmatter must start at line 1` | UTF-8 BOM, blank line, prose before `---` | Strip BOM, remove blank line, move `---` to line 1 |
| `Duplicate section heading: ## Colors` | Two `## Colors` blocks | Merge them into one section |
| `Section out of order: ## Components before ## Layout` | Author re-ordered | Restore canonical order from [canonical-spec-google-alpha](canonical-spec-google-alpha.md) |
> [canonical-spec-google-alpha.md] File structure (spec.md L6-L8) · YAML frontmatter schema (spec.md L17-L40, L43-L58) · Markdown body — the 8 fixed sections (spec.md L82-L92) · Recommended token names (non-normative) (spec.md L334-L342) · Consumer behavior for unknown content (spec.md L344-L356) · Validation rules (per the official linter) · Worked example (full file) · Cross-references
| `Invalid color value: red` | CSS named color | Replace with hex |
| `fontWeight must be a number: bold` | String weight | Replace with integer 100-900 |
| `Unresolved reference: {colors.foo}` | Reference target missing | Either declare `colors.foo` or fix the reference path |
| `Cycle in references: a → b → a` | Self-reference or cycle | Eliminate the cycle |
| `Dimension must have unit: 12` | Bare number | Add unit: `12px` |

See [TECH-14-validation-failure-recovery](TECH-14-validation-failure-recovery.md) for more detailed flowcharts.

## Diff between two DESIGN.md files

For change-tracking between revisions:

```bash
bash <plugin-root>/bin/amw-design-md-diff.sh OLD.md NEW.md
```

Wrapper around `npx @google/design.md diff`. Reports added/removed/changed tokens, section reorderings, prose changes. Useful for code review of DESIGN.md edits.

## CI integration suggestion (out-of-scope but documented)

Projects that ship DESIGN.md as canonical can add a CI step:

```bash
# .github/workflows/design-md-lint.yml
- name: Lint DESIGN.md
  run: |
    bash $CLAUDE_PLUGIN_ROOT/bin/amw-design-md-lint.sh DESIGN.md
    python3 $CLAUDE_PLUGIN_ROOT/bin/amw-design-md-validate.py DESIGN.md
    python3 $CLAUDE_PLUGIN_ROOT/bin/amw-design-md-contrast.py DESIGN.md --threshold 4.5
```

This catches drift introduced by hand-edits before merge.

## Cross-references

- [TECH-01-yaml-frontmatter](./TECH-01-yaml-frontmatter.md) — frontmatter rules
  > What it does · When to use · Hard rules · Delimiters · Top-level fields · Value type rules · Token references · YAML quoting rules · Common gotchas · Worked example — minimal valid frontmatter · Worked example — token reference inside components · Validation · Cross-references
- [TECH-05-token-references](./TECH-05-token-references.md) — reference resolution
  > What it does · Hard rules · Syntax · Where references are valid · Resolution model · Scalar groups must point to primitives · Composite references allowed inside `components` · Self-references and cycles · What a resolved DESIGN.md looks like · When NOT to use references · Common errors · Validation · Cross-references
- [TECH-14-validation-failure-recovery](./TECH-14-validation-failure-recovery.md) — what to do when validation fails
  > What it does · Recovery flowchart · Failure categories · Structural failures (S* — P0, must fix before delivery) · Token-quality failures (T* — P1, must fix before final delivery) · Reference failures (R* — P0) · Accessibility failures (A* — P0 for body text, P1 for others) · Content-integrity failures (C* — P2, warn only) · Iteration cap · What recovery does NOT do · Manual recovery flow for users · Cross-references
- `../../../bin/amw-design-md-lint.sh`
- `../../../bin/amw-design-md-validate.py`
- `../../../bin/amw-design-md-contrast.py`
- `../../../bin/amw-design-md-diff.sh`
