# TECH — Motion easing catalog (Material 3 named curves)

> **Source attribution:** Adapted from Google's Material Design 3 motion guidelines (Apache-2.0). Original at https://m3.material.io/styles/motion/easing-and-duration/. Direct-port of the six named easing curves; non-MD3 vendors map onto the same role taxonomy below.

Covers T-107 in the batch9 master ledger. A complete catalog of six named easing curves (the four "standard" + two "emphasized" tiers), their `cubic-bezier()` values, and the role each curve is reserved for. Existing `TECH-motion-budgets.md` defines four shorter aliases (`--ease-out`, `--ease-in-out`, `--ease-spring`, `--ease-snap`); this file extends that with the full MD3 system used by `amw-motion-designer-agent` for production-grade page transitions, drawer reveals, and emphasized state changes.

## Token block

```css
:root {
  /* --- Standard tier — for routine on-screen motion --- */
  --ease-standard:             cubic-bezier(0.20, 0.00, 0.00, 1.00);
  --ease-standard-decelerate:  cubic-bezier(0.00, 0.00, 0.00, 1.00);
  --ease-standard-accelerate:  cubic-bezier(0.30, 0.00, 1.00, 1.00);

  /* --- Emphasized tier — for "this matters" motion, e.g. drawer open --- */
  --ease-emphasized:            cubic-bezier(0.20, 0.00, 0.00, 1.00);
  --ease-emphasized-decelerate: cubic-bezier(0.05, 0.70, 0.10, 1.00);
  --ease-emphasized-accelerate: cubic-bezier(0.30, 0.00, 0.80, 0.15);

  /* --- Linear — only for ambient loops, never for entrance/exit --- */
  --ease-linear: linear;
}
```

The two emphasized end-tiers (`emphasized-decelerate` and `emphasized-accelerate`) carry stronger curvature than the standard tier — the user perceives the start (or end) of the motion as more authoritative. Reserve them for moments where attention must follow the motion (e.g. modal entrance, primary-CTA dispatch). Overuse drains the emphasis; if every motion is emphasized, none are.

## Role mapping (the contract)

| Role from `TECH-motion-taxonomy.md` | Easing token | Why |
|---|---|---|
| **entry — above-the-fold** | `--ease-emphasized-decelerate` | Hero content lands authoritatively; the user must notice it |
| **entry — below-the-fold** | `--ease-standard-decelerate` | Quieter; scroll-triggered, supportive of reading flow |
| **exit — routine** | `--ease-standard-accelerate` | Leaves quickly without ceremony |
| **exit — emphasized** (drawer close, modal dismiss) | `--ease-emphasized-accelerate` | Exit is decisive; user wired to expect symmetry with the emphasized entrance |
| **hover** | `--ease-standard` | Symmetric in/out so the user's pointer feels in control |
| **focus** | `--ease-standard` | Match hover so motion language stays consistent |
| **interaction** (button press, toggle) | `--ease-standard` | Symmetric — press and release should mirror |
| **page-transition** | `--ease-emphasized` (in) + `--ease-emphasized-accelerate` (out) | Split-curve: enter authoritatively, exit decisively |
| **ambient** | `--ease-linear` (or `--ease-in-out` at 30s+ duration) | Loop must not draw the eye; deceleration peaks would |

## Per-curve detail

### `--ease-standard` — `cubic-bezier(0.20, 0.00, 0.00, 1.00)`

The default. Symmetric S-curve, slight ease at both ends. Use when the user expects neither acceleration nor deceleration to dominate. Hover, focus, interaction.

### `--ease-standard-decelerate` — `cubic-bezier(0.00, 0.00, 0.00, 1.00)`

Pure deceleration — starts at velocity, ends at rest. The brain reads "this object is settling into place." Use for entrance roles below the fold, where the motion must feel arrival-like.

### `--ease-standard-accelerate` — `cubic-bezier(0.30, 0.00, 1.00, 1.00)`

Pure acceleration — starts at rest, ends at velocity. The brain reads "this object is leaving." Use for exit roles. Pairs with `--ease-standard-decelerate` for matched in/out language.

### `--ease-emphasized` — `cubic-bezier(0.20, 0.00, 0.00, 1.00)`

Same bezier coordinates as `--ease-standard` but reserved for emphasized contexts so semantic meaning is preserved. In practice, you'll mostly reach for `--ease-emphasized-decelerate` and `--ease-emphasized-accelerate` instead — the symmetric variant is for cases where the motion stays on-screen continuously (e.g. a panel pinned to the side as it morphs width).

### `--ease-emphasized-decelerate` — `cubic-bezier(0.05, 0.70, 0.10, 1.00)`

