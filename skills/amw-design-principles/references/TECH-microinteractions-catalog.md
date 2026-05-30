# TECH — Microinteractions Catalog

A named catalog of microinteractions for Tier-3 / Tier-4 emitters. Each entry is a small, communicative motion (≤ 400 ms) with a CSS / JS token form and a hard `prefers-reduced-motion` fallback. This file is read by `amw-motion-designer-agent` (primary) and by `amw-wireframe-builder-agent` / `amw-form-designer-agent` (consumers when they need to ship a one-off interaction without spawning the motion specialist).

Provenance / license: each entry's source is annotated. GSAP rules (T-111) and the creative-coder output format (T-112) are direct-port from MIT skills. Popmotion CDN pin (T-113) is a public fact. Goal-Gradient pulse (T-114) and Native browser features (T-123) are clean-room writeups of public web platform behavior.

---

## Tokens (canonical form)

Every microinteraction in this catalog reads from this token set. Define once at the document root; never inline duration / easing in component CSS.

```css
:root {
  /* Duration tokens — 3 stops, no more */
  --motion-fast: 150ms;
  --motion-base: 300ms;
  --motion-slow: 600ms;

  /* Easing tokens — 3 named curves */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);     /* exit, dismiss, hover-leave */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* state change, both directions */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* press release, success */

  /* Composite reduced-motion override — single source of truth */
  --motion-enabled: 1;
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-fast: 0ms;
    --motion-base: 0ms;
    --motion-slow: 0ms;
    --motion-enabled: 0;
  }
}
```

**Hard invariant:** every animation in this catalog uses `transform` / `opacity` only (compositor-only properties). Animating `width`, `height`, `top`, `left`, `margin`, or `padding` triggers layout / paint per frame and is banned outside the explicit kinetic-typography techniques in `amw-pretext/` (TECH-33, TECH-23, TECH-48 — those are agency-of-purpose exceptions, not defaults).

---

## Catalog

### 1. `hover-lift`
**Communicative intent:** "this element is interactive".
**Trigger:** `:hover` (pointer devices only; gated by `(hover: hover)` media query).
**Form:** translateY(-2px) + shadow lift.

```css
.btn-lift {
  transition: transform var(--motion-fast) var(--ease-out),
              box-shadow var(--motion-fast) var(--ease-out);
}
@media (hover: hover) {
  .btn-lift:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgb(0 0 0 / 0.12);
  }
}
```

Reduced-motion fallback: transform becomes 0px (token resolves to 0ms duration); shadow still appears (state cue preserved without movement).

### 2. `focus-ring`
**Communicative intent:** "keyboard focus landed here".
**Trigger:** `:focus-visible` (NOT `:focus` — mouse-click focus does not need a ring).
**Form:** 2px outline + 2px offset, no motion (focus is instantaneous).

```css
.focusable:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  /* No transition — focus must be instant, never animated */
}
```

Reduced-motion: identical (no motion to begin with).

### 3. `press-shrink`
**Communicative intent:** physical press feedback.
**Trigger:** `:active`.
**Form:** scale(0.97), 100 ms.

```css
.btn-press {
  transition: transform var(--motion-fast) var(--ease-out);
}
.btn-press:active {
  transform: scale(0.97);
  transition-duration: 100ms; /* override to faster on press */
}
```

Reduced-motion: scale = 1 (no shrink). Visual selection cue still flows from the `:active` background-color change in the broader button stylesheet.

### 4. `success-pulse`
**Communicative intent:** "the action you just performed succeeded".
**Trigger:** class added on success state.
**Form:** single 600ms scale-and-glow pulse, then settle.

```css
@keyframes success-pulse {
  0%   { transform: scale(1);    box-shadow: 0 0 0 0 var(--color-success); }
  50%  { transform: scale(1.04); box-shadow: 0 0 0 8px transparent; }
  100% { transform: scale(1);    box-shadow: 0 0 0 0 transparent; }
}
.is-success {
  animation: success-pulse var(--motion-slow) var(--ease-spring) 1;
}
@media (prefers-reduced-motion: reduce) {
  .is-success { animation: none; }
  /* Replacement cue: solid 1.5s background flash via separate class */
}
```

### 5. `error-shake`
**Communicative intent:** "the action you just performed failed (input rejected)".
**Trigger:** class added on validation fail.
**Form:** 3-cycle horizontal nudge, ≤ 8 px displacement, 400 ms total.

```css
@keyframes error-shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-6px); }
  40%, 80% { transform: translateX(6px); }
}
.is-error {
  animation: error-shake 400ms var(--ease-in-out) 1;
}
@media (prefers-reduced-motion: reduce) {
  .is-error { animation: none; }
  /* Replacement cue: 2px red outline + error text below input (handled by form-error-recovery) */
}
```

### 6. `loading-shimmer`
**Communicative intent:** "data is loading, this is a skeleton placeholder".
**Trigger:** skeleton-only; never on real content.
**Form:** gradient-position translation, infinite, slow.

