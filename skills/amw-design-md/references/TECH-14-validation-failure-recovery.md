---
name: TECH-14-validation-failure-recovery
category: validation
source: TECH-11-validation-and-lint.md
also-in: TECH-01-yaml-frontmatter.md, TECH-04-component-tokens.md, TECH-05-token-references.md
status: stable
---

# TECH: Validation failure recovery

## What it does

Documents the recovery flow when `bin/amw-design-md-lint.sh`, `bin/amw-design-md-validate.py`, or `bin/amw-design-md-contrast.py` reports an error. Lists every common failure category, its diagnostic signal, the corrective action, and the slash command (if any) that automates the fix.

The flow applies to both author-agent self-revision (after generating a draft) and to user-driven revision (after running a manual lint).

## Recovery flowchart

```
                ┌─────────────────────────────────┐
                │ Run all 3 validators            │
                └──────────────┬──────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │ Any failures?                │
                └────────┬───────────────┬────┘
                         │ No            │ Yes
                         │               │
                         ▼               ▼
                   DELIVER         Categorize failures:
                                   ┌────────────────────┐
                                   │ S* (structural)    │ → P0 — block delivery
                                   │ T* (token quality) │ → P1
                                   │ A* (accessibility) │ → P0 if body text, P1 else
                                   │ C* (content)       │ → P2 — warn only
                                   └─────────┬──────────┘
                                             │
                                             ▼
                                     Apply corrective action
                                             │
                                             ▼
                                     Re-run validators
                                             │
                                             ▼
                                     Iterate up to 3 times
                                             │
                                             ▼
                                     If still failing:
                                       - status=partial
                                       - blocking_issues populated
                                       - escalate to user
```

## Failure categories

### Structural failures (S* — P0, must fix before delivery)

#### S.frontmatter-not-at-line-1
**Signal:** Linter: `Frontmatter must start at line 1 with ---`.
**Cause:** UTF-8 BOM, blank line before `---`, prose preamble.
**Fix:** Strip BOM, remove leading whitespace/blanks, ensure line 1 is exactly `---`.
**Auto-fixable:** Yes — remove leading bytes until first `---` on its own line.

#### S.yaml-parse-error
**Signal:** Linter: `YAML parse error: ...`.
**Cause:** Tabs instead of spaces, unquoted hex values, missing colons, trailing commas.
**Fix:** Run `python3 -c "import yaml; yaml.safe_load(open('DESIGN.md').read().split('---')[1])"` for the exact YAML error position. Common quick-fixes:
- `primary: #1A1C1E` → `primary: "#1A1C1E"` (quote the hex)
- Tabs → 2 spaces
- Trailing comma → remove

#### S.duplicate-section
**Signal:** Linter: `Duplicate section heading: ## Colors`.
**Cause:** Author added a second section by mistake.
**Fix:** Merge the two `## Colors` sections into one (preserve all bullets), delete the duplicate header.
**Auto-fixable:** No — content of duplicates may differ; manual merge required.

#### S.section-out-of-order
**Signal:** Linter: `Section out of order: ## Components must come after ## Layout`.
**Cause:** Author re-ordered sections.
**Fix:** Reorder per canonical sequence: Overview / Colors / Typography / Layout / Elevation & Depth / Shapes / Components / Do's and Don'ts.
**Auto-fixable:** Yes — re-emit sections in canonical order.

### Token-quality failures (T* — P1, must fix before final delivery)

#### T.invalid-color
**Signal:** Linter: `Invalid color value: red`.
**Cause:** CSS named color, `rgb()`, or `hsl()` literal in frontmatter.
**Fix:** Replace with hex. Tools that may help:
- `red` → `#FF0000`
- `rgb(255, 0, 0)` → `#FF0000`
- `hsl(0, 100%, 50%)` → `#FF0000`
- Use a color picker tool or the CSS property of the original source.

#### T.fontWeight-not-numeric
**Signal:** Linter: `fontWeight must be a number: bold`.
**Fix:** Replace named weights:
- `bold` → `700`
- `regular` → `400`
- `light` → `300`
- `medium` → `500`
- `semibold` → `600`
- `extrabold` → `800`
- `black` → `900`

#### T.dimension-no-unit
**Signal:** Linter: `Dimension requires unit (px, em, rem): 12`.
**Fix:** Add unit. Default to `px` for all sizing.

#### T.fontSize-out-of-range
**Signal:** Validator: `fontSize 600px is suspect (expected 8-200px)`.
**Cause:** Decimal point lost, e.g., `60px` typed as `600px`.
**Fix:** Sanity-check; restore intended value.

### Reference failures (R* — P0)

