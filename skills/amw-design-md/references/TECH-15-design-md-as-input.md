---
name: TECH-15-design-md-as-input
category: integration
source: agents/amw-wireframe-builder-agent.md, claudesign-main, design-harness-main
also-in: TECH-12-companion-files.md, TECH-11-validation-and-lint.md
status: stable
---

# TECH: How DESIGN.md is consumed downstream (Phase B)

## Table of Contents

- [What it does](#what-it-does)
- [When this TECH applies](#when-this-tech-applies)
- [The wireframe-builder's flow when DESIGN.md is the input](#the-wireframe-builders-flow-when-designmd-is-the-input)
- [Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape](#token-mapping-designmd-to-wireframe-builders-brand_tokens-shape)
- [Component tokens — direct passthrough](#component-tokens-direct-passthrough)
- [Failure paths](#failure-paths)
  - [DESIGN.md fails lint](#designmd-fails-lint)
  - [DESIGN.md is Variant 2](#designmd-is-variant-2)
  - [DESIGN.md missing required fields](#designmd-missing-required-fields)
- [CLAUDE.md-coupled projects](#claudemd-coupled-projects)
- [Companion-file consumption](#companion-file-consumption)
- [Symmetry with non-DESIGN.md inputs](#symmetry-with-non-designmd-inputs)
- [Cross-references](#cross-references)

## What it does

Documents how the plugin's downstream Phase B agents — chiefly `amw-wireframe-builder-agent` — consume a DESIGN.md as their canonical token source. This is the LAST step in the DESIGN.md lifecycle: after authoring / extraction / validation, the DESIGN.md drives actual UI generation.

The flow is symmetric with the plugin's other input formats. DESIGN.md is ONE OF SIX peer input formats (per the user-guidance peer-input principle):

1. User-provided DESIGN.md (Variant 1 or Variant 2)
2. User-provided ASCII wireframe / sketch
3. User-provided mockup image
4. User-provided slideshow
5. User-said "copy style from this URL"
6. User-described wishes in prose only

When the input is a DESIGN.md, the wireframe-builder treats its tokens as canonical. When the input is one of the other 5, the wireframe-builder gets tokens from a different source (brand-researcher, design-extract, or design-principles defaults).

## When this TECH applies

- A user provided a DESIGN.md and the orchestrator is now in Phase B (rendering HTML).
- A user wants the wireframe-builder to use a recently authored / extracted DESIGN.md as the token source.

## The wireframe-builder's flow when DESIGN.md is the input

```
                ┌───────────────────────────────────────┐
                │ Main-agent enters Phase B with        │
                │ DESIGN.md path as input               │
                └────────────────┬──────────────────────┘
                                 │
                                 ▼
                ┌───────────────────────────────────────┐
                │ amw-wireframe-builder-agent §9 row:   │
                │ "If user provided DESIGN.md, parse    │
                │  it BEFORE generating HTML"            │
                └────────────────┬──────────────────────┘
                                 │
                                 ▼
                ┌───────────────────────────────────────┐
                │ Step 1: Validate via                  │
                │ bin/amw-design-md-lint.sh DESIGN.md   │
                └────────────────┬──────────────────────┘
                                 │
                          Pass? ─┴── Fail?
                            │            │
                            │            ▼
                            │     STOP — return failed
                            │     with blocking_issues
                            │     "DESIGN.md fails lint"
                            │
                            ▼
                ┌───────────────────────────────────────┐
                │ Step 2: Detect variant                │
                │ - V1: parse YAML frontmatter          │
                │ - V2: convert to V1 first via         │
                │   bin/amw-design-md-convert-v2-to-v1  │
                └────────────────┬──────────────────────┘
                                 │
                                 ▼
                ┌───────────────────────────────────────┐
                │ Step 3: Resolve token references      │
                │ Walk YAML tree, resolve all           │
                │ {path.to.token} into literal values   │
                └────────────────┬──────────────────────┘
                                 │
                                 ▼
                ┌───────────────────────────────────────┐
                │ Step 4: Map to brand_tokens shape     │
                │ used by the wireframe-builder         │
                │ (colors, fonts, spacing_unit, radius) │
                └────────────────┬──────────────────────┘
                                 │
                                 ▼
                ┌───────────────────────────────────────┐
                │ Step 5: Render HTML using these       │
                │ tokens — same path as if tokens came  │
                │ from brand-researcher or              │
                │ design-extract                         │
                └───────────────────────────────────────┘
```

## Token mapping — DESIGN.md to wireframe-builder's `brand_tokens` shape

Wireframe-builder's input contract uses this `brand_tokens` shape:

```yaml
brand_tokens:
  colors:
    primary: "#0a2540"
    accent:  "#f0c14b"
    bg:      "#0b0b0c"
    text:    "#f5f5f5"
    muted:   "#8a8a8a"
    danger:  "#d7263d"
  fonts:
    display: "Bebas Neue"
    body:    "Montserrat"
  spacing_unit: 8
  radius:      12
  source:      "design-md"
```

When the source is a DESIGN.md, the agent maps:

| `brand_tokens` field | Source from DESIGN.md frontmatter |
|---|---|
| `colors.primary` | `colors.primary` |
| `colors.accent` | `colors.tertiary` (preferred) OR `colors.secondary` |
| `colors.bg` | `colors.surface` OR `colors.neutral` |
| `colors.text` | `colors.on-surface` OR derived (the high-contrast pair to bg) |
| `colors.muted` | `colors.secondary` (if used for muted text) |
| `colors.danger` | `colors.error` |
| `fonts.display` | `typography.headline-display.fontFamily` OR largest typography level |
| `fonts.body` | `typography.body-md.fontFamily` |
| `spacing_unit` | derived from `spacing.base` (or median of `spacing.*` differences) |
| `radius` | `rounded.md` (most-common interactive radius) |
| `source` | `"design-md"` |

If a mapping is ambiguous (e.g., DESIGN.md has `secondary` and `tertiary` but the wireframe-builder needs one `accent`), the agent picks the one most commonly used as the brand-identity color (heuristic: the one referenced by `button-primary.backgroundColor` or `button-primary-hover`).

The agent documents the mapping decisions in its return contract `warnings`:

```yaml
warnings:
  - "DESIGN.md has both 'secondary' (#6c7278) and 'tertiary' (#b8422e). Mapped 'tertiary' to brand_tokens.accent (referenced by button-primary). Mapped 'secondary' to brand_tokens.muted."
```

## Component tokens — direct passthrough

When DESIGN.md declares `components.*` entries, the wireframe-builder consumes them directly. For example, a `components.button-primary.padding: "12px"` is rendered as a CSS `padding: 12px` declaration on the button element. The wireframe-builder does NOT re-derive button styles from base brand tokens when the DESIGN.md gave explicit component specs.

Hierarchy of resolution:
1. If DESIGN.md has `components.button-primary` → use it directly.
2. Else if DESIGN.md has `colors.primary` + `typography.label-md` → derive a button-primary style.
3. Else fall back to design-principles defaults.

## Failure paths

### DESIGN.md fails lint

The wireframe-builder STOPS. It does not silently substitute design-principles defaults. The user must fix the DESIGN.md or remove it from the inputs.

```yaml
status: failed
blocking_issues:
  - "DESIGN.md at <path> fails official linter (S2: YAML parse error at line 14)."
  - "Cannot proceed to HTML rendering with invalid DESIGN.md."
recommendations:
  - "Run /amw-design-md-lint /path/to/DESIGN.md and fix the reported errors."
  - "Alternatively, remove DESIGN.md from the input and provide brand_tokens directly."
next_action: escalate_to_user
```

### DESIGN.md is Variant 2

The wireframe-builder converts to Variant 1 internally (via `bin/amw-design-md-convert-v2-to-v1.py`), then proceeds. The conversion warning is noted:

```yaml
warnings:
  - "Input DESIGN.md is Variant 2 (community 9-section); converted to Variant 1 internally before token mapping."
```

### DESIGN.md missing required fields

If `colors.primary` is absent (the only required color token), the wireframe-builder cannot resolve `brand_tokens.colors.primary`. It returns `partial`:

```yaml
status: partial
warnings:
  - "DESIGN.md missing colors.primary. Falling back to design-principles default #0a2540 for brand_tokens.colors.primary."
```

The user accepts the fallback or provides a corrected DESIGN.md.

## CLAUDE.md-coupled projects

When a project uses DESIGN.md AND has `CLAUDE.md` snippet from [claude-md-snippet](claude-md-snippet.md), the wireframe-builder reads BOTH:

- DESIGN.md as the token source.
- CLAUDE.md as additional do/don't rules layered on top.

If CLAUDE.md states "always use the primary color sparingly", that becomes a rendering constraint. The wireframe-builder's `## Do's and Don'ts` integration step (existing) checks against both sources.

## Companion-file consumption

If `tokens.css` and `tokens.json` companion files exist alongside DESIGN.md (in the same directory), the wireframe-builder MAY use `tokens.css` directly via a `<style>` import in the rendered HTML. This is preferred for projects with a strict design-system vs ad-hoc inline styles. The agent's choice is documented in `warnings`.

## Symmetry with non-DESIGN.md inputs

The wireframe-builder's behavior with the other 5 input formats is symmetric:

| Input | Token source |
|---|---|
| ASCII wireframe + brand-researcher tokens | `brand_tokens` from `amw-brand-researcher-agent` output |
| Mockup image | `brand_tokens` derived from image color clustering OR design-principles defaults |
| Slideshow | Tokens from the slideshow's metadata frontmatter or design-principles defaults |
| URL "copy this style" | `brand_tokens` from `amw-design-extract` skill or `bin/amw-design-md-from-url.sh` |
| Prose only | `brand_tokens` synthesized from `amw-brand-researcher-agent` interview OR design-principles defaults |
| **DESIGN.md** | `brand_tokens` mapped from the DESIGN.md frontmatter |

In all 6 cases, the wireframe-builder's `brand_tokens` input contract is the same shape. The DESIGN.md is one of several legitimate source paths — not privileged, not penalized.

## Cross-references

- [amw-wireframe-builder-agent](../../../agents/amw-wireframe-builder-agent.md) — the agent that consumes
- [TECH-12-companion-files](./TECH-12-companion-files.md) — alternative consumption via tokens.css
  > What it does · The four companions · tokens.css — CSS custom properties · tokens.json — W3C Design Tokens format · component-inventory.md — human-readable component list · usage-prompt.md — Drop-in agent prompt · Inputs to the emitter · Resolution behavior · Synchronization rule · Cross-references
- [TECH-11-validation-and-lint](./TECH-11-validation-and-lint.md) — the lint gate
  > What it does · The three validators · Official linter (`bin/amw-design-md-lint.sh`) · Pure-Python offline validator (`bin/amw-design-md-validate.py`) · Contrast checker (`bin/amw-design-md-contrast.py`) · Standard validation chain · Lint failure → recovery · Diff between two DESIGN.md files · CI integration suggestion (out-of-scope but documented) · Cross-references
- [TECH-13-converting-variant2-to-1](./TECH-13-converting-variant2-to-1.md) — V2 input handling
  > What it does · When to use · When NOT to use · Conversion overview · Token extraction from V2 prose · Colors · Typography · Spacing · Rounded · Components · Mermaid state diagram · Sections 8-9 merging · Information that may be lost · Inputs · Validation after conversion · Round-trip notes · Cross-references
- [claude-md-snippet](./claude-md-snippet.md) — coupled CLAUDE.md
  > Snippet — paste into the project's `CLAUDE.md` · Where this goes in CLAUDE.md · What `{{placeholders}}` get filled with · Cross-references
