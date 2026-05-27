# TECH — Motion duration budgets (perceptual tiers)

> **Source attribution:** Perceptual duration bands derived from Doherty Threshold research, RAIL performance model (Google, Apache-2.0), and Material Design 3 motion specification. This file consolidates them into a four-tier perceptual budget tied to design-token names.

Covers T-108 in the batch9 master ledger. The 5-band per-role duration table in `TECH-motion-budgets.md` describes which role takes which duration. This file flips the axis: it describes how the human visual cortex perceives duration regardless of role, and what design-token name fits each perceptual band. Use this when authoring duration token vocabularies (Style Dictionary, Figma Tokens, MD3 `duration-short1..extra-long4`) or when reviewing a third-party design system for perceptual coherence.

## Token block

```css
:root {
  /* Below the perceptual threshold of "an animation" — feels instantaneous */
  --duration-instant: 0ms;

  /* Micro — sub-attention; user perceives the change but not the motion */
  --duration-quick:   80ms;   /* Lower bound: 50ms; upper: 100ms */
  --duration-fast:    150ms;  /* Hover, focus, button press */

  /* Short — registered as motion, completes within a glance */
  --duration-short:   240ms;  /* Lower bound: 100ms; upper: 300ms */

  /* Medium — felt as an animation; the eye follows the trajectory */
  --duration-medium:  400ms;  /* Lower bound: 300ms; upper: 500ms */

  /* Long — narrative duration; user can comment on the motion */
  --duration-long:    700ms;  /* Lower bound: 500ms; upper: 1000ms */

  /* Loading-state territory — anything beyond this MUST show a progress UI */
  --duration-loading-threshold: 1000ms;
}
```

The three existing tokens in `TECH-motion-budgets.md` (`--motion-duration-fast/medium/slow`) remain canonical for downstream skills. The five `--duration-*` tokens above are the perceptual layer — a finer-grained scale that lets motion-designer reason about whether a duration crosses a perceptual threshold before it's locked into a role-specific token.

## The four perceptual tiers

| Tier | Range | What the user perceives | Token | Use cases |
|---|---|---|---|---|
| **Micro** | <100 ms | "It happened" — change is registered but no motion experienced | `--duration-quick` | Press-down on button; immediate hover color flicker; checkbox check (when target is small) |
| **Short** | 100–300 ms | "It moved" — motion noticed but eye does not track | `--duration-fast`, `--duration-short` | Hover lift; focus ring grow; toggle slide; tooltip fade-in |
| **Medium** | 300–500 ms | "It animated" — eye follows the trajectory and arrives with the element | `--duration-medium` | Element entrance; modal open; drawer slide; menu reveal |
| **Long** | 500–1000 ms | "I'm watching this animation" — duration becomes part of the experience | `--duration-long` | Page transition; hero reveal; emphasized state change |
| **Loading-state** | >1000 ms | "Is it broken?" — user begins to doubt | n/a — switch to progress UI | Anything that crosses this threshold needs a skeleton screen, spinner, or determinate progress bar (see `TECH-perceived-performance.md` per `MASTER-LEDGER.md` T-110) |

## Why these specific boundaries

- **100 ms** — Doherty Threshold lower bound. Below this the user perceives the change as direct manipulation (no "system delay"). Confirmed by Nielsen, RAIL, and the original IBM Doherty paper (1982).
- **300 ms** — visual cortex's reliable detection of motion direction. Below 300 ms, the eye registers a change but doesn't form a "trajectory mental model." Above 300 ms, the user starts attributing motion to a causing object.
- **500 ms** — the perceptual threshold where a motion goes from "instantaneous-feeling" to "I waited." Material Design 3 puts the boundary between short and medium durations here.
- **1000 ms** — the RAIL "wait" threshold. Beyond 1s, users disengage and begin to suspect failure. Any motion that crosses this MUST be replaced with (or wrapped in) a loading-state UX (skeleton, spinner, progress bar).