#### R.unresolved-reference
**Signal:** Linter: `Unresolved reference: {colors.foo}`.
**Cause:** The path `colors.foo` doesn't exist in the YAML tree.
**Fix:**
- If `colors.foo` should exist: add it to the `colors:` map.
- If the reference is wrong: correct the path (perhaps `{colors.foo}` should be `{colors.primary-foreground}`).

#### R.cycle
**Signal:** Linter: `Cycle in references: a → b → a`.
**Cause:** A references B and B references A (or longer cycle).
**Fix:** Eliminate the cycle. Pick one node to be the literal value; others reference it.

#### R.scope-violation
**Signal:** Linter: `Composite reference {typography.label-md} not allowed in colors.X`.
**Cause:** A composite reference (whole Typography object) used outside `components.*`.
**Fix:** Either reference a primitive sub-field (`{typography.label-md.fontFamily}`) or move the reference into a `components.*` value.

### Accessibility failures (A* — P0 for body text, P1 for others)

#### A.contrast-below-AA
**Signal:** Contrast checker: `text-secondary (#A0A8B0) on surface (#FFFFFF) = 2.98:1, fails WCAG-AA 4.5:1`.
**Cause:** Color pair declared but not contrast-compliant.
**Fix:** Three options:
1. **Darken or lighten** the foreground/background until ratio ≥ 4.5:1. Tools like https://webaim.org/resources/contrastchecker can find the nearest compliant value.
2. **Restrict to large text only** if 3.0:1 ≤ ratio < 4.5:1; document the restriction in `## Do's and Don'ts`.
3. **Acknowledge in `warnings`** and let the user accept the failure; only valid for P1 cases (e.g., decorative use).

The author agent's default behavior on first failure: option 1 (try a darker variant). If a darker variant breaks the brand identity, escalate to user.

#### A.no-focus-ring
**Signal:** Auditor Pass 3: `No focus-ring color or formula declared`.
**Cause:** No `--focus-ring`, no `focus-ring-color`, no prose mention.
**Fix:** Either add a `colors.focus-ring` token or document the focus-ring formula in `## Components` prose ("Focus rings use a 2-px outline of `--primary` offset by 2 px outside the rounded boundary").

### Content-integrity failures (C* — P2, warn only)

These don't block delivery but reduce the rubric score:

| Failure | Fix |
|---|---|
| `C1`: Placeholders remaining | Search-replace `{{...}}`, `TBD`, `FIXME` |
| `C3`: Vague Do/Don't rules | Rewrite per [TECH-06-do-donts](TECH-06-do-donts.md) recipe |
| `C6`: File length out of range (200-1500 lines) | Either expand undeveloped sections or trim verbose ones |
| `C7`: Section header with no prose underneath | Add a 1-paragraph philosophy note |

## Iteration cap

The author agent self-revises up to 3 times after a draft. If the 3rd revision still fails, the agent returns:

```yaml
status: partial
confidence: low
blocking_issues:
  - "After 3 self-revisions, S2 (YAML parse error at line 14) persists. Manual fix required."
recommendations:
  - "Open DESIGN.md, validate the YAML around line 14 manually."
next_action: escalate_to_user
```

The user fixes manually OR provides additional context (e.g., "the original brand uses CSS hsl()" — revealing the hsl() should be converted to hex).

## What recovery does NOT do

- **Never invents tokens** to fix unresolved references. If `{colors.foo}` is unresolved and the context doesn't suggest what `foo` should be, the agent escalates to user.
- **Never silently lowers contrast** to make the file "pass". A failure is reported, not hidden.
- **Never reorders sections without acknowledging.** If the agent fixes section order, the warning notes "section order normalized — verify intent preserved".

## Manual recovery flow for users

When a user is editing a DESIGN.md by hand and a validator fails:

1. Read the error message (line + column + reason).
2. Open the file at that line.
3. Apply the fix per the table above.
4. Re-run the validator.
5. If still failing, apply the next fix.
6. If stuck after 3 fixes, post the file content + error to the agent for review.

## Cross-references

- [TECH-11-validation-and-lint](./TECH-11-validation-and-lint.md) — running the validators
- [TECH-01-yaml-frontmatter](./TECH-01-yaml-frontmatter.md) — YAML rules
- [TECH-04-component-tokens](./TECH-04-component-tokens.md) — component property whitelist
- [TECH-05-token-references](./TECH-05-token-references.md) — reference resolution rules
- [review-rubric](./review-rubric.md) — the rubric checks (S*, T*, R*, A*, C*)
- `<plugin-root>/bin/amw-design-md-lint.sh`
- `<plugin-root>/bin/amw-design-md-validate.py`
- `<plugin-root>/bin/amw-design-md-contrast.py`
