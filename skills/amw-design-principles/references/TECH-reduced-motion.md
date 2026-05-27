# Reduced motion — the `prefers-reduced-motion` contract

`prefers-reduced-motion: reduce` is a user-agent setting reflecting an explicit user accommodation: motion causes me harm, slows me down, or distracts me. Vestibular disorders, ADHD, autism-spectrum sensory sensitivity, migraine triggers, and post-concussion recovery all surface here.

This is not a "nice to have." It is a WCAG 2.3.3 success criterion (AAA) for interaction-triggered motion and a global a11y best practice for everything else. `amw-accessibility-auditor-agent` (Tier-2) holds **VETO power** over Phase B builds that fail this contract.

## The two media queries

```css
/* User wants motion (default, including when no preference set) */
@media (prefers-reduced-motion: no-preference) { ... }

/* User wants motion REDUCED, not eliminated */
@media (prefers-reduced-motion: reduce) { ... }
```

The spec is explicit: "reduce," not "remove." A site that swaps every transition to `0s` is *technically* compliant but reads as broken — state changes happen with no acknowledgement, focus rings appear/disappear instantly with no perceptible cue. The right model is "keep what communicates, drop what decorates."

## What to KEEP under `prefers-reduced-motion: reduce`

Required — these are affordances, not decoration. Removing them removes the user's ability to operate the page:

| Role | What survives | Duration |
|---|---|---|
| **focus** | Outline appears (border / color / ring) | Instant (0–10 ms) |
| **hover** | Color / brightness / border change | Instant |
| **interaction** | Checkbox check, button press, toggle slide | ≤ 100 ms instant-feeling |
| **exit** | Element disappears with a 1-frame `opacity` step | Instant |
| **state announcements** | ARIA live-region updates | Whatever screen reader uses |
| **page-transition** | Single cross-fade ≤ 100 ms — or instant cut | ≤ 100 ms |

The point: the user still receives feedback. The motion just doesn't *travel* — no slide, no scale, no rotate.

## What to DROP under `prefers-reduced-motion: reduce`

These are decoration. Drop them entirely:

| Role | What goes |
|---|---|
| **entry** | All `transform: translateY()` reveals → instant `opacity: 1` |
| **exit** | No slide-out — just `opacity: 0` immediate |
| **ambient** | Stop all infinite loops. Pause marquees, kill drifting backgrounds, freeze breathing CTAs |
| **page-transition** | Drop wipe / morph / slide — instant cut or ≤ 100 ms cross-fade only |
| **scroll-linked** | Remove parallax, kinetic-typography, scroll-driven keyframes |
| **stagger** | Remove delays — all children appear at once |

## The canonical CSS contract

Every page emitted by the plugin MUST include this block at the **end** of the animation CSS (loading order matters — the override must come *after* the default animation rules):

```css
@media (prefers-reduced-motion: reduce) {
  /* Reset all animations to near-instant. Browsers treat 0.01ms as "complete immediately"
     while still firing animation events, so listener-based code keeps working. */
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Restore the focus indicator — instant but visible. */
  *:focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
    transition: none;
  }
}
```

**Why `0.01ms` and not `0s`:** zero-duration animations skip the `animationstart` / `animationend` events in some engines. JS that gates rendering on those events (intersection observers, video player controls) silently breaks. `0.01ms` is one frame's worth and fires the events.

**Why `scroll-behavior: auto`:** `scroll-behavior: smooth` causes vestibular issues. Override it.

## The JavaScript counterpart

For motion driven by JS (framer-motion, GSAP, Web Animations API), CSS overrides do not apply. Each library has its own switch:

### framer-motion

```tsx
import { motion, useReducedMotion } from 'framer-motion'

export function RevealOnScroll({ children }) {
  const shouldReduce = useReducedMotion()

  return (
    <motion.div
      // When reduced, skip the initial offset — element appears in place
      initial={shouldReduce ? false : { opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: shouldReduce ? 0 : 0.4, ease: [0.23, 1, 0.32, 1] }}
    >
      {children}
    </motion.div>
  )
}
```

### Web Animations API

```js
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

element.animate(keyframes, {
  duration: prefersReduced ? 0 : 400,
  easing: 'cubic-bezier(0.23, 1, 0.32, 1)',
});
```

### Vanilla JS — IntersectionObserver entry pattern

```js
const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return
    // The class triggers a CSS transition. The CSS @media block above ensures
    // the transition is near-instant when reduced motion is preferred.
    entry.target.classList.add('visible')
    observer.unobserve(entry.target)
  })
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' })

document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
```

## Live-changes (the gotcha)

`prefers-reduced-motion` can change while the page is loaded — the user opens system settings, toggles "reduce motion," returns to the tab. CSS handles this automatically; JS does not. For JS-driven motion, **listen** for the change:

```js
const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
motionQuery.addEventListener('change', (e) => {
  if (e.matches) {
    // Stop all running animations, pause looping ones
    document.querySelectorAll('.ambient').forEach(el => el.classList.add('paused'))
  } else {
    document.querySelectorAll('.ambient').forEach(el => el.classList.remove('paused'))
  }
})
```

## Common mistakes

| Mistake | Why it breaks |
|---|---|
| `transition: none !important` on everything | Removes affordances (state change with no cue). Use `0.01ms` instead. |
| Override block placed BEFORE animation rules | CSS cascade — later rules win, override never applies. Always place LAST. |
| `animation-duration: 0` (no unit) | Invalid CSS. Use `0.01ms` or `0ms`. |
| Forgetting `scroll-behavior: auto` | `smooth` scroll causes vestibular issues independently of any animation. |
| Removing focus outline along with motion | WCAG 2.4.7 violation. Focus indicator must remain. |
| Disabling `prefers-reduced-motion` testing in CI | Reduced-motion regressions slip in. Lint a snapshot of the rendered CSS for the override block. |

## Verification gate

Before any HTML / React build leaves Phase B, `bin/amw-ai-slop-check.py` enforces:

1. The literal regex `@media\s*\(\s*prefers-reduced-motion:\s*reduce\s*\)` is present at least once
2. The override block appears at the **end** of the animation rules (after all `@keyframes` and `transition` declarations)
3. No element uses `animation: ... infinite` without a corresponding `.paused` class wired to a reduced-motion listener (for JS-controlled) OR the duration is overridden to `0.01ms` (for CSS-only)
4. No `scroll-behavior: smooth` exists without a paired reduced-motion override

Hard fail at any of the four → block Phase B emission until fixed. The accessibility-auditor (Tier-2) can also veto retroactively.

## See also

- `TECH-motion-taxonomy.md` — the 7 roles, which to keep/drop
- `TECH-motion-budgets.md` — defaults that get overridden under reduce
- `TECH-motion-density.md` — ambient density caps that vanish under reduce
- `../../../agents/amw-accessibility-auditor-agent.md` — holds VETO power on this contract
- WCAG 2.3.3 (Animation from Interactions, AAA)
- WCAG 2.4.7 (Focus Visible, AA — must survive `reduce`)
- WCAG 2.2.2 (Pause, Stop, Hide — applies to ambient + auto-advancing carousels)
