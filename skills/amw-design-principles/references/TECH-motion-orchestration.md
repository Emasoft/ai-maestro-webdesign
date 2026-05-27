# TECH — Motion orchestration patterns (cascade / sequence / parallel / interrupted)

> **Source attribution:** Pattern names follow the Material Design 3 motion choreography vocabulary (Apache-2.0). Implementation primitives reuse the Web Animations API and CSS `@keyframes` (W3C, open standard). Direct-port with attribution where prose mirrors MD3.

Covers T-109 in the batch9 master ledger. Once more than one element animates in the same moment, the question stops being "what easing?" and becomes "how do these animations relate to each other in time?" This file enumerates the four canonical orchestration patterns — **cascade**, **sequence**, **parallel**, **interrupted** — with code samples in both Web Animations API and CSS `@keyframes`. The motion-designer agent picks one of these patterns for every Phase-B animation spec it produces.

## Token block

```css
:root {
  /* --- Stagger (cascade) deltas — gap between successive child starts --- */
  --stagger-tight:   60ms;   /* Dense lists, large grids — total window ≤600ms */
  --stagger-default: 80ms;   /* Default for entry-role groups */
  --stagger-loose:   120ms;  /* Emphasized cascades, <6 items */

  /* --- Sequence offsets — gap between A's end and B's start --- */
  --sequence-tight:  0ms;    /* B begins as A ends — eye reads as continuous */
  --sequence-default: 80ms;  /* Brief beat — A clearly settles before B begins */
  --sequence-pause:  200ms;  /* Deliberate beat — chapter break in a multi-step reveal */

  /* --- Interruption reverse-duration ratio --- */
  --interrupt-reverse-ratio: 0.6; /* On cancel, reverse takes 60% of forward time */
}
```

## The four orchestration patterns

### 1. Cascade (staggered children)

**What it is:** N siblings each run the same animation, but each delayed by a constant `--stagger-*` value relative to the previous. The eye reads "a wave" rather than "N independent objects." Default for entry-role groups (card grids, feature rows, navigation links).

**Total stagger window must not exceed 600 ms** — beyond that the late items read as "lagging," not "cascading." If a group has 12+ items, switch to parallel (single fade-up) at the count threshold.

```css
/* CSS @keyframes — pure-CSS cascade with nth-child delays */
@keyframes card-entry {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.card-grid > .card {
  opacity: 0; /* hidden until animation fires */
  animation: card-entry var(--duration-medium) var(--ease-emphasized-decelerate) both;
}
.card-grid > .card:nth-child(1) { animation-delay: 0ms;   }
.card-grid > .card:nth-child(2) { animation-delay: var(--stagger-default); }
.card-grid > .card:nth-child(3) { animation-delay: calc(var(--stagger-default) * 2); }
.card-grid > .card:nth-child(4) { animation-delay: calc(var(--stagger-default) * 3); }
.card-grid > .card:nth-child(5) { animation-delay: calc(var(--stagger-default) * 4); }
.card-grid > .card:nth-child(6) { animation-delay: calc(var(--stagger-default) * 5); }
/* Items 7+ collapse to the last delay value (cap at 600ms) */
.card-grid > .card:nth-child(n+7) { animation-delay: calc(var(--stagger-default) * 6); }

@media (prefers-reduced-motion: reduce) {
  .card-grid > .card {
    animation: none;
    opacity: 1; /* Skip the entrance, keep the end state */
  }
}
```

```js
// Web Animations API — programmatic cascade with proper cap
const STAGGER_MS = 80;
const MAX_STAGGER_WINDOW = 600;

document.querySelectorAll('.card-grid > .card').forEach((card, i) => {
  const delay = Math.min(i * STAGGER_MS, MAX_STAGGER_WINDOW);
  card.animate(
    [
      { opacity: 0, transform: 'translateY(24px)' },
      { opacity: 1, transform: 'translateY(0)' }
    ],
    {
      duration: 400,
      delay,
      easing: 'cubic-bezier(0.05, 0.70, 0.10, 1.00)',
      fill: 'both'
    }
  );
});
```

