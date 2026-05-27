# TECH-16 — Figma Tokens Studio JSON ↔ DESIGN.md bridge

A bidirectional bridge between DESIGN.md (Variant 1, the `@google/design.md`
canonical schema) and the JSON file format used by the **Tokens Studio for
Figma** plugin (https://github.com/tokens-studio/figma-plugin).

The bridge lets a designer round-trip tokens between Figma (Tokens Studio
plugin) and an AI-agent codebase (DESIGN.md) without manual re-keying.

## Scripts

| Direction | Script | Inputs | Output |
|---|---|---|---|
| Import | `bin/amw-figma-tokens-import.py` | `figma-tokens.json` | `DESIGN.md` |
| Export | `bin/amw-figma-tokens-export.py` | `DESIGN.md` | `figma-tokens.json` |

Both are pure Python, stdlib + PyYAML only — no Node, no Figma Desktop, no
network. They run in CI and in a fresh checkout without bootstrap.

## Supported Tokens Studio JSON shapes

The Tokens Studio plugin ships its export in two interchangeable shapes; the
importer accepts both, the exporter defaults to the classic shape and can be
told to emit the modern shape with `--dtcg`.

**Classic shape (current default emit form, widely-supported):**

```json
{
  "global": {
    "colors": {
      "primary": { "value": "#2563EB", "type": "color" }
    }
  },
  "$themes": [],
  "$metadata": { "tokenSetOrder": ["global"] }
}
```

**DTCG (W3C Design Tokens Community Group) shape:**

```json
{
  "global": {
    "colors": {
      "primary": { "$value": "#2563EB", "$type": "color" }
    }
  }
}
```

The two shapes differ only in the leaf keys (`value`/`type` vs `$value`/`$type`).
The plugin accepts both on import.

### Multi-set files

Tokens Studio supports multiple **sets** (e.g. `light` / `dark`, or feature-set
slices). A multi-set file looks like:

```json
{
  "light": { "colors": { "primary": { "value": "#FFFFFF", "type": "color" } } },
  "dark":  { "colors": { "primary": { "value": "#000000", "type": "color" } } },
  "$themes": [],
  "$metadata": { "tokenSetOrder": ["light", "dark"] }
}
```

The importer's default is to **merge all sets in `tokenSetOrder` order** — later
sets override earlier ones on key collision, mirroring Tokens Studio's runtime
"merge sets" semantic. To pick a single set, pass `--set <name>`.

## Schema mapping

The DESIGN.md frontmatter slot ↔ Tokens Studio group mapping is fixed and
deterministic:

| DESIGN.md slot | Tokens Studio group | Type tag |
|---|---|---|
| `colors.primary` | `colors.primary` | `color` |
| `colors.secondary` | `colors.secondary` | `color` |
| `colors.tertiary` | `colors.tertiary` | `color` |
| `colors.neutral` | `colors.neutral` | `color` |
| `colors.surface` | `colors.surface` | `color` |
| `colors.on-surface` | `colors.on-surface` | `color` |
| `colors.error` | `colors.error` | `color` |
| `typography.<slot>` | `typography.<slot>` | `typography` (composite) |
| `spacing.<slot>` | `spacing.<slot>` | `spacing` |
| `rounded.<slot>` | `borderRadius.<slot>` | `borderRadius` |
| `components.<name>.*` | `components.<name>.*` | (heuristic) |

The DESIGN.md slot name is the source of truth on export. On import, the
classifier matches Tokens Studio token paths case-insensitively against the
slot's name plus a small set of synonyms (e.g. `accent` → `secondary`,
`background` → `surface`, `gray` → `neutral`). The first match wins.

### Typography composite

DESIGN.md emits typography per-slot as a YAML sub-mapping:

```yaml
typography:
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0em
```

The bridge maps this 1:1 to Tokens Studio's composite `typography` token:

```json
"body-md": {
  "value": {
    "fontFamily": "Inter",
    "fontSize": "16px",
    "fontWeight": 400,
    "lineHeight": 1.5,
    "letterSpacing": "0em"
  },
  "type": "typography"
}
```

Tokens Studio recognizes composite typography tokens; Figma writes them as text
styles when applied.

## Round-trip lossiness contract

The round-trip is **lossy-but-equivalent** for the canonical token surface.
After two legs (`figma-tokens.json` → `DESIGN.md` → `figma-tokens.json` → `DESIGN.md`)
the following are guaranteed bit-stable:

- Color hex (case-folded to uppercase `#RRGGBB`, alpha `#RRGGBBAA`)
- Font family, font size (px), font weight, line height, letter spacing
- Spacing px values
- Border-radius px values

The following are **dropped on import** (and therefore absent from the second
half of any round-trip):

| Lost surface | Reason | Workaround |
|---|---|---|
| `boxShadow` (drop shadows, inner shadows) | DESIGN.md has no shadow frontmatter block; shadow philosophy lives in prose. | Re-author `## Elevation & Depth` by hand. |
| Gradient color stops | DESIGN.md colors are single-value tokens. | Importer keeps the first gradient stop's hex; document the gradient in prose. |
| `fontFamilies`, `fontWeights`, `letterSpacing`, `lineHeights` as standalone groups | DESIGN.md folds those into the per-slot composite token. | Pass the composite `typography` token instead. |
| Token references (`{colors.primary}`) inside Tokens Studio data | DESIGN.md tokens are concrete values, not refs (refs only appear inside the `components` block). | Bridge resolves refs eagerly on the import leg. |
| Tokens Studio `$themes` matrix | DESIGN.md has no theme-toggle surface. | Pick one theme via `--set <theme>`, or merge all and accept later-set-wins. |

