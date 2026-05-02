---
name: amw-design-md-diff
description: "Diff two DESIGN.md revisions and surface what tokens / sections changed. Wraps `npx @google/design.md diff` for the structured diff plus a fallback markdown-aware textual diff via bin/amw-design-md-diff.sh. Useful for change-tracking when a brand evolves a token set or when a Tailwind config update propagates new colors."
---

# /amw-design-md-diff

Compare two DESIGN.md files and surface the structured token-level differences (colors changed, typography keys added/removed, components modified) in a way that is more readable than a raw `diff -u`.

## Arguments

`$ARGUMENTS` should contain two DESIGN.md paths:

- `<a-path> <b-path>`

If only one path is provided or neither is provided, surface a usage error and stop.

## Action

### 1. Confirm both files exist and are Variant 1

Read the first lines of each. If either lacks `---` YAML frontmatter, surface a warning that the diff may be less precise (the tool can still run a textual diff, but the structured token diff requires Variant 1).

### 2. Run the diff wrapper

```bash
bash bin/amw-design-md-diff.sh "<a>" "<b>"
```

The wrapper invokes `npx @google/design.md diff <a> <b>` for the structured diff. If `npx` is unavailable, it falls back to a Python-driven YAML-aware diff that compares the two frontmatter blocks key-by-key plus a section-level prose diff.

### 3. Surface the result

- **Tokens added** — new color / typography / rounded / spacing / components keys in B not in A
- **Tokens removed** — present in A, absent in B
- **Tokens changed** — present in both with different values
- **Sections changed** — prose section text differences (collapsed to "modified" / "unchanged" rather than full prose diff, unless `--full-prose` was passed)
- **Frontmatter shape changes** — version bump, name change, structural reorg

### 4. Recommend follow-up actions

- If many tokens are removed without a corresponding addition → recommend `/amw-design-md-audit <b>` to verify the new file is internally consistent.
- If tokens are renamed (removed + added with similar but different keys) → suggest manually verifying the rename was intentional.
- If contrast pairs changed → suggest `bin/amw-design-md-contrast.py <b>` to verify the new pairs still meet WCAG AA.

## Non-negotiables

- **Read-only diff.** The command does not modify either file.
- **Variant 1 preferred.** Variant 2 (community) files can be diffed but the output is less precise; recommend converting to Variant 1 first.
- **No silent merge.** This is a diff, not a three-way merge. If the user wants to merge two DESIGN.md revisions, recommend manual editing or running `/amw-design-md-create --input-type brief` to author a new file from a brief that combines both.

## Failure modes

- One or both files missing → surface error and stop.
- `npx` unavailable → fall back to Python diff with a warning. Recommend `npm install -g npx` for the canonical structured diff.
- Either file is malformed (cannot parse YAML) → surface the parse error and stop. Recommend `/amw-design-md-lint` first.

## Cross-references

- `bin/amw-design-md-diff.sh`
- `bin/amw-design-md-validate.py` (used by Python fallback)
- [canonical-spec-google-alpha](skills/amw-design-md/references/canonical-spec-google-alpha.md)
- [TECH-11-validation-and-lint](skills/amw-design-md/references/TECH-11-validation-and-lint.md)
