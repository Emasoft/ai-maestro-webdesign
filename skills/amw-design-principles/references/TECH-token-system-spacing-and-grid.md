<!--
Sources: Material Design 8dp grid (Apache-2.0, https://m2.material.io/design/layout/spacing-methods.html) — direct-port of the 4/8 baseline rationale; Tailwind v4 spacing scale (MIT, https://tailwindcss.com/docs/customizing-spacing) — direct-port of the named-step scale; Bootstrap 12-col grid + 6-breakpoint system (MIT) — direct-port of column/breakpoint counts.
Synthesis novel to this plugin: density-mode multiplier (see TECH-token-system-density-modes.md), inline/block axis token split, breaks-if invariants. Clean-room beyond the cited sources.
-->

---
name: TECH-token-system-spacing-and-grid
category: design-principles-tokens
source: Material 8dp + Tailwind step scale + Bootstrap 12-col direct-port (batch9 Wave 2 Round 3, T-076/T-077/T-078)
license: this file = MIT (plugin license); upstreams are Apache-2.0 / MIT with attribution preserved in the HTML-comment header above
also-in: TECH-token-system-density-modes.md (compact/comfortable/spacious multiplier table); TECH-css-variable-discipline.md (raw `p-4`/`gap-3` is OK, raw `px-[17px]` is not — only token-scaled values); TECH-landing-anatomy.md (section-rhythm spacing budget)
---

# Token system — 4/8pt grid, spacing scale, responsive grid

## Table of Contents

- [What this is](#what-this-is)
- [The 4/8pt baseline](#the-48pt-baseline)
- [The 10-step spacing scale](#the-10-step-spacing-scale)
- [Inline vs block axis tokens](#inline-vs-block-axis-tokens)
- [Responsive grid — 12-col / 16-col + breakpoints](#responsive-grid--12-col--16-col--breakpoints)
- [Token block — canonical declaration](#token-block--canonical-declaration)
- [Breaks if](#breaks-if)
- [Component example A — card grid with section rhythm](#component-example-a--card-grid-with-section-rhythm)
- [Component example B — form field stack](#component-example-b--form-field-stack)
- [Cross-references](#cross-references)

## What this is

Spacing in this plugin is **token-quantized to a base unit of 4 px**, expanded into a 10-step semantic scale, and projected onto a responsive **12-column** (or 16-column for editorial dashboards) grid with a fixed breakpoint ladder. Off-grid values (`17px`, `5px`, `marginTop: 13`) are forbidden — they look improvised because they are. The 4pt grid is the smallest unit that survives 2× rendering on most displays without sub-pixel rounding artefacts, and 8pt is the smallest "rhythm" unit the eye reads as deliberate spacing.

This file gives the baseline rationale, the 10-step scale with when-to-use guidance, the inline/block axis split, the 12-col/16-col grid contract, the canonical token block, and the breaks-if invariants.

## The 4/8pt baseline

**Why 4 and 8.**

| Reason | 4pt | 8pt |
|---|---|---|
| Sub-pixel safety at 2× displays | 4 × 2 = 8 physical pixels; integer-aligned | 8 × 2 = 16; same |
| Smallest perceptually distinct gap | 4 reads as "tight but breathing" | 8 reads as "clearly separated" |
| Conversion to Tailwind / 8pt baselines | `4 = 0.25rem = 4px`; matches `space-1`/`gap-1` | `8 = 0.5rem = 8px`; matches `space-2`/`gap-2` |
| Designer tooling | Figma's nudge step is 8 by default; Sketch's is 8 | — |

**Rule.** Every spacing value used in markup MUST resolve to a multiple of 4 px. The 10-step scale below covers the multiples worth naming; arbitrary multiples (e.g., 20 px, 36 px) are allowed only when they sit on the 4pt grid AND have a semantic reason. Random multiples (13 px, 17 px, 22 px) are forbidden.

The 4pt grid trumps the 8pt grid in **two cases**:
1. Icon/avatar internal spacing — 4 px makes the difference between cramped and balanced inside a 24×24 glyph.
2. Caption/badge internal padding — 4 px reads as deliberate; 8 px reads as oversized.

Everywhere else (sections, cards, forms, body copy), prefer 8 px multiples.

## The 10-step spacing scale

The scale is named by step. Every spacing token in DESIGN.md is one of these.

| Step | Value (px) | Value (rem) | Used for |
|---|---|---|---|
| `--space-0` | 0 | 0 | Reset only — flush to edge |
| `--space-1` | 4 | 0.25 | Icon/glyph internal padding; tight badge / chip padding |
| `--space-2` | 8 | 0.5 | Tight stack (between label + input on a single field); inline gap (icon + text in a button) |
| `--space-3` | 12 | 0.75 | Default button vertical padding; chip-to-chip gap |
| `--space-4` | 16 | 1 | Default card body padding; default form-field vertical rhythm |
| `--space-5` | 24 | 1.5 | Section internal padding (within a hero block, within a feature panel) |
| `--space-6` | 32 | 2 | Card-to-card gap in a grid; default vertical rhythm between H2 sections in body content |
| `--space-7` | 48 | 3 | Top-of-section margin (between major page sections); hero text-to-CTA spacing |
| `--space-8` | 64 | 4 | Page-section gap on desktop (between hero / features / pricing / footer blocks) |
| `--space-9` | 96 | 6 | Hero block top/bottom padding; major editorial spacing |
| `--space-10` | 128 | 8 | Largest deliberate gap — between full-width feature stages on a long landing page |

**When to use each step (the rhythm doctrine):**

- **Steps 1–3** are *intra-component*. Inside a button, inside a chip, inside a field. Choose by component density: dense (1), default (2), spacious (3).
- **Steps 4–6** are *inter-component*. Between fields in a form, between cards in a grid, between H2 sections in body content. Choose by reading direction: dense list (4), default grid (5), open editorial (6).
- **Steps 7–10** are *inter-section*. Between hero and features, between features and pricing, between pricing and footer. Choose by page length: short page (7), default landing (8), editorial long-form (9-10).

Skipping a step is allowed (you can go from 4 to 6 to 8). Inverting a step (a smaller value below a larger one in the same context) is forbidden — it breaks rhythm.

## Inline vs block axis tokens

Spacing is **directional**. The plugin uses logical-property tokens, not physical ones:

| Token | CSS property | Meaning |
|---|---|---|
| `--space-inline-N` | `padding-inline`, `margin-inline`, `gap` | Horizontal in LTR; horizontal in RTL too (logical) |
| `--space-block-N` | `padding-block`, `margin-block`, row-gap | Vertical |
| `--space-N` | (uni-directional fallback) | Use when both axes use the same value |

For LTR/RTL-safe layouts, prefer `padding-inline: var(--space-4)` over `padding-left: 16px`. The 10-step scale above applies to both axes; the same token can be used inline or block. Inline gaps for buttons (`padding-inline: var(--space-4)`) are usually one step larger than block gaps for the same component (`padding-block: var(--space-3)`) — buttons read better wider than tall.

## Responsive grid — 12-col / 16-col + breakpoints

**Two grids, one choice.**

| Grid | When | Why |
|---|---|---|
| **12-column** | Default for landing pages, marketing, blogs, dashboards | 12 factors into 2, 3, 4, 6 — every common layout (halves, thirds, quarters, sixths) is grid-aligned |
| **16-column** | Editorial / data-dense dashboards / spreadsheets / multi-pane apps | 16 factors into 2, 4, 8 — more fine-grained column slices for chart layouts; common in design-tool UIs |

A page picks one and sticks with it. Mixing 12-col and 16-col regions on the same page produces a layout that "feels jittery" because the gutter rhythm shifts mid-page.

**The breakpoint ladder.** Tailwind-default-aligned, but the tokens are first-class:

| Breakpoint token | Min viewport (px) | Min viewport (rem) | Typical device |
|---|---|---|---|
| `--bp-xs` | 0 | 0 | Mobile portrait |
| `--bp-sm` | 640 | 40 | Large mobile / small tablet portrait |
| `--bp-md` | 768 | 48 | Tablet portrait / small landscape |
| `--bp-lg` | 1024 | 64 | Tablet landscape / small desktop |
| `--bp-xl` | 1280 | 80 | Desktop default |
| `--bp-2xl` | 1536 | 96 | Large desktop |

**Gutter widths per breakpoint.** Gutter ≠ section margin; gutter is the gap between columns.

| Breakpoint | 12-col gutter | 16-col gutter |
|---|---|---|
| `--bp-xs` to `--bp-sm` | `var(--space-4)` (16) | `var(--space-3)` (12) |
| `--bp-md` to `--bp-lg` | `var(--space-5)` (24) | `var(--space-4)` (16) |
| `--bp-xl` and above | `var(--space-6)` (32) | `var(--space-5)` (24) |

**Max content width.** The container has a max width to keep line length readable:

| Container token | Max width (px) | When |
|---|---|---|
| `--container-prose` | 720 | Long-form text (blog post, article, docs page) — 65–75 char measure |
| `--container-default` | 1200 | Standard landing / marketing |
| `--container-wide` | 1440 | Dashboard / app shell — uses more horizontal real estate |
| `--container-full` | 100% | Edge-to-edge (footer band, hero with full-bleed background) |

## Token block — canonical declaration

```css
:root {
  /* Base unit — never change. Every other spacing is a multiple of this. */
  --space-unit: 4px;

  /* 10-step spacing scale (multiples of --space-unit) */
  --space-0:  0;
  --space-1:  0.25rem;   /* 4 */
  --space-2:  0.5rem;    /* 8 */
  --space-3:  0.75rem;   /* 12 */
  --space-4:  1rem;      /* 16 */
  --space-5:  1.5rem;    /* 24 */
  --space-6:  2rem;      /* 32 */
  --space-7:  3rem;      /* 48 */
  --space-8:  4rem;      /* 64 */
  --space-9:  6rem;      /* 96 */
  --space-10: 8rem;      /* 128 */

  /* Logical-axis aliases (LTR/RTL-safe) */
  --space-inline-1: var(--space-1);
  --space-inline-2: var(--space-2);
  --space-inline-3: var(--space-3);
  --space-inline-4: var(--space-4);
  --space-inline-5: var(--space-5);
  --space-inline-6: var(--space-6);
  --space-block-1:  var(--space-1);
  --space-block-2:  var(--space-2);
  --space-block-3:  var(--space-3);
  --space-block-4:  var(--space-4);
  --space-block-5:  var(--space-5);
  --space-block-6:  var(--space-6);

  /* Grid + breakpoints */
  --grid-columns: 12;
  --grid-gutter:  var(--space-5);    /* 24 — desktop default; override per breakpoint */
  --bp-xs:  0px;
  --bp-sm:  40rem;     /* 640 */
  --bp-md:  48rem;     /* 768 */
  --bp-lg:  64rem;     /* 1024 */
  --bp-xl:  80rem;     /* 1280 */
  --bp-2xl: 96rem;     /* 1536 */

  /* Container widths */
  --container-prose:   45rem;     /* 720 */
  --container-default: 75rem;     /* 1200 */
  --container-wide:    90rem;     /* 1440 */
}

/* Gutter narrows on small viewports for content-density preservation */
@media (max-width: 48rem) {
  :root { --grid-gutter: var(--space-4); }   /* 16 on mobile */
}
@media (min-width: 80rem) {
  :root { --grid-gutter: var(--space-6); }   /* 32 on large desktop */
}
```

Dashboards / 16-col layouts override `--grid-columns: 16` in the page-shell scope, not at `:root`.

## Breaks if

The auditor and wireframe builder reject the spacing block when any of the following holds:

- A markup or `<style>` value uses a spacing that does not resolve to a multiple of 4 (e.g., `padding: 17px`, `margin-top: 13px`, `gap: 5px`).
- A markup or `<style>` value uses an off-token literal even if 4-aligned (e.g., `padding: 20px` — 20 is between `--space-5`=24 and `--space-4`=16, on the grid but not on the named scale).
- The spacing scale is missing any of steps 0–10.
- The scale uses values that are NOT a multiple of `--space-unit` (4 px) — e.g., declaring `--space-3: 10px`.
- A vertical rhythm crosses an inversion: large gap (`--space-8`) above a small gap (`--space-3`) above a medium gap (`--space-6`) — eye loses the cadence.
- Both 12-col and 16-col grids are used on the same page (mix breaks gutter rhythm).
- `--container-prose` is used for a non-prose context (e.g., a marketing landing — the 720 px cap makes the layout cramped).
- A breakpoint is declared off the canonical ladder (e.g., `@media (min-width: 900px)`) — use one of `--bp-{sm,md,lg,xl,2xl}` instead.
- Mobile gutter exceeds desktop gutter (gutters should grow with viewport, not shrink).
- A grid template skips columns randomly (`grid-template-columns: 1fr 2fr 1fr 5fr`) — column ratios should derive from the 12-or-16-col base.

## Component example A — card grid with section rhythm

A three-card feature grid with proper inter-section + inter-card rhythm:

```html
<section class="feature-section">
  <h2 style="margin-block-end: var(--space-5);">What you get</h2>

  <div class="feature-grid">
    <article class="feature-card">…</article>
    <article class="feature-card">…</article>
    <article class="feature-card">…</article>
  </div>
</section>

<style>
  .feature-section {
    padding-block: var(--space-8);        /* 64 — inter-section rhythm */
    padding-inline: var(--space-4);
    max-width: var(--container-default);
    margin-inline: auto;
  }

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-6);                  /* 32 — inter-card rhythm */
  }

  .feature-card {
    padding: var(--space-5);              /* 24 — intra-card */
    background: var(--color-surface);
    border: 1px solid var(--color-outline);
    border-radius: 12px;
  }

  /* Tablet: 2 cols, less gap */
  @media (max-width: 64rem) {
    .feature-grid { grid-template-columns: repeat(2, 1fr); gap: var(--space-5); }
  }
  /* Mobile: 1 col, tightest gap */
  @media (max-width: 48rem) {
    .feature-grid { grid-template-columns: 1fr; gap: var(--space-4); }
  }
</style>
```

Reading the rhythm: 64 (section top) → 24 (heading-to-grid) → 32 (card-to-card) → 24 (intra-card). Each step is on the named scale, each step is monotonic-or-equal as you zoom in.

## Component example B — form field stack

A login form with field stack + button rhythm:

```html
<form class="login-form">
  <div class="field">
    <label for="email">Email</label>
    <input id="email" type="email" required />
  </div>

  <div class="field">
    <label for="password">Password</label>
    <input id="password" type="password" required />
  </div>

  <button type="submit" class="submit">Sign in</button>
</form>

<style>
  .login-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);                  /* 16 — field-to-field */
    max-width: 24rem;
    padding: var(--space-6);              /* 32 — form padding */
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);                  /* 8 — label-to-input (intra-component) */
  }

  .field label {
    font-size: 0.875rem;
  }

  .field input {
    padding-block: var(--space-3);        /* 12 — field internal vertical */
    padding-inline: var(--space-4);       /* 16 — field internal horizontal */
    border: 1px solid var(--color-outline);
    border-radius: 8px;
  }

  .submit {
    padding-block: var(--space-3);        /* 12 — same vertical as fields for vertical-alignment */
    padding-inline: var(--space-5);       /* 24 — wider horizontal for button (Fitts) */
    margin-block-start: var(--space-2);   /* 8 — tighter than field-to-field, signals "I'm grouped with the form" */
    background: var(--color-primary);
    color: var(--color-on-primary);
    border-radius: 8px;
  }
</style>
```

Vertical rhythm: 32 (form padding) → 16 (field-to-field) → 8 (label-to-input intra-field) → 12 (field internal vertical) → 8 (button extra margin). Every value is a named step. The horizontal token (24) on the button is one step larger than its vertical (12) — buttons read better wider than tall.

## Cross-references

- `skills/amw-design-md/SKILL.md` — DESIGN.md spacing block declares this 10-step scale; the linter at `bin/amw-design-md-lint.sh` checks scale presence + step values.
- `skills/amw-design-system-presets/SKILL.md` — every preset ships the same 10-step scale (the values are universal — only the density mode varies); see `TECH-token-system-density-modes.md` for how the compact/comfortable/spacious modes multiply the scale.
- `TECH-token-system-density-modes.md` — density-mode multiplier table (the spacing scale here is the "comfortable" baseline; compact = ×0.75, spacious = ×1.25).
- `TECH-token-system-color-roles.md` — the color roles that paint surfaces sized by this spacing.
- `TECH-landing-anatomy.md` — section-rhythm budget per landing-page archetype; uses `--space-7` to `--space-10` for between-section gaps.
- `TECH-css-variable-discipline.md` — colors must come from tokens; spacing from this scale follows the same discipline.
- `bin/amw-design-md-validate.py` — checks all 10 steps are declared and resolve to multiples of `--space-unit`.
- `agents/amw-wireframe-builder-agent.md` — Phase B HTML emission must use only `var(--space-N)` for spacing.
- `agents/amw-component-library-architect-agent.md` — authors the token block; defines density-mode multipliers.