```css
@keyframes shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-muted) 0%,
    var(--color-bg-elevated) 50%,
    var(--color-bg-muted) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1500ms linear infinite;
}
@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
    background: var(--color-bg-muted); /* static placeholder color */
  }
}
```

### 7. `goal-gradient-pulse` (Endowed Progress reinforcement) — T-114
**Communicative intent:** "you are almost done — keep going".
**Trigger:** `data-percent` attribute begins with `9` (i.e., 90–99%).
**Form:** soft glow pulse on a progress indicator at the near-completion threshold.

```css
.progress[data-percent^="9"] {
  animation: goal-pulse 1200ms var(--ease-in-out) infinite;
}
@keyframes goal-pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--color-success); }
  50%      { box-shadow: 0 0 8px 2px var(--color-success); }
}
@media (prefers-reduced-motion: reduce) {
  .progress[data-percent^="9"] { animation: none; }
}
```

Companion Endowed-Progress pattern (no animation, structural): when displaying a multi-step checklist, render the first step in a pre-completed state ("1 of N — Profile created") so the user enters at "1 done" rather than "0 done". Hard cap: 5 steps maximum; longer lists kill the goal-gradient effect.

### 8. `native-popover-open` — T-123 fragment
**Communicative intent:** "this tooltip / dropdown just appeared".
**Trigger:** the browser's built-in Popover API (`popovertarget` / `popover` attribute).
**Form:** transition the `:popover-open` state — no JS framework required.

```html
<button popovertarget="hint">Help</button>
<div id="hint" popover>What this field does.</div>
```

```css
[popover] {
  opacity: 0;
  transform: translateY(4px);
  transition: opacity var(--motion-fast) var(--ease-out),
              transform var(--motion-fast) var(--ease-out);
}
[popover]:popover-open {
  opacity: 1;
  transform: translateY(0);
}
@media (prefers-reduced-motion: reduce) {
  [popover] { transition: none; transform: none; }
}
```

Why prefer this over a JS tooltip library: zero bundle weight, native `Escape` dismiss, native focus-trap handling, native top-layer compositing. Browser support: Chrome 114+, Safari 17+, Firefox 125+. If a target browser lacks support, fall back to standard `:hover` + `aria-describedby` (do not polyfill — graceful degradation, not parity).

### 9. `popmotion-physics-spring` (only allowed external lib path) — T-113

The plugin's house rule (see `amw-design-principles/SKILL.md` + the global plugin rule "Animation stack order") is: starter-components animations first; Popmotion 11.0.5 only for physics / spring / drag / inertia that CSS cannot express. No Framer Motion, no GSAP for layout animation.

Pinned CDN:

```html
<!-- Popmotion 11.0.5 — physics/spring fallback only -->
<script src="https://unpkg.com/popmotion@11.0.5/dist/popmotion.global.min.js"
        integrity="sha384-VERIFY_HASH_BEFORE_USE"
        crossorigin="anonymous"></script>
```