The lossy surface is the bridge's hard contract, **not a bug list**. Reconstructing
shadow tokens or theme matrices would require DESIGN.md schema extensions
outside Variant 1; that is intentionally out of scope.

## Round-trip stability table

| Token kind | After leg 1 | After leg 2 | After leg 3 (input ↔ ?) | Stable? |
|---|---|---|---|---|
| Color hex `#2563EB` | preserved | preserved | preserved | YES |
| Color RGB short `#abc` | normalized to `#AABBCC` | preserved | preserved | YES (after first import) |
| Color RGBA `rgba(255,0,0,0.5)` | normalized to `#FF000080` | preserved | preserved | YES (after first import) |
| Color gradient | first-stop hex | preserved | preserved | YES (other stops gone) |
| Font family `Inter` | preserved | preserved | preserved | YES |
| Font size `16px` | preserved | preserved | preserved | YES |
| Font weight `400` | preserved | preserved | preserved | YES |
| Line height `1.5` (unitless) | preserved | preserved | preserved | YES |
| Letter spacing `-0.01em` | preserved | preserved | preserved | YES |
| Spacing `16px` | preserved | preserved | preserved | YES |
| Border radius `8px` | preserved | preserved | preserved | YES |
| Box shadow | DROPPED | — | — | NO (intentional) |
| Token reference `{colors.primary}` | RESOLVED | resolved-as-concrete | resolved-as-concrete | NO (intentional) |

## CLI surface

### Import

```bash
amw-figma-tokens-import.py <figma-tokens.json> -o <DESIGN.md> [--set <name>] [--name <title>]
```

| Flag | Meaning |
|---|---|
| `<figma-tokens.json>` | Input path (Tokens Studio JSON, classic or DTCG, single- or multi-set) |
| `-o <DESIGN.md>` | Output path; parent dirs are created |
| `--set <name>` | In a multi-set file, import only that set (default: merge all in `tokenSetOrder` order) |
| `--name <title>` | Design system name to embed as `name:` in frontmatter (default: derived from the input filename) |
| `--variant 1` | Currently the only supported output variant; reserved for future Variant 2 support |

Exit codes: `0` success, `1` invalid input JSON, `2` invocation error.

### Export

```bash
amw-figma-tokens-export.py <DESIGN.md> -o <figma-tokens.json> [--dtcg]
```

| Flag | Meaning |
|---|---|
| `<DESIGN.md>` | Input DESIGN.md with valid YAML frontmatter |
| `-o <figma-tokens.json>` | Output path; parent dirs are created |
| `--dtcg` | Emit DTCG-style (`$value`/`$type`) keys instead of classic (`value`/`type`); both are valid Tokens Studio imports |

Exit codes: `0` success, `1` invalid DESIGN.md frontmatter, `2` invocation error.

## Validation

After import, run the standard validation chain — this catches importer bugs
where a slot got missed or a hex normalized incorrectly:

```bash
bin/amw-design-md-lint.sh DESIGN.md           # @google/design.md alpha lint
bin/amw-design-md-validate.py DESIGN.md       # offline structural lint
bin/amw-design-md-contrast.py DESIGN.md       # WCAG AA contrast pair sweep
```

The importer's emitted frontmatter is structured to pass the official linter
with no manual fixup.

## Cross-references

- `TECH-01-yaml-frontmatter.md` — frontmatter schema
- `TECH-02-color-tokens.md` — color token spec
- `TECH-03-typography-tokens.md` — typography composite spec
- `TECH-04-component-tokens.md` — component token spec (export-only; importer
  cannot infer per-component tokens from Tokens Studio's flat groups)
- `TECH-07-url-extraction.md` — alternative extraction path (live URL → DESIGN.md)
- `TECH-08-codebase-extraction.md` — alternative extraction path (codebase scan)
- `TECH-11-validation-and-lint.md` — full lint chain
- `TECH-12-companion-files.md` — emit `tokens.css` / `tokens.json` from DESIGN.md
- `canonical-template.md` — the Variant 1 schema this bridge targets

## Test coverage

`tests/test_amw_figma_tokens_roundtrip.py` exercises:

1. Classic shape import → DESIGN.md
2. DTCG shape import → DESIGN.md
3. Short-hex (`#abc`) and `rgba()` color normalization
4. Multi-set merge (later-set wins) and explicit `--set` selection
5. DESIGN.md → classic Tokens Studio JSON
6. DESIGN.md → DTCG Tokens Studio JSON
7. Three-leg round-trip preserves every canonical color, spacing, radius, and
   composite typography value
8. Invocation errors (missing file, invalid JSON, missing frontmatter)
9. `--help` returncode `0` on both scripts

Run via `uv run --with pyyaml pytest tests/test_amw_figma_tokens_roundtrip.py -v`.