## Mapping to existing role budgets

Cross-reference with `TECH-motion-budgets.md` per-role table:

| Role | Role's default duration | Perceptual tier | Notes |
|---|---|---|---|
| hover | 120 ms | Short | At the boundary of micro/short — user perceives change but not motion |
| focus | 120 ms | Short | Same as hover |
| interaction | 180 ms | Short | Below the trajectory-tracking threshold; feels decisive |
| exit | 200 ms | Short | Quick dismissal |
| entry — above-fold | 250 ms | Short | Must complete before user begins reading |
| entry — below-fold | 400 ms | Medium | Eye follows the entrance; trajectory matters |
| page-transition | 500 ms | Medium/long boundary | Split-curve: 200 ms exit + 300 ms enter |
| ambient | 2000–30000 ms | Loading-state territory but exempt — loops don't trigger doubt because they're never "complete" |

## Code samples

### Before — fixed duration across all motion (bad)

```css
* {
  transition: all 0.3s ease;
}
.btn { transition: transform 0.3s ease; }
.modal-overlay { transition: opacity 0.3s ease; }
.page-content { transition: opacity 0.3s ease; }
```

Problems: a 300 ms hover feels laggy (above the Doherty Threshold); a 300 ms page transition feels rushed (below the medium-duration threshold). One value cannot serve micro and macro at once.

### After — perceptual tiers honored (good)

```css
/* Hover — micro tier so press feels direct */
.btn {
  transition:
    transform var(--duration-fast) var(--ease-standard),
    filter    var(--duration-fast) var(--ease-standard);
}
.btn:hover {
  transform: translateY(-2px);
  filter: brightness(1.05);
}

/* Modal — medium tier so the eye tracks the entrance */
.modal {
  transition:
    transform var(--duration-medium) var(--ease-emphasized-decelerate),
    opacity   var(--duration-medium) var(--ease-emphasized-decelerate);
}

/* Page transition — long tier for narrative weight */
.page-enter {
  animation: page-enter var(--duration-long) var(--ease-emphasized-decelerate) both;
}

/* Anything over the loading threshold — switch to skeleton, not a long animation */
.list-loading {
  /* DO NOT animate the list itself — show a shimmer skeleton instead */
  /* See TECH-perceived-performance.md per ledger T-110 */
}
```

### JS — gating long motion behind a loading-state UX

```js
// Operation expected to take 1+ seconds — DO NOT animate the wait
async function fetchAndRenderList() {
  showSkeleton();                 // <1000ms tier: skeleton shimmer
  const data = await fetch('/api/list').then(r => r.json());
  hideSkeleton();
  // Render new content with --duration-medium entrance
  renderList(data, { entranceDuration: 400 });
}
```

## Breaks if

- A hover or focus duration is set to a value in the Medium tier (300+ ms). The user perceives lag.
- A page transition is set to a value in the Short tier (<300 ms). The user perceives a hard cut instead of a transition; the route change feels disorienting.
- An animation crosses 1000 ms without a loading-state wrapper (skeleton, spinner, progress bar). The user begins to doubt whether the UI is responsive.
- A token-emitting agent (`amw-component-library-architect-agent`) exports a single `--motion-duration: 0.3s` token without the perceptual tier scaffolding. Downstream consumers cannot reason about role-appropriate durations.

## See also

- `TECH-motion-budgets.md` — per-role duration matrix (this file is its perceptual companion)
- `TECH-motion-easing-catalog.md` — which easing curve pairs with which duration
- `TECH-motion-orchestration.md` — how to sequence multiple durations
- `TECH-motion-perceptual-budgets.md` — concurrent-motion budget per viewport
- `TECH-reduced-motion.md` — what every duration collapses to under reduced-motion
- Doherty Threshold reference: https://en.wikipedia.org/wiki/Doherty_threshold
- RAIL performance model: https://web.dev/articles/rail (Apache-2.0)
