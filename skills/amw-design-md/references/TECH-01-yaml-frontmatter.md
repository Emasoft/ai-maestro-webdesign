---
name: TECH-01-yaml-frontmatter
category: authoring
source: design.md-main/docs/spec.md L17-L72
also-in: TECH-02-color-tokens.md, TECH-03-typography-tokens.md, TECH-04-component-tokens.md, TECH-05-token-references.md
status: stable
---

# TECH: Authoring the YAML frontmatter (Variant 1)

## What it does

Documents the rules for writing the YAML frontmatter at the top of a Variant 1 (canonical `@google/design.md`) DESIGN.md file. Covers delimiters, top-level fields, value types, escaping rules, and common gotchas.

## When to use

- Every time you author a new Variant 1 DESIGN.md.
- Every time you edit an existing Variant 1 frontmatter.
- When converting Variant 2 → Variant 1, the conversion produces frontmatter — these rules apply.

## Hard rules

### Delimiters

The frontmatter MUST be delimited by exactly `---` on its own line at the start of the file and exactly `---` on its own line to close. Examples that fail:

| Wrong | Why |
|---|---|
| Blank line before opening `---` | Frontmatter must start at line 1 |
| `--- ` (trailing space) | Must be exactly `---` |
| `----` (4 dashes) | Must be exactly 3 |
| UTF-8 BOM at start of file | Linter rejects |
| `---\r\n` (CRLF line endings) | Linter expects LF only |

### Top-level fields

Allowed top-level keys (per spec L43-L58):

| Key | Required? | Type | Notes |
|---|---|---|---|
| `version` | optional | string | Current literal: `alpha` |
| `name` | **REQUIRED** | string | Design system name |
| `description` | optional | string | One-line description |
| `colors` | optional | map<string, Color> | At least `primary` recommended |
| `typography` | optional | map<string, Typography> | 9-15 levels typical |
| `rounded` | optional | map<string, Dimension> | Corner radii |
| `spacing` | optional | map<string, Dimension \| number> | Spacing scale |
| `components` | optional | map<string, map<string, string>> | Component variant tokens |

Any other top-level key is **accepted with warning** by the official linter (per "Consumer Behavior for Unknown Content" in spec.md L344-L356). Do not invent top-level keys; they will not be parsed by downstream consumers.

### Value type rules

- **Color**: Must be `#xxxxxx` or short-form `#xxx` in sRGB. No CSS named colors. No `rgb()`. No `hsl()`. Quoted strings: `primary: "#1A1C1E"`.
- **Dimension**: String with unit suffix `px`, `em`, or `rem`. Quoted: `fontSize: "48px"`.
- **fontWeight**: Integer 100-900. Bare number (`fontWeight: 600`) or quoted string (`fontWeight: "600"`) both accepted. NEVER `fontWeight: bold`.
- **lineHeight**: Either Dimension (`"1.5rem"`) or unitless number (`1.6`). Unitless = multiplier of fontSize.
- **letterSpacing**: Dimension only. Common to use em: `letterSpacing: "-0.02em"`.
- **fontFamily**: Plain string, no quotes around CSS identifiers needed in YAML but quoting is safe: `fontFamily: "Public Sans"`.

### Token references

Inside `components.<name>.<property>` values:

```yaml
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
```

Reference syntax: `"{path.to.token}"` — quoted string, curly-brace-wrapped, dotted path, ASCII alnum + `-` + `_`.

The reference resolver:
1. Walks the YAML tree from root.
2. For `colors.*`, `rounded.*`, `spacing.*`: must point to a primitive (a string or number). Pointing to a group (`{colors}`) is an error.
3. For `components.*`: composite references allowed (`{typography.label-md}` resolves to the whole Typography object).

Token references in scalar groups (`colors`, `typography`, `rounded`, `spacing`) themselves are also allowed but rare. The common pattern is: declare primitives in scalar groups, reference them in `components`.

### YAML quoting rules

YAML accepts unquoted strings, single-quoted, and double-quoted. The plugin convention (matches the spec's example block in spec.md L21-L36):

- Hex values: **double-quoted** (`primary: "#1A1C1E"`). Hex strings start with `#`, which YAML treats as comment-start unless quoted.
- Dimensions: **double-quoted** (`fontSize: "48px"`). Optional but safer.
- Token references: **double-quoted** mandatory (curly braces would otherwise need escape).
- Bare numbers: unquoted (`fontWeight: 600`, `lineHeight: 1.6`).
- Font family names: unquoted OK if ASCII (`fontFamily: Public Sans`); quote if non-ASCII or with special chars.

## Common gotchas

| Gotcha | Symptom | Fix |
|---|---|---|
| Tabs instead of spaces | Linter: "YAML parse error" | Use 2 spaces consistently |
| `primary: #1A1C1E` (unquoted hex) | YAML treats `#` as comment, value becomes empty | Quote: `primary: "#1A1C1E"` |
| `rounded: full: 9999px` (collapsed indent) | YAML parses as scalar | Indent properly: `rounded:\n  full: 9999px` |
| `fontWeight: bold` | Linter: "fontWeight must be number" | Use `700` |
| `padding: 12` (no unit) | Linter: "Dimension requires unit" | Use `"12px"` |
| Token ref to non-existent path | Linter: "unresolved reference {colors.foo}" | Either declare `colors.foo` or fix the reference |
| Trailing comma in YAML | Linter: parse error | Remove trailing comma |
| Empty value: `description:` | Some parsers warn | Either fill it or remove the key |

## Worked example — minimal valid frontmatter

```yaml
---
version: alpha
name: My Design System
colors:
  primary: "#1A1C1E"
typography:
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
---
```

This passes `npx @google/design.md lint` with no warnings.

## Worked example — token reference inside components

```yaml
---
version: alpha
name: My Design System
colors:
  primary: "#1A1C1E"
  on-primary: "#F7F5F2"
typography:
  label-md:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.4
rounded:
  md: 8px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.md}"
    padding: 12px
---
```

The reference `"{typography.label-md}"` resolves to the whole `label-md` typography object — this is allowed inside `components.*` per spec L76.

## Validation

```bash
bash <plugin-root>/bin/amw-design-md-lint.sh DESIGN.md
python3 <plugin-root>/bin/amw-design-md-validate.py DESIGN.md
```

Both should exit 0. Any error halts delivery per the skill's hard rules.

## Cross-references

- [canonical-spec-google-alpha](./canonical-spec-google-alpha.md) — full spec
- [TECH-02-color-tokens](./TECH-02-color-tokens.md) — color authoring details
- [TECH-03-typography-tokens](./TECH-03-typography-tokens.md) — typography authoring
- [TECH-04-component-tokens](./TECH-04-component-tokens.md) — component-property authoring
- [TECH-05-token-references](./TECH-05-token-references.md) — reference resolution rules
- [TECH-11-validation-and-lint](./TECH-11-validation-and-lint.md) — validator usage
