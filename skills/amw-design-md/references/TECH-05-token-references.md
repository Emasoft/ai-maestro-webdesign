---
name: TECH-05-token-references
category: authoring
source: design.md-main/docs/spec.md L76
also-in: TECH-01-yaml-frontmatter.md, TECH-04-component-tokens.md, TECH-11-validation-and-lint.md
status: stable
---

# TECH: Token references — `{path.to.token}` syntax

## What it does

Documents the canonical reference syntax used in DESIGN.md frontmatter to point one token at another. Covers syntax rules, scope (where references are allowed), what they resolve to, and common errors.

## Hard rules

### Syntax

```
"{path.to.token}"
```

- Curly-brace-wrapped (`{` open, `}` close).
- Dotted path with no spaces, e.g., `colors.primary` or `typography.label-md`.
- Path uses ASCII alphanumerics + `-` + `_`. No spaces, no quotes inside, no escape sequences.
- The whole reference is a string in YAML — must be quoted with double quotes (so YAML doesn't try to interpret the curly braces).

### Where references are valid

| Location | Allowed? | Reference type |
|---|---|---|
| `colors.<name>` value | Yes | Must resolve to a primitive (a hex string) |
| `typography.<name>.<sub-field>` | Yes | Must resolve to a primitive |
| `rounded.<name>` | Yes | Must resolve to a Dimension primitive |
| `spacing.<name>` | Yes | Must resolve to a Dimension/number primitive |
| `components.<name>.<property>` | Yes | Primitives OR composite (whole Typography object) |
| Top-level (`name`, `description`, `version`) | NO | These are scalar literals only |
| In markdown body prose | NO | Prose uses descriptive text + literal hex |

### Resolution model

The resolver walks the YAML tree from root using the dotted path:

```
"{colors.primary}" → tree["colors"]["primary"] → "#1A1C1E"
"{typography.body-md}" → tree["typography"]["body-md"] → {fontFamily, fontSize, ...}
"{rounded.md}" → tree["rounded"]["md"] → "8px"
```

If any segment of the path is missing, the linter raises an error: "unresolved reference {colors.foo}: path 'colors.foo' not found".

### Scalar groups must point to primitives

Per spec.md L76: "For most token groups, the reference must point to a primitive value (e.g., `colors.primary-60`), not a group (e.g., `colors`)."

This means inside `colors.*`, `typography.*.*`, `rounded.*`, `spacing.*`, the reference must end at a leaf (string or number). Pointing at a group:

```yaml
colors:
  primary: "{colors}"        # ERROR — points at a group, not a primitive
  primary-60: "{colors}"     # ERROR
typography:
  body-md: "{typography.label-md}"   # ERROR — points at a Typography object inside typography group
```

These all fail the linter.

### Composite references allowed inside `components`

The exception: per spec.md L76 second sentence, references inside `components.*` MAY point to composite values:

```yaml
components:
  button-primary:
    typography: "{typography.label-md}"   # OK — composite reference
    backgroundColor: "{colors.primary}"   # OK — primitive reference
```

The reader resolves `{typography.label-md}` to the whole Typography object and applies it to the button's typography (font-family + size + weight + line-height etc. all at once).

### Self-references and cycles

References to oneself or to anything that creates a cycle are errors:

```yaml
colors:
  primary: "{colors.primary}"     # ERROR — self-reference
  a: "{colors.b}"
  b: "{colors.a}"                  # ERROR — cycle a → b → a
```

The linter detects cycles and rejects the file.

### What a resolved DESIGN.md looks like

After resolution, the file is conceptually flattened. Tools that consume DESIGN.md (like `bin/amw-design-md-emit-companions.py`) typically resolve all references to produce the companion `tokens.json`:

```yaml
# Source
colors:
  primary: "#1A1C1E"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
```

```json
// Resolved tokens.json (W3C format)
{
  "colors": {
    "primary": {"$value": "#1A1C1E", "$type": "color"}
  },
  "components": {
    "button-primary": {
      "backgroundColor": {"$value": "#1A1C1E", "$type": "color"}
    }
  }
}
```

The reference is preserved in the source DESIGN.md (so changing `colors.primary` propagates) but resolved when emitting code.

## When NOT to use references

References add a level of indirection. Use them when:

- The same value appears 3+ times across components.
- Token meaning matters (a button background that "is" the primary color, not just the same hex).
- The system supports themes and the value should track theme switches.

Don't use them when:

- The value appears once and changing it doesn't affect any other token.
- The reference makes the file harder to read (e.g., `padding: "{spacing.md}"` for a one-off button when `padding: 12px` is just clearer).

The plugin's authoring tools default to `{path.to.token}` references for `backgroundColor`, `textColor`, `typography`, and `rounded` properties (these benefit from indirection). They emit literal values for `padding`, `size`, `height`, `width` (these vary per component and rarely need the indirection).

## Common errors

| Error | Wrong | Right |
|---|---|---|
| Unresolved | `{colors.foo}` (no `colors.foo` declared) | Either declare it or fix the path |
| Bad syntax | `{ colors.primary }` (spaces) | `{colors.primary}` |
| Unquoted | `padding: {colors.primary}` | `padding: "{colors.primary}"` |
| Wrong scope | `colors.primary: "{typography.label-md}"` (typography in colors) | Don't cross types |
| Cycle | `a → b → a` | Eliminate the cycle |
| Group target | `"{colors}"` (whole group) | Target a leaf: `"{colors.primary}"` |

## Validation

The linter resolves all references; unresolved or bad-syntax references fail:

```bash
bash <plugin-root>/bin/amw-design-md-lint.sh DESIGN.md
python3 <plugin-root>/bin/amw-design-md-validate.py DESIGN.md --check-references
```

## Cross-references

- `./TECH-01-yaml-frontmatter.md`
- `./TECH-04-component-tokens.md` — composite references inside `components`
- `./TECH-11-validation-and-lint.md` — running the resolver
- `./TECH-12-companion-files.md` — what the resolver outputs in `tokens.json`
- `../canonical-spec-google-alpha.md`
