---
name: TECH-19-design-md-apply
category: integration
source: agents/amw-wireframe-builder-agent.md, TECH-05-token-references.md, TECH-06-do-donts.md
also-in: TECH-12-companion-files.md, TECH-15-design-md-as-input.md, ../ai-slop-avoid.md
status: stable
---

# TECH: Apply DESIGN.md — token enforcement at code-gen time

## Table of Contents

- [What it does](#what-it-does)
- [When this TECH applies](#when-this-tech-applies)
- [The five-pass apply pipeline](#the-five-pass-apply-pipeline)
  - [Pass 1 — Raw-hex sweep](#pass-1-raw-hex-sweep)
  - [Pass 2 — Raw-px sweep](#pass-2-raw-px-sweep)
  - [Pass 3 — Typography sweep](#pass-3-typography-sweep)
  - [Pass 4 — WCAG contrast pair-check](#pass-4-wcag-contrast-pair-check)
  - [Pass 5 — Do's and Don'ts enforcement](#pass-5-dos-and-donts-enforcement)
- [Replacement table — DESIGN.md slot → CSS-var name](#replacement-table-designmd-slot-css-var-name)
- [Token-resolution algorithm](#token-resolution-algorithm)
- [Failure paths](#failure-paths)
- [Worked example](#worked-example)
- [Cross-references](#cross-references)

## What it does

Documents the **token-enforcement workflow** used by `amw-wireframe-builder-agent` (and any other producer agent that generates HTML / CSS / JSX from a DESIGN.md). The apply step takes a freshly synthesized HTML draft plus the canonical DESIGN.md and rewrites every raw value into a token reference, then verifies WCAG-AA contrast on every emitted color pair, then checks the result against the DESIGN.md's `## Do's and Don'ts` section.

Apply is the **last code-gen step before delivery**. It catches:

- Hard-coded hex like `#2665fd` that should be `var(--color-primary)`.
- Magic numbers like `16px`, `24px` that should be `var(--spacing-md)` or `var(--spacing-lg)`.
- `font-family: Inter, sans-serif` literals that should be `var(--font-body)`.
- Color pairs below WCAG-AA contrast (`< 4.5:1` for normal text, `< 3:1` for large text).
- Generated patterns that violate the DESIGN.md's stated Don'ts.

This is the symmetric inverse of [TECH-15-design-md-as-input](TECH-15-design-md-as-input.md) — that TECH explains how the DESIGN.md is READ at the start of Phase B; this TECH explains how the DESIGN.md is ENFORCED at the end of Phase B before the artifact is shipped.

## When this TECH applies

- `amw-wireframe-builder-agent` has produced a draft HTML and is about to deliver it.
- A producer agent has rendered SVG / JSX / MJML and needs token discipline applied before delivery.
- A user provided both a DESIGN.md and a hand-written HTML draft, and asks: *"normalize this to my design system"*.

This TECH does NOT apply to:

- Wireframe-only deliverables (ASCII sketches, low-fi mockups). Token enforcement happens only on real CSS-emitting artifacts.
- Email templates — those use `tokens.css` companion-file inlining via the `juice` pre-renderer, not runtime `var()` references (email clients don't all support CSS variables). Email's apply pass runs the same pipeline but the output substitutes literal values back in at inline time.

## The five-pass apply pipeline

The pipeline runs deterministically — each pass is idempotent, so re-running apply on an already-applied artifact is a no-op.

### Pass 1 — Raw-hex sweep

Scan the artifact for every `^#[0-9A-Fa-f]{3,8}$` literal. For each, resolve the nearest DESIGN.md color slot (exact hex match preferred; perceptual ΔE76 within 3.0 acceptable for near-matches authored by hand). Rewrite to `var(--color-<slot>)`.

```css
/* before */
.btn-primary { background: #2665fd; color: #ffffff; }

/* after */
.btn-primary { background: var(--color-primary); color: var(--color-on-primary); }
```

Hexes that resolve to NO slot get flagged in `warnings` — the agent declares this an undeclared color and either escalates to the user or selects the closest slot (documented in warnings).

### Pass 2 — Raw-px sweep

Scan for `^-?\d+(\.\d+)?px$` literals on spacing-relevant properties (`padding`, `margin`, `gap`, `inset`, `top`, `right`, `bottom`, `left`, `width`, `height`, `min-*`, `max-*`, `border-radius`). For each, resolve the nearest DESIGN.md `spacing.*` or `rounded.*` slot. Rewrite to `var(--spacing-<slot>)` or `var(--rounded-<slot>)`.

```css
/* before */
.card { padding: 16px; border-radius: 8px; gap: 24px; }

/* after */
.card { padding: var(--spacing-md); border-radius: var(--rounded-md); gap: var(--spacing-lg); }
```

Pixel values that resolve to NO slot (e.g. `1px` for hairlines, `14px` for unusual gutters) stay literal but get listed in `warnings`. The threshold is **exact match only** — a `17px` does NOT round to `var(--spacing-md)` (16px). Round-up nudging requires user approval.

### Pass 3 — Typography sweep

Scan every `font-family`, `font-size`, `font-weight`, `line-height`, `letter-spacing` declaration. For each, resolve the nearest DESIGN.md `typography.<slot>` composite. Rewrite as a single shorthand reference where possible, or as four `var()` lookups.

```css
/* before */
.hero-title {
  font-family: Inter, sans-serif;
  font-size: 48px;
  font-weight: 600;
  line-height: 1.1;
}

/* after */
.hero-title {
  font-family: var(--font-headline-display-family);
  font-size: var(--font-headline-display-size);
  font-weight: var(--font-headline-display-weight);
  line-height: var(--font-headline-display-line-height);
}
```

A DESIGN.md that has emitted the [`tokens.css`](../../amw-design-md/references/TECH-12-companion-files.md) companion makes this trivial — the companion already declares each typography slot as four CSS variables.

### Pass 4 — WCAG contrast pair-check

Every emitted color pair (foreground + background) is checked against WCAG-AA via `bin/amw-design-md-contrast.py` (re-used from authoring). The check walks every `color` / `background-color` adjacency in the HTML — text inside a colored container, link inside a button, badge inside a card.

| Element class | Required ratio |
|---|---|
| Body text < 18pt | 4.5:1 |
| Large text >= 18pt (or >= 14pt bold) | 3.0:1 |
| Non-text UI (icon stroke, focus ring) | 3.0:1 |
| Decorative (no semantic content) | none |

Pairs below the required ratio get logged in `blocking_issues` (not `warnings` — contrast is mandatory). The producer STOPS and either swaps to the DESIGN.md's high-contrast alternative pair (`primary` ↔ `on-primary`) or escalates to the user.

### Pass 5 — Do's and Don'ts enforcement

Read the DESIGN.md's `## Do's and Don'ts` section (Variant 1 §8 / Variant 2 §7 — see [TECH-06-do-donts](../../amw-design-md/references/TECH-06-do-donts.md)). For each Don't, run a heuristic check against the emitted HTML:

| Don't pattern | Heuristic check |
|---|---|
| *"Don't mix corner styles"* | Every `border-radius` resolves to the same DESIGN.md slot (or a documented exception). |
| *"Don't use more than two font weights per page"* | Distinct `font-weight` count across the page is `<= 2`. |
| *"Don't combine the brand color with the alert color"* | No adjacent foreground/background pair where one is `--color-primary` and the other is `--color-error`. |
| *"Don't use raw shadow values; use the elevation tokens"* | No `box-shadow` literals; only `var(--elevation-*)` references. |
| *"Don't put primary buttons next to each other"* | No two `<button class="*primary*">` elements as immediate siblings. |
| *"Use the brand color sparingly"* | `--color-primary` appears `<= N` times where N is user-defined (default 3 occurrences per page). |

Heuristics are best-effort — they catch the high-leverage Don'ts but cannot enforce every nuanced rule. Don'ts that the heuristic engine cannot verify get listed in `warnings` for human review.

## Replacement table — DESIGN.md slot → CSS-var name

Apply uses the same naming scheme as `bin/amw-design-md-emit-companions.py`:

| DESIGN.md frontmatter path | CSS variable |
|---|---|
| `colors.primary` | `--color-primary` |
| `colors.secondary` | `--color-secondary` |
| `colors.tertiary` | `--color-tertiary` |
| `colors.neutral` | `--color-neutral` |
| `colors.surface` | `--color-surface` |
| `colors.on-surface` | `--color-on-surface` |
| `colors.on-primary` (derived) | `--color-on-primary` |
| `colors.error` | `--color-error` |
| `typography.body-md.fontFamily` | `--font-body-md-family` |
| `typography.body-md.fontSize` | `--font-body-md-size` |
| `typography.body-md.fontWeight` | `--font-body-md-weight` |
| `typography.body-md.lineHeight` | `--font-body-md-line-height` |
| `spacing.<slot>` | `--spacing-<slot>` |
| `rounded.<slot>` | `--rounded-<slot>` |
| `components.<name>.<prop>` | `--component-<name>-<prop>` |

If the project already imports `tokens.css` via `<link>` or `<style>`, the variables are already declared and the apply pass simply rewrites the literals — no `:root` block injection needed.

## Token-resolution algorithm

For a given literal value `V` and DESIGN.md group `G` (e.g. `colors`):

1. **Exact match.** If any slot `G.S` has `value == V`, rewrite to `var(--<group>-<S>)`. Stop.
2. **Perceptual near-match** (colors only). Compute ΔE76 between `V` and every `G.S`. If the closest is `< 3.0`, rewrite and log a warning (`"#2664fd nudged to colors.primary (#2665fd, ΔE 0.4)"`). Stop.
3. **Token-reference resolution.** If `V` is already a `{path.to.token}` alias, resolve to the literal first, then re-run the algorithm. See [TECH-05-token-references](../../amw-design-md/references/TECH-05-token-references.md).
4. **No match.** Leave the literal, add a warning listing the offending value. Escalate to user if `blocking_undeclared_values=true` is set.

The algorithm is deterministic, side-effect free, and runs in O(n × |G|) per pass.

## Failure paths

| Failure | Cause | Recovery |
|---|---|---|
| Pass 1/2/3 leaves > 10% of literals unresolved | DESIGN.md is incomplete or the artifact uses an extension surface (shadow / motion) the DESIGN.md doesn't cover | Extend the DESIGN.md with the missing slots (use [extension-sections-10-14](../../amw-design-md-spec/references/extension-sections-10-14.md)) and re-run apply. |
| Pass 4 reports `blocking_issues` | Color pair below WCAG-AA | Swap to the DESIGN.md's high-contrast alternative pair, OR add a `colors.on-<X>` slot, OR escalate to user with the failing pair. |
| Pass 5 heuristic flags a Don't violation | Generated HTML repeats a banned pattern | Re-render the offending section; if the violation is intentional, document it in the agent's `warnings`. |
| Apply loop doesn't converge (same warnings on second pass) | Token-resolution edge case or DESIGN.md mapping ambiguity | Hand-edit the artifact; do NOT re-run apply blindly. |

## Worked example

Input DESIGN.md (excerpt):

```yaml
colors:
  primary: "#2665fd"
  on-primary: "#ffffff"
  surface: "#0b0b0c"
  on-surface: "#f5f5f5"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
rounded:
  md: "8px"
```

Input HTML draft (just the relevant snippet):

```html
<button style="background:#2665fd;color:#ffffff;padding:16px 24px;border-radius:8px;font-family:Inter;font-size:14px;">
  Buy now
</button>
```

After apply:

```html
<button style="background:var(--color-primary);color:var(--color-on-primary);padding:var(--spacing-md) var(--spacing-lg);border-radius:var(--rounded-md);font-family:var(--font-body-md-family);font-size:var(--font-body-md-size);">
  Buy now
</button>
```

`warnings` returned by the apply pass:

```yaml
warnings:
  - "Pass 4: button contrast (#2665fd / #ffffff) is 5.16:1 — passes AA."
  - "Pass 5: 'Use the brand color sparingly' — --color-primary used 1 time in this page (OK)."
```

`blocking_issues` would only appear if the contrast pair had failed.

## Cross-references

- [TECH-05-token-references](../../amw-design-md/references/TECH-05-token-references.md) — the `{path}` alias syntax used in DESIGN.md component specs; apply resolves these eagerly before Pass 1
- [TECH-06-do-donts](../../amw-design-md/references/TECH-06-do-donts.md) — what `## Do's and Don'ts` looks like; Pass 5 reads from this section
- [TECH-11-validation-and-lint](../../amw-design-md/references/TECH-11-validation-and-lint.md) — `bin/amw-design-md-contrast.py` is re-used in Pass 4
- [TECH-12-companion-files](../../amw-design-md/references/TECH-12-companion-files.md) — the tokens.css companion declares the `var()` names that apply rewrites literals to
- [TECH-15-design-md-as-input](./TECH-15-design-md-as-input.md) — the symmetric inverse: how DESIGN.md is read at the START of Phase B
- [TECH-18-figma-input-path](../../amw-design-md-extract/references/TECH-18-figma-input-path.md) — Figma → DESIGN.md (upstream); apply runs on the artifact built from the imported tokens
- [TECH-20-design-library](./TECH-20-design-library.md) — cross-project DESIGN.md library; apply consumes the same DESIGN.md regardless of source
- [ai-slop-avoid](../../amw-design-md-audit/references/ai-slop-avoid.md) — Pass 5 escalation cases overlap with the slop checklist
- [amw-wireframe-builder-agent](../../../agents/amw-wireframe-builder-agent.md) — primary consumer of this TECH