When you ship this CDN tag, fetch the integrity SHA from `https://www.srihash.org/` against the exact file — never paste a guessed integrity. The `integrity=` attribute is non-optional (the plugin's React/Babel pin doctrine extends to every CDN script tag).

Usage shape (no API rewrite — Popmotion's docs are canonical):

```js
const { animate } = window.popmotion;
animate({
  from: 0,
  to: 100,
  type: 'spring',
  stiffness: 200,
  damping: 20,
  onUpdate: v => element.style.transform = `translateX(${v}px)`,
});
```

Reduced-motion gate: every Popmotion call site checks `matchMedia('(prefers-reduced-motion: reduce)').matches` and short-circuits to the end state if true.

---

## GSAP rules (T-111) — when the project already has GSAP installed

The plugin does not ship GSAP and does not recommend introducing it (the starter-components timeline + Popmotion physics cover ~95% of needs). When a downstream project already uses GSAP and you must integrate, these rules are non-negotiable:

1. **Never `useEffect` for GSAP timelines.** Always `useGSAP` from `@gsap/react`. `useEffect`'s cleanup ordering races GSAP's tween disposal and leaks tweens on Hot Module Replacement.
2. **Use `autoAlpha`** for show/hide, not separate `opacity` + `visibility` tweens. `autoAlpha` keeps the element out of the accessibility tree when invisible.
3. **Hardware-aliased properties only.** `x`, `y`, `scale`, `rotation` — never `top`, `left`, `width`, `height`. The aliases compile to `transform` (compositor); the others trigger layout.
4. **`scope: container` is required.** Pass the scoping container ref so cleanup tears down only this component's tweens, not the page's.
5. **ScrollTrigger must register exactly once.** `gsap.registerPlugin(ScrollTrigger)` at module top-level, not inside the component (registering twice silently double-fires).
6. **Reduced-motion gate:** every GSAP entry point checks `gsap.matchMedia()` with a `(prefers-reduced-motion: reduce)` query and provides a no-animation branch.

---

## Creative-coder output format (T-112)

When designing a non-trivial microinteraction (anything beyond the catalog entries above), use this skeleton in your spec:

1. **Purpose** — one sentence: what does this motion communicate? If the answer is "it looks cool", the motion is rejected.
2. **Spec** — trigger / states / duration token / easing token.
3. **Implementation** — minimal-first: CSS-only if possible, then CSS + class toggle, then Popmotion spring, then GSAP (last resort).
4. **Accessibility** — explicit `prefers-reduced-motion` branch.
5. **Performance** — names the properties animated and confirms they are `transform` / `opacity` only.
6. **Next** — what is the natural follow-up motion (entry → settle → idle), or "none — this is one-shot".

Checklist gate (apply before delivery):
- [ ] Can I explain this motion's communicative purpose in one sentence?
- [ ] Does it avoid layout-triggering properties? (`transform` / `opacity` only — verified by reading the keyframes.)
- [ ] Reduced-motion branch is present and meaningful (not just `animation: none` with no replacement cue when the cue itself carried information).
- [ ] Duration ≤ 400 ms for state changes; ≤ 600 ms for celebration / ack motions; only `loading-shimmer` may loop.
- [ ] No INP / LCP impact — the animation is not on a layout-affecting element during initial paint.

---

## Breaks-if

This catalog stops working when:

- A consumer hardcodes a duration (`transition: 0.3s`) instead of reading `var(--motion-base)`. Reduced-motion override silently fails because the consumer bypassed the token.
- A consumer animates `top` / `left` / `width` / `height` to mimic these patterns. The animation looks identical at 60 fps on a fast laptop and stutters at 15 fps on a low-end mobile.
- The reduced-motion replacement cue is just `animation: none` for an animation that carried meaning (e.g., `error-shake` without a replacement red-outline rule). The user with motion sensitivity loses the error signal entirely — that is a violation, not a fallback.
- A Popmotion CDN is included without the `integrity=` attribute. A future supply-chain attack at the CDN replaces the script with malicious code; the browser still loads it.
- `prefers-reduced-motion` is queried in JS via `window.matchMedia(...).matches` but never re-queried when the media query changes (user toggling system setting). Use `mql.addEventListener('change', ...)` for live updates if the page lifetime exceeds a typical session.

---

## Component examples

### Example A — Form submit button with success-pulse

```html
<button class="btn-primary btn-lift btn-press" id="submit-order">
  Place order
</button>
```

```js
async function handleSubmit() {
  const btn = document.getElementById('submit-order');
  btn.disabled = true;
  btn.textContent = 'Processing...';
  try {
    await placeOrder();
    btn.classList.add('is-success');
    btn.textContent = 'Order placed';
    btn.addEventListener('animationend', () => btn.classList.remove('is-success'), { once: true });
  } catch (err) {
    btn.classList.add('is-error');
    btn.textContent = 'Try again';
    btn.disabled = false;
    btn.addEventListener('animationend', () => btn.classList.remove('is-error'), { once: true });
  }
}
```

Why this composes: `btn-lift` handles hover, `btn-press` handles tactile feedback, `is-success` / `is-error` are state class swaps that read directly from tokens. The reduced-motion branch in each `@keyframes` rule sets all three durations to zero — the user gets the state class swap as a static color change, which is the correct accessible degradation.

### Example B — Multi-step checkout near-completion glow

```html
<div class="progress" data-percent="92" role="progressbar" aria-valuenow="92" aria-valuemin="0" aria-valuemax="100">
  <div class="progress__fill" style="width: 92%"></div>
</div>
```

```css
.progress { /* ... base styles ... */ }
.progress[data-percent^="9"] {
  animation: goal-pulse 1200ms var(--ease-in-out) infinite;
}
```

The 90–99% bucket gets the reinforcement glow; below 90% the progress bar is static; at 100% the pulse stops (the attribute selector no longer matches `9*`). Reduced-motion users get the static progress bar with no glow — the `aria-valuenow` is still announced, so the goal-gradient signal still reaches assistive-tech users via voice rather than visual reinforcement.

---

## Cross-references

- Animation baseline: `skills/amw-design-principles/starter-components/animations.html` — the ~50-LOC timeline core. Use first; do not reintroduce Framer Motion or GSAP for layouts.
- AI-slop motion rules: `skills/amw-design-principles/ai-slop-avoid.md` § V (interaction and motion) — parallax overuse, infinite spinning logos, scroll-jacking are banned.
- Kinetic typography exceptions: `skills/amw-pretext/references/TECH-33-kinetic-width-animation.md`, TECH-23, TECH-48 — these animate layout properties on purpose; they are not exceptions to the perf rule, they are a distinct category of work owned by `amw-pretext`.
- Form-error microinteractions: `TECH-form-error-recovery.md` (this references catalog uses the `error-shake` and `success-pulse` entries above; form-error-recovery owns the accessibility wiring).
