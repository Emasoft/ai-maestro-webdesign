# TECH — Motion perceptual budgets (concurrent-motion caps per viewport)

> **Source attribution:** Concurrent-motion thresholds derived from Doherty / RAIL research, Material Design 3 motion guidance (Apache-2.0), and the WCAG 2.1 vestibular-disorder accommodation guidance (W3C, open standard). Direct-port with attribution where prose mirrors MD3.

Covers T-110 in the batch9 master ledger. `TECH-motion-density.md` already defines a three-tier density per page archetype. This file zooms in on what the **viewport** can carry at any single moment without crossing the user's perceptual budget. The density rule asks "how busy is the page over time"; the perceptual-budget rule asks "how busy is the screen *right now*." Both must be satisfied.

## Token block

```css
:root {
  /* Maximum number of elements with an active animation at one instant */
  --concurrent-animated-regions-max: 5;

  /* Maximum number of distinct easing curves visible at one instant */
  --concurrent-easings-max: 3;

  /* Reduced-motion override duration — every active animation collapses to this */
  --reduced-motion-duration: 0ms;

  /* Interactive vs ambient footprint allocations */
  --interactive-motion-share: 4;  /* Of the 5 concurrent slots, 4 may be interactive */
  --ambient-motion-share:     1;  /* And 1 may be ambient */
}
```

## The four hard rules

### Rule 1 — `≤5 simultaneous animated regions`

At any single rendered frame, no more than 5 elements may have an active `transform` or `opacity` animation. Above this count, the cognitive load is measurably degraded: eye-tracking studies show users miss critical UI cues when more than 5 regions move concurrently.

Counting:
- Each animated DOM element counts as 1, regardless of how many properties it animates.
- A cascading group counts as 1 only if all items finish within a 600 ms window — beyond that, late items count separately because the cascade has "broken apart" perceptually.
- Ambient loops count as 1 each. (A footer with 6 client logos drifting independently is 6, not 1.)
- A `transition` triggered by `:hover` counts as 1 while active.

The motion-designer agent enforces this by audit at the artifact-completion stage. If the proposed animation set exceeds 5 concurrent regions, the agent returns a `warnings` entry suggesting which animations to defer (typically: ambient first, then non-hero entries).

### Rule 2 — `≤3 distinct easings concurrently = signal, ≥4 = chaos`

Within the 5 active animations, no more than 3 distinct easing curves should be visible at once. Above 3, the eye loses the ability to read "motion language" — the screen becomes a soup of motion signatures that no longer communicate a hierarchy of importance.

Counting:
- Two animations both using `--ease-emphasized-decelerate` count as 1 distinct easing.
- The four short aliases (`--ease-out`, `--ease-in-out`, `--ease-spring`, `--ease-snap`) and the six MD3 names map onto each other — count by distinct cubic-bezier value, not by token name.
- Linear (ambient) is exempt from this count up to one usage per viewport.

### Rule 3 — `prefers-reduced-motion: reduce` overrides ALL durations to 0ms while preserving the state transition

Every animation has TWO required outputs from the motion-designer agent:
1. The normal-motion spec.
2. The reduced-motion fallback.

The reduced-motion fallback strips the motion (duration → 0ms or replaces with an opacity-only crossfade ≤150ms) but preserves the **state change**. The user with vestibular sensitivity still sees that the modal opened, the dropdown expanded, the new content arrived — they just don't see it move.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 1ms !important;
    animation-delay: 0ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    /* IMPORTANT: do NOT set animation: none or display: none */
    /* The state change must still occur; only the motion is suppressed */
  }
}
```

The `1ms` (rather than `0ms`) is a workaround for Safari, which occasionally drops events on `0ms` durations. Functionally indistinguishable from instant.

### Rule 4 — Safe motion footprint allocation (interactive vs ambient)

Of the 5 concurrent slots:
- **4 slots reserved for interactive motion** — entry, exit, hover, focus, interaction, page-transition. These are user-triggered or user-relevant.
- **1 slot reserved for ambient motion** — background drift, breathing CTA, low-density particle field. Never more than 1 ambient motion in a viewport, ever.

This means a page can have a hero entrance, a card-grid cascade, an open modal, a hover on a sidebar nav item, AND a slow background gradient drift — all simultaneously — and stay within budget. Adding a second ambient (e.g. a marquee in the footer while a hero gradient also drifts) violates the allocation.

## Code samples

### Before — unbudgeted motion (bad)

```html
<body>
  <section class="hero"> <!-- ambient gradient drift -->
    <h1 class="hero-headline">...</h1> <!-- entrance fade-up -->
    <p class="hero-subhead">...</p>    <!-- entrance fade -->
    <a class="hero-cta">...</a>        <!-- entrance scale -->
  </section>
  <section class="features">
    <div class="card"></div> <!-- card 1 entrance -->
    <div class="card"></div> <!-- card 2 entrance -->
    <div class="card"></div> <!-- card 3 entrance -->
    <div class="card"></div> <!-- card 4 entrance -->
    <div class="card"></div> <!-- card 5 entrance -->
    <div class="card"></div> <!-- card 6 entrance -->
  </section>
  <footer>
    <div class="marquee">...</div>      <!-- ambient marquee -->
    <div class="logo-strip-drift">...</div> <!-- ambient drift -->
  </footer>
</body>
<style>
  /* No prefers-reduced-motion override anywhere */
  .card-grid > .card { animation: card-entry 800ms cubic-bezier(.34,1.56,.64,1) both; }