### 2. Sequence (A then B)

**What it is:** B begins after A ends (with optional `--sequence-*` gap). The user reads a narrative — first thing happens, then the second. Use for multi-part reveals where each part communicates a distinct idea.

**Hard rule:** sequences with more than three steps risk losing the user's attention. If you need four steps, ask whether step 4 is actually decorative.

```js
// Web Animations API — sequence with .finished promise chain
async function heroReveal() {
  const headline = document.querySelector('.hero-headline');
  const subhead  = document.querySelector('.hero-subhead');
  const cta      = document.querySelector('.hero-cta');

  // Step 1: headline lands
  const a = headline.animate(
    [{ opacity: 0, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }],
    { duration: 400, easing: 'cubic-bezier(0.05, 0.70, 0.10, 1.00)', fill: 'both' }
  );
  await a.finished;

  // Step 2: subheading appears after 80ms beat
  await new Promise(r => setTimeout(r, 80));
  const b = subhead.animate(
    [{ opacity: 0 }, { opacity: 1 }],
    { duration: 240, easing: 'cubic-bezier(0.20, 0.00, 0.00, 1.00)', fill: 'both' }
  );
  await b.finished;

  // Step 3: CTA enters
  cta.animate(
    [{ opacity: 0, transform: 'scale(0.96)' }, { opacity: 1, transform: 'scale(1)' }],
    { duration: 240, easing: 'cubic-bezier(0.05, 0.70, 0.10, 1.00)', fill: 'both' }
  );
}
```

```css
/* CSS @keyframes — sequence via cumulative delays
   Total length: 400 + 80 + 240 + 0 + 240 = 960ms (just under the long-tier ceiling) */
.hero-headline { animation: fade-up var(--duration-medium) var(--ease-emphasized-decelerate) 0ms both; }
.hero-subhead  { animation: fade-in var(--duration-short)  var(--ease-standard) 480ms both; }
.hero-cta      { animation: pop-in  var(--duration-short)  var(--ease-emphasized-decelerate) 720ms both; }
```

### 3. Parallel (A and B together)

