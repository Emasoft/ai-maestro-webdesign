---
name: TECH-27-token-interpolation
category: validation
source: design.md {token.ref} convention (Apache-2.0); awesome-design-md cross-reference linting (MIT)
license: Apache-2.0 / MIT
also-in: TECH-05-token-references.md, TECH-11-validation-and-lint.md, TECH-24-authoring-rules-spec.md
status: stable
---

# TECH: {token.ref} interpolation + dead-reference linting

## Table of Contents

- [What it does](#what-it-does)
- [The interpolation contract](#the-interpolation-contract)
- [Syntax](#syntax)
- [Why prose references tokens, not raw values](#why-prose-references-tokens-not-raw-values)
- [Dead-reference detection](#dead-reference-detection)
  - [What counts as dead](#what-counts-as-dead)
  - [What does NOT count as dead](#what-does-not-count-as-dead)
- [Resolution order](#resolution-order)
- [Where interpolation is enforced](#where-interpolation-is-enforced)
- [Where interpolation is suggested but not enforced](#where-interpolation-is-suggested-but-not-enforced)
- [Worked examples](#worked-examples)
  - [Pass examples](#pass-examples)
  - [Fail examples](#fail-examples)
- [Lint message format](#lint-message-format)
- [Implementation notes](#implementation-notes)
- [Cross-references](#cross-references)

## What it does

Documents the `{token.ref}` interpolation convention used throughout DESIGN.md prose, tables, and component definitions to reference tokens declared in the YAML frontmatter. Also documents the dead-reference detection (`{token.ref}` whose target does not exist) that surfaces as a P1 lint error.

The bin script that performs this check is `bin/amw-design-md-validate.py`. The check runs by default on every `validate` and `lint` invocation.

## The interpolation contract

DESIGN.md prose references tokens via a curly-brace dotted-path syntax:

```
{colors.primary}
{typography.body.size}
{spacing.4}
{rounded.md}
{elevation.raised.treatment}
```

This syntax is machine-substitutable. An emitter, an agent, or a downstream consumer can replace every `{token.ref}` occurrence with the resolved value from the frontmatter:

- `{colors.primary}` → `#1A1C1E`
- `{typography.body.size}` → `16px`
- `{spacing.4}` → `32px`

The substitution is one-pass, no nested resolution, no expression evaluation. Each `{token.ref}` resolves to exactly one literal value.

## Syntax

The grammar is strict:

- Opening brace `{`.
- Dotted path: `<top-key>.<sub-key>[.<sub-key>...]`.
- Closing brace `}`.
- No whitespace inside the braces.
- No quotes around path segments.
- Path segments are kebab-case or snake_case; the convention is kebab-case to match CSS-custom-property names.

Permitted top-keys are exactly those declared at the top level of the YAML frontmatter, typically:

- `colors`
- `typography`
- `spacing`
- `rounded`
- `elevation`
- `motion` (when §7-ext present per [TECH-26-extended-sections-7-8](TECH-26-extended-sections-7-8.md))
- `components`

Path depth is limited to 4 levels (most paths are 2 or 3 levels). Deeper paths usually indicate that the frontmatter is over-nested.

## Why prose references tokens, not raw values

When DESIGN.md prose contains raw hex / px values instead of `{token.ref}` references, three problems arise:

1. **Drift.** If the frontmatter `colors.primary` is later changed from `#1A1C1E` to `#0F0F0F`, every prose mention of the old value becomes stale. The linter cannot detect drift in prose.
2. **Substitution failure.** Downstream emitters (e.g. `tokens.css` generator) cannot replace raw values — they only substitute `{token.ref}` patterns. Prose with raw values silently bypasses the substitution chain.
3. **Translation friction.** When the DESIGN.md is translated to another language, prose with raw values produces tokenless translations. Prose with `{token.ref}` produces translations where the token references are preserved unchanged.

Rule 12 of [TECH-24-authoring-rules-spec](../../amw-design-md-spec/references/TECH-24-authoring-rules-spec.md) enforces this: component definitions in §6 MUST cite tokens, never raw values. The same principle is recommended (warning-level) for all prose mentioning a color or spacing value.

## Dead-reference detection

### What counts as dead

A `{token.ref}` is DEAD when:

- The top-key (e.g. `colors`) does not exist in the YAML frontmatter.
- The path traverses into a value that does not exist (e.g. `{colors.tertiary}` when only `primary` and `secondary` are declared).
- The terminal path segment lands on a parent node, not a leaf (e.g. `{colors}` alone, or `{typography.body}` when `body` is a sub-object with `size`/`weight`/`line-height` sub-keys).
- The path contains a typo that does not match any declared key (e.g. `{coloors.primary}`).

Dead references are P1 LINT ERRORS. They block delivery until resolved.

### What does NOT count as dead

The following do NOT trigger the dead-reference check:

- References inside code fences (` ``` ` blocks). Code is opaque to the validator.
- References inside HTML comments (`<!-- ... -->`).
- The escaped form `\{colors.primary\}` (used to document the interpolation syntax in meta-text).
- References to CSS custom properties via `var(--name)` — that's a different convention, validated by CSS lint, not by this check.

## Resolution order

When the validator encounters `{a.b.c}`, it resolves in this order:

1. Look up top-level key `a` in the YAML frontmatter.
2. If `a` is a mapping, look up sub-key `b`.
3. If `b` is a mapping, look up sub-key `c`.
4. The final value must be a SCALAR (string, number, bool) — not a mapping.

If any step fails, the reference is dead.

The validator does NOT follow `value` indirections. If the frontmatter declares:

```yaml
colors:
  primary: '#1A1C1E'
  brand: '{colors.primary}'
```

then `{colors.brand}` resolves to the literal string `'{colors.primary}'`, NOT to `'#1A1C1E'`. Indirection chains are not supported in the frontmatter; the source-of-truth is always a literal.

## Where interpolation is enforced

Interpolation (use `{token.ref}` instead of raw value) is ENFORCED in:

- §6 Components definitions (Rule 12, P1 error).
- §5 Surfaces & Elevation table Treatment column when it references a color or shadow value.
- §7-ext Transition Tokens table (when present).
- §8-ext Color Contrast table FG/BG columns (when present) — these MAY use raw values for direct readability, but `{token.ref}` is preferred.

Dead-reference detection is ENFORCED everywhere `{token.ref}` syntax appears, including:

- All prose sections.
- All table cells.
- §9 Agent Prompt Guide CSS snippets (when token references are used).
- §10 Iteration Guide.
- §11 Known Gaps.

## Where interpolation is suggested but not enforced

Interpolation is SUGGESTED (warning, not error) in:

- §1 Identity prose mentioning a color or spacing.
- §2-§4 narrative paragraphs alongside the token tables.
- §8 Do's and Don'ts list items (the rule itself can mention raw values for human readability).
- All `STYLE-REFERENCES.md` companion content.

The asymmetry: STRUCTURAL content (token tables, component specs) is strict; NARRATIVE content (prose explaining the system) is permissive.

## Worked examples

### Pass examples

Frontmatter:
```yaml
colors:
  primary: '#1A1C1E'
  secondary: '#6C7278'
  tertiary: '#B8422E'
typography:
  body:
    family: 'Inter, sans-serif'
    size: '16px'
    line-height: 1.55
spacing:
  '1': '8px'
  '2': '16px'
  '3': '24px'
```

Body text:
```markdown
The primary color {colors.primary} is paired with surface white. Body text
uses {typography.body.family} at {typography.body.size}. Section spacing
follows a {spacing.3} rhythm.
```

All four `{token.ref}` references resolve. Validator passes.

### Fail examples

Frontmatter (same as above).

Body text:
```markdown
The primary color {colors.primary} pairs with {colors.brand} on hero
sections. The accent {colors.accent} appears at scroll milestones. Body
text uses {typography.bodytext.size}.
```

Three failures:
- `{colors.brand}` — `brand` is not declared. DEAD.
- `{colors.accent}` — `accent` is not declared. (`tertiary` is declared but the author wrote `accent`.) DEAD.
- `{typography.bodytext.size}` — `bodytext` is not declared (`body` is). DEAD.

Validator emits three P1 errors and blocks delivery.

## Lint message format

When a dead reference is detected, the validator emits:

```
[P1] {token.ref} dead: '{colors.brand}' at DESIGN.md:L42
  Resolution path: colors.brand
  Did you mean: {colors.tertiary}? {colors.primary}? {colors.secondary}?
  (these are the declared keys under 'colors')
```

The "Did you mean" suggestion uses Levenshtein distance over the declared key set; suggestions appear when the edit distance is ≤2.

## Implementation notes

The validator is `bin/amw-design-md-validate.py`. The dead-reference check is the function `check_dead_references()` and is called by `main()` after frontmatter and section structure validation.

Performance: the check is O(n × k) where n is the count of `{token.ref}` occurrences and k is the average dotted-path depth. For typical DESIGN.md files (40 references, depth 3) this is ~120 operations — sub-millisecond.

The check does not parse the full Markdown AST; it uses a regex `\{[a-z][a-z0-9_-]*(\.[a-z0-9_-]+)*\}` over the source text. This means:

- References inside code fences ARE caught by the regex but suppressed by a code-fence detection pre-pass.
- References inside HTML comments are similarly suppressed.
- The regex does not require the file to be valid Markdown — broken Markdown still gets dead-reference detection.

## Cross-references

- [TECH-05-token-references](../../amw-design-md/references/TECH-05-token-references.md) — broader token-reference patterns
- [TECH-11-validation-and-lint](../../amw-design-md/references/TECH-11-validation-and-lint.md) — `bin/amw-design-md-validate.py` usage
- [TECH-24-authoring-rules-spec](../../amw-design-md-spec/references/TECH-24-authoring-rules-spec.md) — Rule 12 (components must cite tokens, not raw values)
- [TECH-22-section-10-11-extended](TECH-22-section-10-11-extended.md) — §10/§11 dead-reference enforcement
- [TECH-23-section-9-agent-prompt-guide](TECH-23-section-9-agent-prompt-guide.md) — §9 CSS snippets dead-reference enforcement
- [TECH-26-extended-sections-7-8](TECH-26-extended-sections-7-8.md) — §7-ext / §8-ext tables dead-reference enforcement
- `<plugin-root>/bin/amw-design-md-validate.py` — pure-Python validator implementing the check