Stronger deceleration than the standard tier — the curve sweeps in then settles dramatically at the end. Use for hero entrance, primary modal reveal, "wow" moments. Cap to one per viewport.

### `--ease-emphasized-accelerate` — `cubic-bezier(0.30, 0.00, 0.80, 0.15)`

Stronger acceleration than the standard tier — slow start, then disappears fast. Use for emphasized exits where dismissal must feel definitive (modal dismiss with backdrop fade, large drawer close).

## Aliases vs the MD3 catalog

This file's 6 emphasized + standard curves are the authoritative names. The four shorter aliases defined in `TECH-motion-budgets.md` (`--ease-out`, `--ease-in-out`, `--ease-spring`, `--ease-snap`) coexist; they map as:

| Alias | Equivalent in this catalog | Notes |
|---|---|---|
| `--ease-out` | `--ease-standard-decelerate` (looser variant) | The shorter alias's `cubic-bezier(0.23, 1, 0.32, 1)` is slightly different but visually indistinguishable below 400 ms |
| `--ease-in-out` | `--ease-standard` | Direct alias |
| `--ease-spring` | n/a — spring physics, not bezier | See `TECH-spring-physics.md` for the spring tier |
| `--ease-snap` | `--ease-standard-accelerate` (steeper variant) | Reserve `--ease-snap` for interaction-role microcurves where overshoot is undesirable |

Both naming systems remain valid. Prefer the MD3 names (`--ease-emphasized-*`) when emitting design-token JSON for Style Dictionary or Figma Tokens — those tools and downstream consumers already understand MD3 semantics.

## Code samples

### Before — generic easing (bad)

```css
.modal {
  transition: transform 300ms ease, opacity 300ms ease;
}
.modal.open {
  transform: scale(1) translateY(0);
  opacity: 1;
}
```

Problems: `ease` is the browser default cubic-bezier(0.25, 0.1, 0.25, 1.0) — feels generic; no distinction between modal entrance (emphasized) and a routine hover; transition duration is fixed regardless of role.

### After — named curves with role mapping (good)

```css
.modal {
  /* Hidden state */
  transform: scale(0.96) translateY(8px);
  opacity: 0;
  transition:
    transform var(--motion-duration-medium) var(--ease-emphasized-accelerate),
    opacity   var(--motion-duration-medium) var(--ease-emphasized-accelerate);
}
.modal.open {
  /* Visible state — entrance uses decelerate */
  transform: scale(1) translateY(0);
  opacity: 1;
  transition:
    transform var(--motion-duration-medium) var(--ease-emphasized-decelerate),
    opacity   var(--motion-duration-medium) var(--ease-emphasized-decelerate);
}
@media (prefers-reduced-motion: reduce) {
  .modal { transition: opacity var(--motion-duration-fast) linear; }
}
```

Why: entrance uses `--ease-emphasized-decelerate` (the modal settles into place with authority). Exit uses `--ease-emphasized-accelerate` (modal leaves quickly). The split-curve language is the MD3 default for emphasized motion. Reduced-motion strips the transform and keeps a short opacity-only fade.

### Web Animations API equivalent

```js
const card = document.querySelector('.card');
card.animate(
  [
    { transform: 'translateY(24px)', opacity: 0 },
    { transform: 'translateY(0)',    opacity: 1 }
  ],
  {
    duration: 300,
    easing: 'cubic-bezier(0.05, 0.70, 0.10, 1.00)', // --ease-emphasized-decelerate
    fill: 'both'
  }
);
```

## Breaks if

- An author uses `transition: all 0.3s ease` — the `ease` keyword resolves to a generic curve that is neither in this catalog nor in the role mapping. `bin/amw-ai-slop-check.py` flags this on every Phase B HTML emission.
- An author uses `--ease-emphasized-*` on more than one viewport-prominent element simultaneously — the emphasis loses meaning. The motion-designer agent caps emphasized curves to one above-the-fold entrance + one drawer/modal at a time.
- `--ease-linear` (or the keyword `linear`) appears on an entrance or exit role — robotic, banned for non-ambient motion.
- The motion-designer agent invents new bezier values outside this catalog without explicit user request. Custom curves are reserved for branded `--ease-brand-*` tokens (see `TECH-brand-voltage.md`).

## See also

- `TECH-motion-taxonomy.md` — the 7 roles each easing maps onto
- `TECH-motion-budgets.md` — duration bands per role; the 4 shorter aliases
- `TECH-motion-duration-budgets.md` — perceptual duration tiers
- `TECH-motion-orchestration.md` — how multiple curves compose across a sequence
- `TECH-spring-physics.md` — when to swap bezier easings for physics-based springs
- `TECH-reduced-motion.md` — easing under reduced-motion overrides
- MD3 source: https://m3.material.io/styles/motion/easing-and-duration/
