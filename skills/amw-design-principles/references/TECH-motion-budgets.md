# Motion budgets — duration and easing per role

Every role in `TECH-motion-taxonomy.md` has a duration band and an easing curve. Going outside the band is allowed only with explicit justification recorded in the design doc; going outside the easing column produces motion that reads as "generic" or "robotic."

The duration tiers below are the canonical 5-band table (micro / state / entrance / page / luxurious) carried over from the `web-designer-plugin` Animation Playbook, extended with a per-role assignment.

## Per-role duration + easing matrix

| Role | Duration (min–max) | Default | Easing | Notes |
|---|---|---|---|---|
| **hover** | 80–150 ms | 120 ms | `--ease-out` | Must complete before the next pointer event lands |
| **focus** | 80–150 ms | 120 ms | `--ease-out` | Match hover so motion language stays consistent |
| **interaction** | 150–250 ms | 180 ms | `--ease-snap` | Quick start, smooth end — feels decisive |
| **exit** | 150–300 ms | 200 ms | `--ease-out` | Shorter than entry — leaving is decisive |
| **entry** | 200–400 ms | 300 ms | `--ease-out` | Above-the-fold ≤ 250 ms; below-the-fold up to 400 ms |
| **page-transition** | 300–700 ms | 500 ms | `--ease-in-out` or split (in/out) | Two half-curves: 200 ms exit + 300 ms enter |
| **ambient** | 2 000–30 000 ms | 8 000 ms | `--ease-in-out` linear-ish | Slow loop; must not draw the eye |

## The 4 canonical easing curves

```css
:root {
  /* Smooth deceleration — the default for entrances, hovers, focus */
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);

  /* Weighty, intentional — for page transitions */
  --ease-in-out: cubic-bezier(0.65, 0.01, 0.05, 0.99);

  /* Slight overshoot — for celebrations / playful interactions */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Quick start, smooth end — for UI state changes / interaction */
  --ease-snap: cubic-bezier(0.85, 0, 0.15, 1);
}
```

**Forbidden:** `transition: all 0.3s ease` (generic, lifeless), `transition: 0.3s linear` (robotic). Both are auto-flagged by `bin/amw-ai-slop-check.py`.

## The 3-tier CSS custom-property contract

Every plugin-generated artifact MUST emit these three duration tokens so downstream skills (wireframe-builder, infographic-builder, motion-designer) share a vocabulary:

```css
:root {
  --motion-duration-fast:   150ms;  /* Micro: hover, focus, interaction */
  --motion-duration-medium: 300ms;  /* Meso: entry, exit, state reveal */
  --motion-duration-slow:   500ms;  /* Macro: page-transition */
}
```

These are the **defaults** — actual durations within a role pick from the band in the table above. The token names match Material Design 3 conventions so projects already on MD3 inherit cleanly.

## The 5-tier duration reference (canonical 16-step table)

Used when motion is being authored at the design-token layer (e.g. component-library-architect emitting Style Dictionary). The 5 tiers correspond to MD3's broader 16-step durations.

| Tier | Range | Use case | MD3 step |
|---|---|---|---|
| **Micro-interaction** | 80–250 ms | Hover, focus, button press, checkbox toggle | duration-short1..short4 |
| **State change** | 250–500 ms | Menu open, panel expand, modal slide | duration-medium1..medium4 |
| **Entrance animation** | 500–1 000 ms | Scroll-triggered content reveal | duration-long1..long4 |
| **Page transition** | 800–1 200 ms | Route change, overlay full-bleed | duration-extra-long1..extra-long2 |
| **Slow / luxurious** | 1 200–2 000 ms | Editorial scroll, hero parallax (when allowed) | duration-extra-long3..extra-long4 |

## Stagger budget

When multiple elements share a role (e.g. a grid of cards with `entry`), they stagger their starts by 60–120 ms per item. The stagger window for the whole group should not exceed 600 ms — beyond that the user starts to read the late items as "lagging."

```css
.stagger > *:nth-child(1) { animation-delay: 0ms;   }
.stagger > *:nth-child(2) { animation-delay: 80ms;  }
.stagger > *:nth-child(3) { animation-delay: 160ms; }
.stagger > *:nth-child(4) { animation-delay: 240ms; }
/* Cap at 600 ms total — drop the rest into a single fade-up */
```

## Equivalents in framer-motion and Web Animations API

For agents emitting React (`amw-wireframe-builder-agent`) or arbitrary JS (rare):

```tsx
// framer-motion — entry role, default 300 ms
<motion.div
  initial={{ opacity: 0, y: 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
/>
```

```js
// Web Animations API — interaction role, 180 ms, ease-snap
element.animate(
  [{ transform: 'translateY(0)' }, { transform: 'translateY(1px)' }, { transform: 'translateY(0)' }],
  { duration: 180, easing: 'cubic-bezier(0.85, 0, 0.15, 1)' }
);
```

```css
/* Pure CSS — hover role, 120 ms */
.btn {
  transition: transform var(--motion-duration-fast) var(--ease-out),
              filter    var(--motion-duration-fast) var(--ease-out);
}
.btn:hover {
  transform: translateY(-2px);
  filter: brightness(1.05);
}
/* DO NOT: transform: scale(1.05) — banned in ai-slop-avoid.md §21 */
```

## Performance budgets

Independent of duration, three hard performance rules:

1. **Animate only `transform` and `opacity`.** These are GPU-composited. Animating `width`, `height`, `top`, `left`, `margin`, or `padding` triggers layout and will jank on low-end devices.
2. **`will-change` is a loaded gun.** Only set it on elements that are *about to* animate (e.g. on `:hover` parent), never on everything. `will-change` permanently allocates a GPU layer — abused, it tanks memory.
3. **One concurrent ambient.** No page should have two `ambient` motions running simultaneously. Two breathing CTAs read as broken.

## Verification

Before any HTML is delivered, `bin/amw-ai-slop-check.py` runs:

- All `transition` declarations have explicit durations (not `transition: all 0.3s ease`)
- No `transform: scale(1.05)` on `:hover` (or any `scale(1.0X)` between 1.01 and 1.10)
- A `@media (prefers-reduced-motion: reduce)` block exists (see `TECH-reduced-motion.md`)
- No `animation` without `animation-fill-mode: both` (cause of flicker on cold-start)

## See also

- `TECH-motion-taxonomy.md` — the 7 roles this table indexes
- `TECH-motion-density.md` — how many concurrent motions per page
- `TECH-reduced-motion.md` — what survives `prefers-reduced-motion`
- `../ai-slop-avoid.md` §21 — the `scale(1.05)` ban
- `../starter-components/animations.html` — the ~50-LOC timeline core agents reach for
