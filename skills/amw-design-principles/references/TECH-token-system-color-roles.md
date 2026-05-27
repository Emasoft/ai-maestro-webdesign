<!--
Sources: Material 3 color roles (Apache-2.0, https://m3.material.io/styles/color/roles) — direct-port of role names + on-* pairing semantics; Radix Colors 12-step scale (MIT) — direct-port of step semantics; WCAG 2.1 §1.4.3 §1.4.11 contrast ratios — public spec.
Synthesis novel to this plugin: brand-voltage tie-in, plugin-token-prefix convention, breaks-if invariants. Clean-room beyond the cited sources.
-->

---
name: TECH-token-system-color-roles
category: design-principles-tokens
source: Material 3 + Radix Colors direct-port (roles, on-* pairs); WCAG 2.1 pair-contrast invariants; clean-room synthesis for plugin conventions (batch9 Wave 2 Round 3, T-074/T-075)
license: this file = MIT (plugin license); Material 3 source is Apache-2.0 with attribution preserved in the HTML-comment header above; Radix is MIT
also-in: TECH-brand-voltage.md (the one accent hue feeds `primary`); TECH-named-color-shadow-techniques.md (near-black floor on `surface-dark-*`); TECH-css-variable-discipline.md (raw Tailwind color utilities banned — colors must be roles)
---

# Token system — semantic color roles and pair-contrast invariants

## Table of Contents

- [What this is](#what-this-is)
- [The 14 mandatory color roles](#the-14-mandatory-color-roles)
- [The on-* pair invariants (WCAG-AA gate)](#the-on--pair-invariants-wcag-aa-gate)
- [Token block — canonical declaration](#token-block--canonical-declaration)
- [Breaks if](#breaks-if)
- [Component example A — pricing card](#component-example-a--pricing-card)
- [Component example B — toast/alert stack](#component-example-b--toaststack-alert)
- [Cross-references](#cross-references)

## What this is

Every artifact the plugin emits resolves its colors through a fixed set of **semantic roles** (`primary`, `surface`, `error`, etc.), not through raw palette steps. Each foreground role is **paired** with the matching background role through an `on-*` token whose value is pre-validated for WCAG 2.1 AA contrast against its pair. That pairing is the difference between a theme that survives a brand swap and a theme that breaks on the first re-skin.

This file gives the role list, the on-* pairing rule, the canonical CSS token block, and the breaks-if invariants the wireframe builder and the design-md auditor both check.

## The 14 mandatory color roles

A DESIGN.md token block MUST declare these 14 roles. Any extra roles are permitted; any missing role fails the lint.

| Role token | Job | Notes |
|---|---|---|
| `--color-primary` | The single brand chromatic accent | Saturation > 50% (see brand-voltage); only one chromatic accent per brand |
| `--color-on-primary` | Foreground that sits on `--color-primary` (button label, CTA text) | Paired-contrast ≥ 4.5:1 against `--color-primary` |
| `--color-primary-container` | Tinted-low surface using the primary hue (selected-row, active-tab background) | Same hue as primary, lightness shifted toward surface |
| `--color-on-primary-container` | Foreground on primary-container | Paired-contrast ≥ 4.5:1 against `--color-primary-container` |
| `--color-secondary` | Restrained secondary action (outline button, link) | NOT a second chromatic accent — usually a desaturated tint of primary or a neutral with primary-hue temperature |
| `--color-on-secondary` | Foreground on `--color-secondary` | Paired-contrast ≥ 4.5:1 |
| `--color-tertiary` | Optional third role (rare — only for systems that legitimately need a third semantic family, e.g. complementary metric in a dashboard) | If unused, omit — do NOT fill with a random hue |
| `--color-on-tertiary` | Foreground on `--color-tertiary` | Paired-contrast ≥ 4.5:1 |
| `--color-background` | The page-canvas color (body background) | The lowest surface in the elevation stack |
| `--color-on-background` | Default body text on `--color-background` | Paired-contrast ≥ 7:1 (body text needs AAA) |
| `--color-surface` | Card / panel / sheet background (one step above page) | Slightly different from background; see "1-tier surface" rule below |
| `--color-on-surface` | Default text on `--color-surface` | Paired-contrast ≥ 7:1 |
| `--color-surface-variant` | Subdued surface (input field background, secondary panel) | Less prominent than surface |
| `--color-on-surface-variant` | Foreground on `--color-surface-variant`, also the "muted text" role | Paired-contrast ≥ 4.5:1 (muted text is not body text, so AA is acceptable) |
| `--color-error` | Destructive / error state hue (delete button, invalid input border, error toast background) | Independent of brand voltage — semantic colors are not "accents" |
| `--color-on-error` | Foreground on `--color-error` | Paired-contrast ≥ 4.5:1 |
| `--color-outline` | Border / hairline / divider role | Paired-contrast ≥ 3:1 against the surface it borders (WCAG 2.1 §1.4.11 non-text contrast) |
| `--color-outline-variant` | Decorative low-contrast border (rare — for subdivisions inside a card, not for primary borders) | No contrast floor — explicitly decorative |

**Status colors (warning / success / info) are NOT in the mandatory 14.** They're optional roles (`--color-warning`, `--color-success`, `--color-info`) with their own `on-*` pairs. Declare them only if the product needs the affordance. A dashboard with status badges needs them; a marketing landing page rarely does. Padding a token block with unused status colors is slop.

## The on-* pair invariants (WCAG-AA gate)

Each `--color-on-X` token MUST satisfy contrast against the matching `--color-X`. The plugin gates this mechanically through `bin/amw-design-md-contrast.py`.

| Pair | Required contrast | Why |
|---|---|---|
| `--color-on-primary` / `--color-primary` | ≥ 4.5:1 | Buttons / CTAs carry interactive text; AA-large is not enough since CTA labels are typically 14–16px |
| `--color-on-primary-container` / `--color-primary-container` | ≥ 4.5:1 | Selected-row text, active-tab text |
| `--color-on-secondary` / `--color-secondary` | ≥ 4.5:1 | Outline-button text |
| `--color-on-tertiary` / `--color-tertiary` | ≥ 4.5:1 | If declared |
| `--color-on-background` / `--color-background` | ≥ 7:1 | Body copy is the AAA case; this is the longest-read text |
| `--color-on-surface` / `--color-surface` | ≥ 7:1 | Card body copy is also AAA |
| `--color-on-surface-variant` / `--color-surface-variant` | ≥ 4.5:1 | Muted/secondary text — AA acceptable |
| `--color-on-error` / `--color-error` | ≥ 4.5:1 | Error-toast text, delete-button label |
| `--color-outline` / `--color-surface` | ≥ 3:1 | Non-text contrast (WCAG §1.4.11) — borders must remain visible |
| `--color-outline` / `--color-background` | ≥ 3:1 | Hairlines between sections |

**No mixing across the pair.** `--color-on-primary` paints text on `--color-primary`, full stop. It does NOT also paint text on `--color-surface`. A foreground used in two contexts needs two roles; reusing one risks one of the two pairs failing AA.

**Themes preserve invariants.** When a `[data-theme="dark"]` override redefines `--color-primary`, it MUST also redefine `--color-on-primary` such that the new pair still passes ≥ 4.5:1. The auditor runs the contrast gate per theme, not once globally.

## Token block — canonical declaration

This block is the literal template `amw-design-md-emit-companions.py` emits and the lint checks. Light theme is `:root`; the dark override lives in `[data-theme="dark"]`. Values shown are placeholders — the brand researcher / design-md author fills them.

```css
:root {
  /* Brand primary (the single chromatic accent) */
  --color-primary:                  #2d4a7c;
  --color-on-primary:               #faf7f2;
  --color-primary-container:        #e0e8f2;
  --color-on-primary-container:     #14233d;

  /* Secondary (restrained — usually a tinted neutral, NOT a second chromatic) */
  --color-secondary:                #5c6470;
  --color-on-secondary:             #faf7f2;

  /* Surfaces (page + 1 tier above) */
  --color-background:               #faf7f2;
  --color-on-background:            #1a1a1d;
  --color-surface:                  #ffffff;
  --color-on-surface:               #1a1a1d;
  --color-surface-variant:          #f0ebe1;
  --color-on-surface-variant:       #5c6470;

  /* Semantic */
  --color-error:                    #ba1a1a;
  --color-on-error:                 #ffffff;

  /* Hairlines (non-text contrast ≥ 3:1) */
  --color-outline:                  #c7c3bb;
  --color-outline-variant:          #e6e1d8;
}

[data-theme="dark"] {
  --color-primary:                  #87a3d6;
  --color-on-primary:               #14233d;
  --color-primary-container:        #2c4368;
  --color-on-primary-container:     #d3def0;

  --color-secondary:                #b0b5bd;
  --color-on-secondary:             #2a2d33;

  --color-background:               #1a1c20;
  --color-on-background:            #e5e5ea;
  --color-surface:                  #23262b;
  --color-on-surface:               #e5e5ea;
  --color-surface-variant:          #2c3035;
  --color-on-surface-variant:       #a0a4ac;

  --color-error:                    #ffb4ab;
  --color-on-error:                 #690005;

  --color-outline:                  #4a4e54;
  --color-outline-variant:          #353a40;
}
```

Tertiary roles (`--color-tertiary`, `--color-on-tertiary`) are absent here because most products do not need a third semantic family. Add them only when there is a real third role to fill (e.g., a complementary metric series in a dashboard chart); leaving them undeclared is correct minimalism, not omission.

## Breaks if

The wireframe builder and the design-md auditor reject the token block when any of the following holds:

- Any of the 14 mandatory roles is missing.
- Any on-* pair fails its contrast floor (≥ 4.5:1 default, ≥ 7:1 for body text, ≥ 3:1 for outlines).
- The hue of `--color-primary` is the same as `--color-error` within ΔH < 30° — the brand accent and the destructive color collide.
- Two roles point at the same hex value (token reuse — the `on-*` pair needs distinct values).
- A theme override redefines `--color-primary` without redefining `--color-on-primary` (orphaned override).
- The dark theme `--color-on-background` is `#ffffff` (violates near-black/near-white rule from `TECH-named-color-shadow-techniques.md` — pure white on dark is harsh; use `#e5e5ea`/`#fafafa` instead).
- A second chromatic accent (saturation > 50%) appears under any non-primary role — secondary/tertiary/surface variants must stay neutral or low-saturation (see brand-voltage).
- Status colors (warning/success/info) are declared but their pairs are not — incomplete role families are worse than absent ones.

## Component example A — pricing card

Three-tier pricing with one "most popular" tier elevated. Token-only colors:

```html
<article class="pricing-card pricing-card--highlight">
  <h3 style="color: var(--color-on-primary-container);">Pro</h3>
  <p class="badge"
     style="background: var(--color-primary); color: var(--color-on-primary);">
    Most popular
  </p>
  <p class="price" style="color: var(--color-on-primary-container);">$24/mo</p>
  <button class="cta"
          style="background: var(--color-primary); color: var(--color-on-primary);">
    Start free trial
  </button>
</article>

<style>
  .pricing-card {
    background: var(--color-surface);
    color: var(--color-on-surface);
    border: 1px solid var(--color-outline);
  }
  .pricing-card--highlight {
    background: var(--color-primary-container);
    color: var(--color-on-primary-container);
    border: 1px solid var(--color-primary);
  }
</style>
```

Two background roles in one card (`primary-container` body + `primary` for the badge + CTA), each with its matching `on-*` foreground. Every text-on-background pair passes ≥ 4.5:1 by construction because the token block validated it.

## Component example B — toast / alert stack

Three toast variants — info, success, error — each using its semantic role pair plus the outline role for the hairline. No raw hex anywhere:

```html
<div class="toast toast--error" role="alert">
  <strong style="color: var(--color-on-error);">Sync failed.</strong>
  <span style="color: var(--color-on-error);">Retrying in 5s…</span>
  <button class="dismiss"
          style="background: transparent; color: var(--color-on-error); border: 1px solid var(--color-on-error);">
    Dismiss
  </button>
</div>

<style>
  .toast {
    background: var(--color-surface);
    color: var(--color-on-surface);
    border-left: 4px solid var(--color-outline);
  }
  .toast--error {
    background: var(--color-error);
    color: var(--color-on-error);
    border-left-color: var(--color-on-error);
  }
</style>
```

The `--error` variant flips the background to `--color-error` and the foreground to `--color-on-error`; the dismiss button reuses the same `on-error` for its text + border — both reads pass AA against the error background by the pair invariant.

## Cross-references

- `skills/amw-design-md/SKILL.md` — DESIGN.md frontmatter declares these 14 roles as the canonical token contract; the linter at `bin/amw-design-md-lint.sh` checks role completeness.
- `skills/amw-design-system-presets/SKILL.md` — each preset (linear / vercel / stripe / etc.) ships a full token block conformant to the 14-role contract; switching presets re-assigns the role values, not the role names.
- `TECH-brand-voltage.md` — the one chromatic accent that becomes `--color-primary`; all other roles stay neutral or low-saturation by the voltage rule.
- `TECH-named-color-shadow-techniques.md` — near-black floor (`min(R,G,B) ≥ 0x18`) applies to `--color-background` and `--color-surface` when dark; pure `#000` is forbidden.
- `TECH-css-variable-discipline.md` — raw Tailwind color utilities (`bg-blue-500`) are banned; markup uses `var(--color-*)` exclusively.
- `bin/amw-design-md-contrast.py` — mechanical AA gate over every `on-*` pair.
- `bin/amw-design-md-validate.py` — checks all 14 mandatory roles present.
- `agents/amw-component-library-architect-agent.md` — authors the token block; runs the contrast gate before delivery.
- `agents/amw-wireframe-builder-agent.md` — consumes the token block when emitting HTML; rejects raw hex literals.
