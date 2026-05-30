---
name: TECH-17-dtcg-export
category: emission
source: W3C DTCG Format Module (design-tokens.github.io/community-group/format/)
also-in: TECH-05-token-references.md, TECH-12-companion-files.md, TECH-15-design-md-as-input.md
status: stable
---

# TECH: DTCG export and harmonize pass (`amw-dtcg-export.py`)

## Table of Contents

- [What it does](#what-it-does)
- [Why a dedicated DTCG exporter](#why-a-dedicated-dtcg-exporter)
- [DTCG schema mapping](#dtcg-schema-mapping)
  - [Leaf shape](#leaf-shape)
  - [Group shape and `$type` inheritance](#group-shape-and-type-inheritance)
  - [Alias syntax](#alias-syntax)
  - [Composite typography tokens](#composite-typography-tokens)
- [Source coverage](#source-coverage)
- [Harmonize mode](#harmonize-mode)
  - [Bare-key rewrite](#bare-key-rewrite)
  - [Type inference for unlabelled leaves](#type-inference-for-unlabelled-leaves)
  - [Idempotence](#idempotence)
- [Validation contract](#validation-contract)
- [Round-trip contract with `amw-design-md-emit-companions.py`](#round-trip-contract-with-amw-design-md-emit-companionspy)
- [CLI reference](#cli-reference)
- [Cross-references](#cross-references)

## What it does

`bin/amw-dtcg-export.py` exports a [DTCG](https://design-tokens.github.io/community-group/format/)-conformant token JSON from a DESIGN.md (Variant 1) or from a Figma-Tokens-style nested-group JSON. Compared to the partial DTCG output emitted by `bin/amw-design-md-emit-companions.py --targets json`, this script:

- Stamps `$type` and `$value` on **every** leaf — DTCG's hard requirement.
- Sets a group-level `$type` when every direct child of a group shares the same primitive type (spec-allowed inheritance — saves repetition and matches the canonical schema from the W3C Format Module).
- Preserves alias references verbatim as the leaf's `$value` string. DTCG consumers (Style Dictionary, Tokens Studio, Specify, etc.) resolve them at consumption time.
- With `--harmonize`, accepts non-canonical input that uses bare `value`/`type`/`description` keys and arbitrary nesting (typical Figma Tokens / Tokens Studio shape) and rewrites it to canonical DTCG with `$`-prefixed keys.

## Why a dedicated DTCG exporter

The four companions emitted by `amw-design-md-emit-companions.py` target four different audiences:

| Companion | Audience |
|---|---|
| `tokens.css` | CSS / SCSS / LESS / vanilla DOM consumers — read with `var(--name)`. |
| `tokens.json` | **Partial** DTCG — sufficient for casual consumers but misses leaves where a group-level `$type` would be needed. |
| `component-inventory.md` | Humans reviewing the system. |
| `usage-prompt.md` | Downstream LLM prompts. |

`tokens.json` was originally a "good enough" DTCG snapshot. As the spec stabilized in 2025 and 2026 it gained a hard requirement that every leaf MUST carry both `$value` and `$type`. Several mainstream consumers (Tokens Studio v2+, Style Dictionary v4+, Specify CLI) now reject JSON that violates this. `amw-dtcg-export.py` is the strict exporter — pair it with the four-companion emitter when full DTCG conformance is the goal, fall back to the casual emitter when only CSS variables are needed.

## DTCG schema mapping

### Leaf shape

Every leaf in the emitted tree has at least these two keys:

```json
{
  "$value": "#1a1c1e",
  "$type": "color"
}
```

When the parent group has a uniform `$type`, the leaf omits its own `$type` and relies on inheritance:

```json
{
  "colors": {
    "$type": "color",
    "primary": { "$value": "#1a1c1e" },
    "secondary": { "$value": "#6c7278" }
  }
}
```

Optional leaf metadata:

- `$description` — a human-readable note. Populated from a sibling `description` field in the source.
- `$extensions` — vendor-specific data. Pass-through when present in harmonize input.

### Group shape and `$type` inheritance

A group is any JSON object that is **not** a leaf — i.e. has no `$value`. The DTCG spec lets a group declare `$type` to set the inherited type for every descendant leaf that omits its own. The exporter sets group-level `$type` for the four monomorphic source groups:

| Source group | Group `$type` |
|---|---|
| `colors` | `color` |
| `rounded` | `dimension` |
| `spacing` | `dimension` |
| `typography` | `typography` (composite) |

`components` is **not** monomorphic — its leaves mix `color`, `dimension`, `typography`, and `string` types. Each component property gets its `$type` on the leaf itself.

### Alias syntax

DTCG aliases use the form `{group.subgroup.token}`. The exporter:

- Recognizes any string matching `^\{[A-Za-z0-9._-]+\}$` as an alias.
- Emits the alias verbatim as the leaf's `$value`.
- Validates that every alias resolves to an existing token before exit. A dangling alias is a contract violation (exit code 3).

Example after export:

```json
{
  "components": {
    "button-primary": {
      "backgroundColor": { "$value": "{colors.primary}", "$type": "color" }
    }
  }
}
```

The consumer resolves `{colors.primary}` to `#1a1c1e` at use time.

### Composite typography tokens

DTCG's `typography` is a composite type whose `$value` is an object of sub-properties. Each typography leaf in DESIGN.md becomes:

```json
{
  "typography": {
    "$type": "typography",
    "headline-lg": {
      "$type": "typography",
      "$value": {
        "fontFamily": "Inter",
        "fontSize": "36px",
        "fontWeight": 600,
        "lineHeight": 1.2
      }
    }
  }
}
```

The leaf keeps its own `$type` even though the group declares one — this is intentional for composite types, where some consumers (notably Style Dictionary v4) require the explicit per-leaf type.

## Source coverage

The exporter recognises the following DESIGN.md frontmatter groups:

| Group | DTCG `$type` | Notes |
|---|---|---|
| `colors` | `color` | Leaves are hex strings or aliases. |
| `typography` | `typography` (composite) | Each leaf is an object of font sub-properties. |
| `rounded` | `dimension` | Leaves are `Npx` strings or aliases. |
| `spacing` | `dimension` | Leaves are `Npx` strings or aliases. |
| `components` | (per-property) | Each property is a leaf; type inferred from property name. |

Top-level scalar metadata (`name`, `version`, `description`) is **not** emitted into the DTCG output — DTCG is a token format, not a manifest. Use a sidecar `manifest.json` if a downstream consumer needs the system name.

Unknown top-level groups are silently skipped (forward-compat: future DESIGN.md sections like `motion`, `elevation`, `border` may be added; the exporter is updated then).

## Harmonize mode

### Bare-key rewrite

Figma Tokens / Tokens Studio / several commercial Figma plugins emit JSON with bare keys:

```json
{
  "color": {
    "brand": {
      "primary": {
        "value": "#1a1c1e",
        "type": "color",
        "description": "Primary brand"
      }
    }
  }
}
```

`--harmonize` walks the tree depth-first and rewrites every leaf:

| Bare key | DTCG key |
|---|---|
| `value` | `$value` |
| `type` | `$type` |
| `description` | `$description` |
| `extensions` | `$extensions` |

Group structure (nesting) is preserved as-is — harmonize never flattens, never re-groups. The consumer keeps their intended hierarchy.

### Type inference for unlabelled leaves

If a harmonize input has a leaf with `value` but no `type`, the exporter infers `$type` from the value shape:

| Value shape | Inferred `$type` |
|---|---|
| `^#[0-9A-Fa-f]{3,8}$` | `color` |
| `^-?\d+(\.\d+)?(px|rem|em|%|pt|vw|vh)$` | `dimension` |
| Integer or float | `number` |
| Alias string | (left untagged — the consumer resolves the target's type) |
| Other strings | (left untagged — validator will flag if no inheritance covers it) |

Inferred types are conservative: a string like `"Inter"` won't be auto-typed as `fontFamily` because nothing in the value shape distinguishes a font name from arbitrary text. Tag explicitly in the source for those cases.

### Idempotence

Running `--harmonize` on an already-DTCG tree returns an equal tree. The script never doubles `$$value` or leaves stale bare keys behind.

## Validation contract

After emission (and before writing output), the script walks the DTCG and asserts:

1. **Every leaf has `$value`.** A "leaf" is detected by the presence of `$value` — pathological cases (e.g. a leaf with only `$description`) trigger a "looks like a leaf but missing $value" error.
2. **Every leaf has an effective `$type`** — either declared on the leaf or inherited from the nearest group ancestor.
3. **Every alias `{path}` resolves** to a token that exists in the same document. Dangling aliases are a hard error.
4. **Every declared `$type` is recognised** — one of the DTCG primitives (`color`, `dimension`, `fontFamily`, `fontWeight`, `fontSize`, `lineHeight`, `letterSpacing`, `duration`, `cubicBezier`, `number`, `string`) or composites (`typography`, `border`, `shadow`, `strokeStyle`, `transition`, `gradient`).

Validation failure exits with code 3. To bypass (for debugging only) use `--no-validate`.

## Round-trip contract with `amw-design-md-emit-companions.py`

The two emitters share the same source-of-truth: the DESIGN.md frontmatter parsed by both scripts via the same code path. Their outputs differ only in shape, not in content:

| Property | `amw-design-md-emit-companions.py --targets json` | `amw-dtcg-export.py` |
|---|---|---|
| Output filename (convention) | `tokens.json` | `tokens.dtcg.json` |
| `$value` on every leaf | yes | yes |
| `$type` on every leaf (own or inherited) | partial — `colors` leaves lack `$type` when group-level was set on a sibling but not the group | yes (always) |
| Group-level `$type` | no | yes (for monomorphic groups) |
| Aliases preserved | yes | yes |
| Composite typography leaves | yes (per-leaf `$type` + `$value` object) | yes (group `$type` + per-leaf `$type` + `$value` object) |
| Validation pre-write | no | yes (exit 3 on contract violation) |

**Use `amw-dtcg-export.py` when** you need full DTCG conformance for downstream consumers like Style Dictionary v4+, Tokens Studio v2+, or Specify CLI. **Use the companions emitter** when you want the four-file bundle (`tokens.css`, `tokens.json`, `component-inventory.md`, `usage-prompt.md`) and DTCG conformance is not a hard requirement.

## CLI reference

```text
amw-dtcg-export.py <input> [-o OUTPUT] [--harmonize] [--no-validate]
```

| Flag | Meaning |
|---|---|
| `<input>` | Path to DESIGN.md, `.json` (Figma Tokens style), or `.yaml`. |
| `-o OUTPUT` | Write DTCG JSON to this path. Default: stdout. |
| `--harmonize` | Required for non-`.md` inputs. Rewrites bare-key nested input to canonical DTCG. |
| `--no-validate` | Skip the post-emit validator. Output may be non-conformant; useful only for debugging. |

Exit codes:

| Code | Meaning |
|---|---|
| 0 | Success — DTCG written. |
| 2 | Invocation / parse error (file missing, malformed JSON/YAML, frontmatter missing on `.md`). |
| 3 | DTCG validation failed (dangling alias, missing `$type`, unknown type, etc). |

## Cross-references

- `TECH-01-yaml-frontmatter.md` — the source format for DESIGN.md.
- `TECH-04-component-tokens.md` — components-section structure.
- `TECH-05-token-references.md` — the `{path}` alias syntax and resolution rules.
- `TECH-12-companion-files.md` — the four-companion emitter (`bin/amw-design-md-emit-companions.py`).
- `TECH-15-design-md-as-input.md` — how downstream tools consume DESIGN.md and its derivatives.
- DTCG Format Module: <https://design-tokens.github.io/community-group/format/>
