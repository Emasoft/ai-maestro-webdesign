<!--
Sources: Material 3 elevation scale (Apache-2.0, https://m3.material.io/styles/elevation/tokens) — direct-port of the 0/1/2/3/4/5-dp tiers; Tailwind v4 shadow scale (MIT) — direct-port of step counts + role mapping; Bootstrap z-index layer table (MIT) — direct-port of layer assignments.
Synthesis novel to this plugin: colored-shadow integration with TECH-named-color-shadow-techniques.md, radius-to-role mapping for chip/button/card/sheet, breaks-if invariants. Clean-room beyond the cited sources.
-->

---
name: TECH-token-system-elevation-and-radius
category: design-principles-tokens
source: Material 3 elevation + Tailwind shadow + Bootstrap z-index direct-port (batch9 Wave 2 Round 3, T-079/T-080/T-081)
license: this file = MIT (plugin license); Material 3 is Apache-2.0, Tailwind + Bootstrap are MIT — attribution preserved in the HTML-comment header above
also-in: TECH-named-color-shadow-techniques.md (colored shadow rule applies to every elevation tier — never raw black); TECH-material-language.md (1-2 material-moment budget caps how many elevated cards a page may have); TECH-css-variable-discipline.md (raw `shadow-lg` / `rounded-2xl` Tailwind utilities are NOT in the discipline gate but their values must derive from tokens)
---

# Token system — z-index layers, elevation shadows, radius scale

## Table of Contents

- [What this is](#what-this-is)
- [The z-index layer table](#the-z-index-layer-table)
- [The 7-tier elevation/shadow scale](#the-7-tier-elevationshadow-scale)
- [The 7-step radius scale + role mapping](#the-7-step-radius-scale--role-mapping)
- [Token block — canonical declaration](#token-block--canonical-declaration)
- [Breaks if](#breaks-if)
- [Component example A — modal stack with backdrop](#component-example-a--modal-stack-with-backdrop)
- [Component example B — card with hover lift](#component-example-b--card-with-hover-lift)
- [Cross-references](#cross-references)

## What this is

Three depth-related token families live together because they're always specified together:
1. **z-index layers** — which element sits on top of which (no random `z-index: 9999`).
2. **Elevation shadows** — a 7-tier scale from flat to deeply elevated.
3. **Radius scale** — corner roundness, with role-mapped defaults for chip/button/card/sheet.

These three jointly answer the question "how does this element relate to the page in depth and form?". Without a token contract, agents (and humans) invent random `z-index: 999`, random box-shadow blur radii, and random border-radius values per component — and the page reads as a stack of stickers, not a coherent depth system.

## The z-index layer table

The plugin uses **8 named z-index layers**. Every `z-index` value in markup MUST be a `var(--z-*)` token. Raw integers (`z-index: 100`, `z-index: 9999`) are forbidden — they cause the layer-drift bug where each new component picks a slightly higher value until the stack ordering becomes nondeterministic.

| Layer token | Value | What sits here | Notes |
|---|---|---|---|
| `--z-base`         | 0     | Default flow; no stacking context | Everything that doesn't explicitly elevate |
| `--z-dropdown`     | 1000  | Select dropdowns, autocomplete menus, hover popovers | Above content; below sticky headers |
| `--z-sticky`       | 1100  | Sticky table headers, sticky sidebars | Above content; below the page-level chrome |
| `--z-banner`       | 1200  | Promo banner, system-status banner | Above sticky content; below modals + tooltips |
| `--z-overlay`      | 1300  | Modal backdrop, drawer scrim | Just below the modal it belongs to |
| `--z-modal`        | 1400  | Modal dialog, sheet, drawer body | Above the overlay |
| `--z-popover`      | 1500  | Floating popovers (NOT bound to a parent like dropdowns); date pickers | Above modals when triggered from inside one |
| `--z-tooltip`      | 1600  | Tooltip — the topmost UI layer | Highest; tooltips win over everything else |

The integer values are spaced by 100 so future inserts don't require renumbering. Order matters: dropdown < sticky < banner < overlay < modal < popover < tooltip is the canonical stack. Reversing any pair breaks expected UI behavior (e.g., if a tooltip can be obscured by a modal, the user can't see the tooltip explaining the modal field).

**Two hard rules.**

1. Never use `z-index: 9999` or any other "I want to be on top" magic number. If the existing layers don't cover the case, the case is wrong — re-evaluate why a new layer is needed.
2. Negative z-index is allowed ONLY for decorative background SVG glyphs that must sit visually behind page content but in the same stacking context. Tokenize this as `--z-behind: -1`; do NOT use `-100` or random negatives.

## The 7-tier elevation/shadow scale

Material 3 names these "elevation levels"; this plugin names them by the **dp tier they correspond to** (0 / 1 / 2 / 4 / 8 / 16 / 24) but the values themselves are pixel-rendered CSS shadows. The dp naming is preserved for cross-team communication; the actual rendered offsets/blurs are what matter.

| Elevation token | dp tier | Used for | Default CSS shadow (light theme) |
|---|---|---|---|
| `--elevation-0`  | 0  | Flat — no shadow; on-surface text, default body | `none` |
| `--elevation-1`  | 1  | Hairline lift — chip on hover, slight raise | `0 1px 2px rgba(15,23,42,0.06)` |
| `--elevation-2`  | 2  | Default card / panel rest | `0 1px 2px rgba(15,23,42,0.06), 0 1px 3px rgba(15,23,42,0.10)` |
| `--elevation-3`  | 4  | Card hover, button raised state | `0 2px 4px rgba(15,23,42,0.06), 0 4px 6px rgba(15,23,42,0.10)` |
| `--elevation-4`  | 8  | Floating action button, popover | `0 4px 6px rgba(15,23,42,0.05), 0 10px 15px rgba(15,23,42,0.10)` |
| `--elevation-5`  | 16 | Modal dialog, drawer, sheet | `0 10px 15px rgba(15,23,42,0.05), 0 20px 25px rgba(15,23,42,0.12)` |
| `--elevation-6`  | 24 | Dropdown menu (above modal), large floating panel | `0 20px 25px rgba(15,23,42,0.06), 0 25px 50px rgba(15,23,42,0.15)` |

**The colored-shadow rule applies to every tier.** When the elevated element has a chromatic surface (a blue card, a violet button), the `rgba(15,23,42, …)` values above are replaced by the surface's own hue darkened ~35% and desaturated ~20% — see `TECH-named-color-shadow-techniques.md` for the construction. Neutral elements (white cards on white pages) keep the slate-tinted defaults above.

**The dark-theme override.** Shadows in dark themes get *brighter* alpha (since the canvas is dark, a darker shadow disappears). A dark-theme override on `--elevation-2` typically goes to `rgba(0,0,0,0.30)` floor — but again, only for neutral surfaces. Chromatic surfaces in dark themes use the inverse colored-shadow rule (shadow hue = surface hue, lightness shifted toward background).

**Hard cap.** A page may use at most **3 distinct elevation tiers simultaneously** (e.g., `elevation-0` body + `elevation-2` cards + `elevation-5` modal when open). Using all 7 tiers on one page produces a depth soup — every component competes for "I'm important." When in doubt, prefer fewer tiers and use color/border to differentiate instead.

**No mixing colored + neutral shadows on the same page.** A card with a blue-tinted shadow next to a card with a slate-tinted shadow reads as two different design systems. Pick one shadow model per page.

## The 7-step radius scale + role mapping

A 7-step scale covers everything from "sharp" to "pill." Each step has a default role; deviations are allowed but rare.

| Radius token | Value (px) | Default role |
|---|---|---|
| `--radius-0`   | 0        | Hairline dividers; flush-to-edge banner bars; tables |
| `--radius-1`   | 4        | Inputs, text fields, small chips, badges |
| `--radius-2`   | 8        | Buttons, default chips, small cards |
| `--radius-3`   | 12       | Default cards, panels, popovers |
| `--radius-4`   | 16       | Modal dialogs, sheets, drawers |
| `--radius-5`   | 24       | Hero cards, large feature blocks |
| `--radius-pill` | 9999     | Pills (rounded-full): tags, avatars, fully-rounded CTAs |

**Role-mapping defaults (used unless the brand explicitly overrides):**

| Component | Default radius token |
|---|---|
| Input field | `--radius-1` |
| Badge / tag | `--radius-1` or `--radius-pill` (depending on brand voice) |
| Button | `--radius-2` |
| Small card (preview card, list item) | `--radius-2` |
| Default card (feature card, pricing card) | `--radius-3` |
| Modal dialog | `--radius-4` |
| Drawer / sheet | `--radius-4` on the top edge only; flush to viewport on the other edges |
| Hero / feature block (large) | `--radius-5` |
| Avatar | `--radius-pill` |
| Fully-rounded CTA ("Get started →" in a pill) | `--radius-pill` |

**Cross-role consistency rule.** A button with `--radius-2` inside a card with `--radius-3` reads correctly: the smaller element gets the smaller radius. **Inverting** the relationship (large component with smaller radius than its children) reads as broken nesting. If your card uses `--radius-3` (12), every button or chip inside it MUST use `--radius-2` (8) or `--radius-1` (4) — never `--radius-4` (16).

**Sharp vs soft brand voice.** A brand-voice override may shift the entire scale:
- **Sharp** (Linear, Stripe modern): default to `--radius-1` for inputs, `--radius-2` for buttons, `--radius-3` for cards. Avoid `--radius-4` and `--radius-5` except for modals.
- **Soft / friendly** (Notion, consumer apps): default to `--radius-2` for inputs, `--radius-3` for buttons (NOT 2), `--radius-4` for cards. Pills are fine.
- **Brutalist** (Hardcover, editorial): default to `--radius-0` everywhere except modals. Sharp corners are the brand voice.

The shift moves every default by one step; it does NOT invent new radius values. The 7-step scale is universal.

## Token block — canonical declaration

```css
:root {
  /* z-index layers */
  --z-behind:   -1;
  --z-base:     0;
  --z-dropdown: 1000;
  --z-sticky:   1100;
  --z-banner:   1200;
  --z-overlay:  1300;
  --z-modal:    1400;
  --z-popover:  1500;
  --z-tooltip:  1600;

  /* Elevation shadows (light theme, neutral surfaces) */
  --elevation-0: none;
  --elevation-1: 0 1px 2px rgba(15,23,42,0.06);
  --elevation-2: 0 1px 2px rgba(15,23,42,0.06), 0 1px 3px rgba(15,23,42,0.10);
  --elevation-3: 0 2px 4px rgba(15,23,42,0.06), 0 4px 6px rgba(15,23,42,0.10);
  --elevation-4: 0 4px 6px rgba(15,23,42,0.05), 0 10px 15px rgba(15,23,42,0.10);
  --elevation-5: 0 10px 15px rgba(15,23,42,0.05), 0 20px 25px rgba(15,23,42,0.12);
  --elevation-6: 0 20px 25px rgba(15,23,42,0.06), 0 25px 50px rgba(15,23,42,0.15);

  /* Radius scale */
  --radius-0:    0;
  --radius-1:    4px;
  --radius-2:    8px;
  --radius-3:    12px;
  --radius-4:    16px;
  --radius-5:    24px;
  --radius-pill: 9999px;
}

[data-theme="dark"] {
  /* Darker canvas needs higher-alpha shadows to remain visible */
  --elevation-1: 0 1px 2px rgba(0,0,0,0.30);
  --elevation-2: 0 1px 2px rgba(0,0,0,0.30), 0 1px 3px rgba(0,0,0,0.35);
  --elevation-3: 0 2px 4px rgba(0,0,0,0.30), 0 4px 6px rgba(0,0,0,0.40);
  --elevation-4: 0 4px 6px rgba(0,0,0,0.30), 0 10px 15px rgba(0,0,0,0.45);
  --elevation-5: 0 10px 15px rgba(0,0,0,0.30), 0 20px 25px rgba(0,0,0,0.55);
  --elevation-6: 0 20px 25px rgba(0,0,0,0.30), 0 25px 50px rgba(0,0,0,0.60);
}
```

Chromatic-surface elevations are computed per-element from the surface's own hue (see `TECH-named-color-shadow-techniques.md`). The block above is the neutral fallback only.

## Breaks if

The auditor and wireframe builder reject the elevation/radius/z-index block when any of the following holds:

- A markup or `<style>` uses `z-index: <integer>` instead of `var(--z-*)`.
- A markup or `<style>` uses `z-index: 9999` or any value above `1600` (the tooltip ceiling).
- A page uses more than 3 distinct elevation tiers simultaneously visible on screen.
- A page mixes colored shadows (`rgba(<hue>, …)`) with slate-neutral shadows (`rgba(15,23,42, …)`) on chromatic surfaces — pick one shadow model.
- A chromatic surface (card with `background: var(--color-primary)`) uses the neutral shadow values above instead of a hue-derived shadow.
- A modal's z-index is below its overlay's z-index (modal must sit above its scrim).
- A radius value is used that is NOT in the 7-step scale (e.g., `border-radius: 6px`, `border-radius: 14px`).
- An interior element's radius is larger than its container's radius (a button with `--radius-4` inside a card with `--radius-3` — looks broken).
- A pill (`--radius-pill`) is used on a rectangular element wider than 480 px — pills only work on small/medium-width components; on large rectangles, the corners look detached.
- Elevation skipping by ≥2 tiers in a hover transition (e.g., `--elevation-1` resting → `--elevation-4` on hover); the visual jump is too large. Hover transitions should move by 1 tier.
- Dark-theme shadows reuse the light-theme alpha values — they will be invisible.

## Component example A — modal stack with backdrop

A modal with backdrop, dialog, dropdown inside, and a tooltip pointing at the dropdown:

```html
<div class="modal-backdrop" style="z-index: var(--z-overlay);"></div>
<dialog class="modal" style="z-index: var(--z-modal);">
  <h2>Confirm action</h2>
  <select class="modal-select" style="z-index: var(--z-dropdown);">…</select>
  <span class="tooltip" style="z-index: var(--z-tooltip);">Select an option</span>
  <div class="modal-footer">
    <button class="confirm">Confirm</button>
  </div>
</dialog>

<style>
  .modal-backdrop {
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.40);
  }

  .modal {
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    background: var(--color-surface);
    color: var(--color-on-surface);
    padding: var(--space-6);
    border-radius: var(--radius-4);              /* 16 — modal tier */
    box-shadow: var(--elevation-5);
    max-width: 32rem;
  }

  .confirm {
    background: var(--color-primary);
    color: var(--color-on-primary);
    padding-block: var(--space-3);
    padding-inline: var(--space-5);
    border-radius: var(--radius-2);               /* 8 — button is one tier smaller than the modal */
    box-shadow: var(--elevation-1);
  }
</style>
```

Reading the depth: overlay (z 1300) < modal (z 1400) < dropdown inside modal (z 1500 via `--z-popover`-equivalent, but actually `--z-dropdown` since this dropdown is anchored to the modal's select — the rule is that ALL elements inside a modal that need to float adopt the layer-above their modal, so a dropdown inside a modal becomes effectively layer-popover by stacking-context, not by literal z-index). The tooltip remains the absolute topmost.

Reading the form: modal uses `--radius-4`, button inside uses `--radius-2` (one tier smaller). Modal uses `--elevation-5`; button at rest uses `--elevation-1`. On button hover, lift one tier to `--elevation-3` (skip `--elevation-2` is allowed because it's a hover transition matching the brand voice — the rule against ≥2-tier skips applies to RESTING-state designs, not hover deltas).

## Component example B — card with hover lift

A feature card that lifts on hover, with chromatic shadow:

```html
<article class="feature-card">
  <h3>Real-time sync</h3>
  <p>Changes propagate within 200 ms.</p>
</article>

<style>
  .feature-card {
    /* Chromatic surface — primary-container */
    background: var(--color-primary-container);
    color: var(--color-on-primary-container);

    padding: var(--space-5);
    border-radius: var(--radius-3);                /* 12 — default card tier */

    /* Colored shadow — hue = primary-container's hue, darkened ~35% */
    box-shadow:
      0 1px 2px rgba(30, 60, 110, 0.10),
      0 1px 3px rgba(30, 60, 110, 0.14);

    transition: transform 180ms ease, box-shadow 180ms ease;
  }

  .feature-card:hover {
    transform: translateY(-2px);                   /* physical lift */
    box-shadow:
      0 2px 4px rgba(30, 60, 110, 0.10),
      0 4px 6px rgba(30, 60, 110, 0.16);
  }
</style>
```

Reading the depth-change: rest = `--elevation-2`-equivalent (with colored shadow) → hover = `--elevation-3`-equivalent. One tier up, with translateY for the physical-press / lift feedback. The shadow values use the primary-container's hue darkened, NOT the slate-neutral defaults, because this card is chromatic — see `TECH-named-color-shadow-techniques.md` rule 1.

## Cross-references

- `skills/amw-design-md/SKILL.md` — DESIGN.md elevation/radius/z-index blocks declare these scales as the canonical token contract; the linter at `bin/amw-design-md-lint.sh` checks scale presence + value integrity.
- `skills/amw-design-system-presets/SKILL.md` — every preset ships its own brand-voice radius shift (sharp/soft/brutalist) over this universal 7-step scale.
- `TECH-token-system-color-roles.md` — surface roles (`--color-surface`, `--color-background`) define the canvas against which shadows are computed; the on-* contrast rule applies to elevated text too.
- `TECH-token-system-spacing-and-grid.md` — padding inside elevated cards uses the 10-step spacing scale.
- `TECH-token-system-density-modes.md` — density mode does NOT change radius or elevation values; only spacing scales by density.
- `TECH-named-color-shadow-techniques.md` — colored-shadow construction (hue/saturation/lightness derivation) for chromatic surfaces; the neutral defaults in this file apply only to grey-on-white.
- `TECH-material-language.md` — caps total material moments per page; elevation is one of the four primitives (Elevated card).
- `TECH-css-variable-discipline.md` — Tailwind `shadow-*` / `rounded-*` utilities are OK for geometry, but if used they must resolve to token-equivalent values.
- `bin/amw-design-md-validate.py` — checks all 7 elevation + 7 radius + 8 z-index tokens declared.
- `agents/amw-wireframe-builder-agent.md` — Phase B HTML emission must use `var(--z-*)`, `var(--elevation-*)`, `var(--radius-*)`; raw integer z-indexes are rejected.
- `agents/amw-component-library-architect-agent.md` — authors the token block; defines brand-voice radius shifts.