**What it is:** Two or more animations start at the exact same timestamp. Use when the elements are conceptually one unit and the user should read them as moving together (e.g. a card's background fades while its label types in).

**Hard rule:** more than three concurrent easings in the same viewport reads as chaos. See `TECH-motion-perceptual-budgets.md` for the cap.

```js
// Web Animations API — true parallel via simultaneous calls
function modalOpen(modal, backdrop) {
  // Both calls fire in the same task — animations begin together
  backdrop.animate(
    [{ opacity: 0 }, { opacity: 0.6 }],
    { duration: 400, easing: 'cubic-bezier(0.20, 0.00, 0.00, 1.00)', fill: 'both' }
  );
  modal.animate(
    [
      { opacity: 0, transform: 'translateY(16px) scale(0.96)' },
      { opacity: 1, transform: 'translateY(0)    scale(1)'    }
    ],
    { duration: 400, easing: 'cubic-bezier(0.05, 0.70, 0.10, 1.00)', fill: 'both' }
  );
}
```

```css
/* CSS @keyframes — parallel via identical animation-delay (or none) */
.modal-overlay {
  animation: fade-in var(--duration-medium) var(--ease-standard) both;
}
.modal-card {
  animation: card-enter var(--duration-medium) var(--ease-emphasized-decelerate) both;
}
/* Both start at 0ms — read as one motion */
```

### 4. Interrupted (cancel + reverse)

**What it is:** An ongoing animation is canceled mid-flight and replaced with a reverse animation back to the original state. Most common case: user mouses over a button (forward animation starts), then mouses out before completion (reverse animation must take over from the current intermediate state, not jump).

**Hard rule:** the reverse must respect the current position. Replaying the keyframes from `to` to `from` causes a snap if the user interrupted at, say, 40 % progress.

The `--interrupt-reverse-ratio: 0.6` token says: reverse animations run at 60 % of forward duration. The asymmetry feels right because the user has already seen the forward — speed on the reverse signals "okay, I'm not committed."

```js
// Web Animations API — interruption via cancel + reverse-from-current-state
let activeAnimation = null;

function setupInterruptibleHover(el) {
  el.addEventListener('pointerenter', () => {
    if (activeAnimation) activeAnimation.cancel();
    activeAnimation = el.animate(
      [{ transform: 'translateY(0)' }, { transform: 'translateY(-2px)' }],
      { duration: 150, easing: 'cubic-bezier(0.20, 0.00, 0.00, 1.00)', fill: 'forwards' }
    );
  });

  el.addEventListener('pointerleave', () => {
    if (!activeAnimation) return;
    // Read current computed transform — reverse continues from there
    const current = getComputedStyle(el).transform;
    activeAnimation.cancel();
    activeAnimation = el.animate(
      [{ transform: current }, { transform: 'translateY(0)' }],
      { duration: 90, easing: 'cubic-bezier(0.20, 0.00, 0.00, 1.00)', fill: 'forwards' }
    );
  });
}
```

```css
/* CSS-only interruption — uses transition (not animation) so the browser
   handles current-state interpolation automatically. Use for hover/focus. */
.btn {
  transform: translateY(0);
  transition: transform var(--duration-fast) var(--ease-standard);
}
.btn:hover {
  transform: translateY(-2px);
  /* transition handles cancellation on pointerleave naturally */
}
```

The CSS `transition` property handles interruption better than `@keyframes` because the browser's transition engine knows the current intermediate value and interpolates from it. Use `transition` for hover/focus/pointer-driven motion; use `@keyframes` for time-driven motion that should not be interrupted (page entries, scheduled reveals).

## Pattern decision tree

```
Is the motion triggered by something the user can cancel mid-flight?
├── YES → Use CSS transition (auto-interruptible) — pattern "interrupted"
└── NO ↓

Are multiple elements involved?
├── NO → Single element; pick easing+duration, done
└── YES ↓

Are they conceptually one unit (modal + backdrop, card + label)?
├── YES → Pattern "parallel" — start at same timestamp
└── NO ↓

Do they share a class/role but appear as a group (card grid, list items)?
├── YES → Pattern "cascade" — stagger via --stagger-default
└── NO ↓

Should the user read them as discrete narrative steps?
├── YES → Pattern "sequence" — chain via await .finished
└── If none of the above, the motion is probably decorative — remove it.
```

## Breaks if

- A cascade fails to cap at 600 ms total — late items in long lists read as broken.
- A sequence exceeds three steps without explicit user justification — risks user attention loss.
- A parallel pattern uses more than three distinct easings simultaneously — see `TECH-motion-perceptual-budgets.md` chaos rule.
- An interrupted pattern is built on `@keyframes` (instead of `transition`) and the reverse replays the full keyframe range — produces a snap.
- A `prefers-reduced-motion` override is forgotten on a cascade — N delayed transforms still fire, multiplying motion against the user's stated preference.

## See also

- `TECH-motion-taxonomy.md` — the role each orchestrated animation maps to
- `TECH-motion-easing-catalog.md` — easing curves the orchestrator picks per role
- `TECH-motion-duration-budgets.md` — perceptual duration tiers; the long-tier ceiling
- `TECH-motion-perceptual-budgets.md` — viewport-level concurrent-motion cap
- `TECH-motion-budgets.md` — per-role duration + easing matrix; stagger window
- `TECH-reduced-motion.md` — what each pattern collapses to under reduced-motion
- `starter-components/animations.html` — the ~50-LOC timeline core for sequence patterns