</style>
```

Problems counted at the moment the hero is in view: 1 ambient + 3 hero entries + (cards not yet animating — they wait on scroll). But on scroll into the features section: 1 ambient (still) + 6 cards entering simultaneously = 7 concurrent regions. Plus the footer has 2 ambient loops continuously = at peak, 9 concurrent animated regions across 3+ easings. Chaos. No reduced-motion override.

### After — budgeted motion (good)

```html
<body>
  <section class="hero">
    <div class="hero-bg-drift"></div>  <!-- ambient: 1 slot -->
    <h1 class="hero-headline">...</h1> <!-- entry: 1 slot -->
    <p class="hero-subhead">...</p>    <!-- entry: 1 slot -->
    <a class="hero-cta">...</a>        <!-- entry: 1 slot -->
  </section>
  <!-- Hero peak: 4 concurrent regions, 2 easings (ambient linear + entry decelerate). Within budget. -->

  <section class="features">
    <div class="card-grid"> <!-- cascade of 6, total window 600ms — 1 perceptual unit -->
      <div class="card"></div>
      <div class="card"></div>
      <div class="card"></div>
      <div class="card"></div>
      <div class="card"></div>
      <div class="card"></div>
    </div>
  </section>
  <!-- Features peak: 1 ambient (still) + 1 cascade unit = 2 concurrent regions. -->

  <footer>
    <div class="logo-strip-drift">...</div>  <!-- ambient: replaces hero ambient as user scrolls -->
  </footer>
  <!-- Footer peak: 1 ambient. Hero ambient paused once it scrolls out of view via IntersectionObserver. -->
</body>

<style>
  /* All non-ambient animations gated through perceptual budget tokens */
  .hero-headline { animation: fade-up var(--duration-medium) var(--ease-emphasized-decelerate) 0ms   both; }
  .hero-subhead  { animation: fade-in var(--duration-short)  var(--ease-standard)              200ms both; }
  .hero-cta      { animation: pop-in  var(--duration-short)  var(--ease-emphasized-decelerate) 400ms both; }

  /* Cascade caps at 600ms total — past item 6 collapses to last delay */
  .card-grid > .card:nth-child(n+7) { animation-delay: var(--stagger-cap, 600ms); }

  /* MANDATORY reduced-motion override */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 1ms !important;
      animation-delay: 0ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 1ms !important;
    }
    /* State changes preserved — modal still opens, card grid still appears,
       hero still renders. The user just doesn't see motion. */
  }
</style>

<script>
  // Pause ambient when not in view — keeps the 1-ambient-slot invariant
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      e.target.style.animationPlayState = e.isIntersecting ? 'running' : 'paused';
    });
  });
  document.querySelectorAll('.hero-bg-drift, .logo-strip-drift').forEach(el => obs.observe(el));
</script>
```

### JS — runtime budget audit (debug-only)

```js
// Drop into console during Phase B QA — counts active animations
function auditMotionBudget() {
  const allAnims = document.getAnimations();
  const running = allAnims.filter(a => a.playState === 'running');
  const easings = new Set(running.map(a => a.effect?.getTiming().easing));

  console.table({
    'Concurrent animations': running.length,
    'Limit (--concurrent-animated-regions-max)': 5,
    'Distinct easings':       easings.size,
    'Limit (--concurrent-easings-max)':         3,
    'Status': (running.length <= 5 && easings.size <= 3) ? 'PASS' : 'FAIL'
  });
}

setInterval(auditMotionBudget, 500); // Run every 500ms during scroll/interaction
```

## Interactive vs ambient — the safe footprint

| Class | Concurrent cap | Examples |
|---|---|---|
| **Interactive** | 4 simultaneous max | Entry, exit, hover, focus, interaction, page-transition |
| **Ambient** | 1 simultaneous max — period | Background drift, breathing CTA, low-density particles |

Interactive motion is user-triggered or user-relevant; the user "expects" it because they did something. Ambient motion is unprovoked; the user reads it as the page being "alive." A second ambient signals "noise" — the page reads as agitated rather than alive.

The motion-designer agent enforces a hard ban on any artifact emitting 2+ ambient loops in the same viewport. If a hero ambient drift and a footer marquee both exist, only the in-view one runs (via IntersectionObserver `animationPlayState` toggling).

## Breaks if

- An artifact emits 6+ concurrent animated regions visible in one viewport — agent flags `warnings` entry and proposes a cascade collapse.
- An artifact emits 4+ distinct easing curves visible at once — agent flags `warnings` with the recommendation to consolidate to ≤3 easings.
- The `@media (prefers-reduced-motion: reduce)` block is missing — `bin/amw-ai-slop-check.py` fails the gate. The check is mandatory before any HTML emission.
- A reduced-motion override sets `animation: none` or `display: none` — strips not only motion but the state change itself. Always use `animation-duration: 1ms` or an opacity-only crossfade.
- Two ambient loops run in the same viewport simultaneously — agent flags this regardless of total count.
- An ambient loop runs even when scrolled out of view — wastes GPU and battery; must be `animation-play-state: paused` via IntersectionObserver.

## See also

- `TECH-motion-taxonomy.md` — the 7 roles each budgeted animation maps to
- `TECH-motion-density.md` — per-page density (this file is the per-viewport companion)
- `TECH-motion-budgets.md` — per-role duration + easing matrix
- `TECH-motion-orchestration.md` — cascade/sequence/parallel/interrupted patterns
- `TECH-motion-duration-budgets.md` — perceptual duration tiers
- `TECH-motion-easing-catalog.md` — the 6 MD3 + 4 alias easing curves
- `TECH-reduced-motion.md` — the canonical reduced-motion contract
- `../ai-slop-avoid.md` §V — interaction-and-motion bans
- WCAG 2.1 SC 2.3.3 — Animation from Interactions (vestibular accommodation)
