---
name: TECH-spring-physics
category: design-principles-motion
source: Bexa design-principles cluster (direct port, batch9 Wave 2 Round 2, T-049)
license: MIT (Bexa upstream is MIT; plugin re-licenses under its own MIT — see ../../../LICENSE)
also-in: TECH-motion-taxonomy.md (where spring fits among other motion types); TECH-motion-budgets.md (how many simultaneous springs are tolerable); TECH-reduced-motion.md (how spring motion degrades for users with prefers-reduced-motion)
---

# Spring physics for interactive motion

## Table of Contents

- [What it does](#what-it-does)
- [The rule: springs for interactive, easings for non-interactive](#the-rule-springs-for-interactive-easings-for-non-interactive)
- [Why springs feel right where easings feel wrong](#why-springs-feel-right-where-easings-feel-wrong)
- [The 5 named spring presets](#the-5-named-spring-presets)
  - [heavy — modals, drawers, sheets](#heavy--modals-drawers-sheets)
  - [default — buttons, toggles, hover lifts](#default--buttons-toggles-hover-lifts)
  - [snappy — tooltips, popovers, contextual menus](#snappy--tooltips-popovers-contextual-menus)
  - [drift — hero animations, ambient motion](#drift--hero-animations-ambient-motion)
  - [bounce — celebrations, success states](#bounce--celebrations-success-states)
- [How to read stiffness, damping, mass](#how-to-read-stiffness-damping-mass)
- [Reduced-motion fallback](#reduced-motion-fallback)
- [Cross-references](#cross-references)

## What it does

Every interactive motion in this plugin is implemented as a **spring**, not a CSS `ease` / `ease-in-out` / `linear` curve. Springs feel correct to humans because the physics matches lived experience — a real object responding to a push behaves like a damped harmonic oscillator, not like a linear interpolation. CSS easings feel mechanical the moment the user can see two of them at once.

This file enshrines 5 named spring presets that the motion-designer agent and the animation-stack starter component compose into every interactive surface. Tuning is done by name (`heavy`, `default`, `snappy`, `drift`, `bounce`), not by inventing new triples for each component.

## The rule: springs for interactive, easings for non-interactive

**Interactive motion** = any motion the user causes by clicking, tapping, dragging, hovering, focusing, or pressing a key. The user expects the system to respond to *them*; if the response feels mechanical, the system feels mechanical.

- Modal opens / closes: **spring**.
- Button presses: **spring**.
- Toggle flips: **spring**.
- Drawer / sheet slide-ins: **spring**.
- Hover lift on a card: **spring**.
- Tooltip appearance after a delay: **spring**.
- Notification toast slide-in: **spring**.

**Non-interactive motion** = animation the system runs on its own schedule, where there's no user causing the motion. Cubic-bezier easings are correct here.

- Loading spinners (continuous rotation): **linear** or `cubic-bezier`.
- Marquees (continuous horizontal scroll): **linear**.
- Skeleton shimmers (pulsing brightness): **ease-in-out**.
- Progress-bar fills tied to a known duration: **linear** or `cubic-bezier`.
- Page-load fade-in (one-time, no user input): **cubic-bezier** is acceptable; spring is also acceptable.

**Forbidden everywhere:**
- `transition: all 200ms ease` on buttons. Reads as a 2015 CSS tutorial. Use a spring.
- `transition: all 200ms linear` on anything visible. Linear interpolation looks wrong on any motion under 800ms.

## Why springs feel right where easings feel wrong

A cubic-bezier easing has a fixed duration and a fixed shape. Two simultaneous easings — say, two cards animating in at the same time — finish at exactly the same moment in lockstep. That synchronisation reads as choreographed-and-fake.

A spring has stiffness, damping, and mass — three numbers — and converges to the target asymptotically. Two simultaneous springs from different starting positions arrive at different moments because their initial velocities differ. That asynchrony reads as physical and natural.

Springs also handle interruption gracefully. If the user clicks a button mid-animation, a spring continues from its current velocity to the new target — the motion doesn't reset, doesn't snap, doesn't jank. A cubic-bezier interrupted mid-flight either snaps to the new target or restarts the whole curve, both of which feel broken.

This is why the rule is **never `ease` / `linear` for interactive elements — springs only**.

## The 5 named spring presets

These are the canonical names every agent uses. Adding a 6th preset requires a TRDD; tuning the existing 5 is an open invitation to inconsistency and is forbidden in normal Phase B work.

### heavy — modals, drawers, sheets

```js
{ stiffness: 80, damping: 18, mass: 1.2 }
```

**Use for:**
- Modal open / close
- Drawer (side panel) slide in
- Bottom-sheet slide up
- Full-screen takeover transition

**Why these numbers.** Low stiffness (80) means the spring is "soft" and takes longer to traverse. High damping (18) and high mass (1.2) prevent overshoot — a modal that bounces past its target reads as a toy, not a system surface. The result: ~400–600ms motion that feels substantial without being slow.

### default — buttons, toggles, hover lifts

```js
{ stiffness: 140, damping: 20, mass: 0.8 }
```

**Use for:**
- Button press (scale 1 → 0.97 → 1)
- Toggle / switch flip
- Card hover lift (`translateY(-4px)`)
- Tab indicator slide
- Accordion expand / collapse

**Why these numbers.** Medium stiffness with damping ≈ critical damping (computed as `2 * sqrt(k * m)` ≈ 21 for these values — damping 20 is just below critical, so the motion is fast and barely overshoots). Mass under 1 (0.8) means the response feels light and responsive. The result: ~200–300ms motion that feels snappy without being abrupt.

### snappy — tooltips, popovers, contextual menus

```js
{ stiffness: 300, damping: 28, mass: 0.5 }
```

**Use for:**
- Tooltip appearance after hover delay
- Popover / context menu open
- Dropdown open
- Floating-label move on input focus

**Why these numbers.** High stiffness (300) means fast convergence. Low mass (0.5) means low inertia. Damping (28) is set above critical-for-this-mass to suppress any overshoot — tooltips that bounce feel weird. The result: ~120–180ms motion that's essentially immediate but smooth.

### drift — hero animations, ambient motion

```js
{ stiffness: 60, damping: 15, mass: 1.0 }
```

**Use for:**
- Hero element entrance (one-time on page load)
- Parallax decoration drift
- Ambient floating SVG / blob
- Section-on-scroll reveal

**Why these numbers.** Very low stiffness (60) and below-critical damping (15) produce a long, lazy convergence. The result: ~700–1000ms motion that reads as deliberate and atmospheric. Used sparingly — drift on too many elements at once reads as "every animation is fighting for attention".

### bounce — celebrations, success states

```js
{ stiffness: 400, damping: 12, mass: 0.6 }
```

**Use for:**
- Success checkmark appearance
- Confetti pop on a milestone
- "Thanks for subscribing" reveal
- Achievement badge unlock
- Cart-item add (slight overshoot to confirm "yes, it landed")

**Why these numbers.** High stiffness (400) for snap. Damping (12) is well below critical-for-this-mass-and-stiffness (critical ≈ 31), which produces deliberate overshoot — the motion goes past the target, returns, and settles. The result: ~300–400ms motion with 1–2 visible bounces that conveys "yes! something good happened!"

Use sparingly. Bounce on every interaction reads as a children's app.

## How to read stiffness, damping, mass

In a damped harmonic spring (`F = -kx - cv`):

- **Stiffness (`k`)** — how strongly the spring pulls toward the target. Higher = faster convergence. Lower = slower, lazier convergence.
- **Damping (`c`)** — how strongly velocity is resisted. Damping ABOVE critical (`c > 2*sqrt(k*m)`) means no overshoot, the target is approached asymptotically. Damping BELOW critical means overshoot and bounce.
- **Mass (`m`)** — how much inertia the moving element has. Higher = slower to start, slower to stop. Lower = more responsive.

Critical damping coefficient: `c_critical = 2 * sqrt(k * m)`. Above critical → smooth-no-bounce. Below critical → underdamped → bouncy. At critical → fastest possible no-bounce response.

Cross-checking the presets:

| Preset | k | c | m | c_critical = 2√(km) | Behavior |
|---|---|---|---|---|---|
| heavy | 80 | 18 | 1.2 | 19.6 | slightly underdamped, settles fast (modal feels weighty) |
| default | 140 | 20 | 0.8 | 21.2 | slightly underdamped, ~1 micro-bounce (button feels alive) |
| snappy | 300 | 28 | 0.5 | 24.5 | overdamped → no bounce, fast (tooltips feel immediate) |
| drift | 60 | 15 | 1.0 | 15.5 | very slightly underdamped → slow, lazy convergence (hero feels atmospheric) |
| bounce | 400 | 12 | 0.6 | 31.0 | strongly underdamped → 1–2 visible bounces (success feels celebratory) |

Agents should not invent new triples — pick the preset whose row matches the intended feeling.

## Reduced-motion fallback

Users with `prefers-reduced-motion: reduce` get a different code path entirely:

- Springs for interactive motion are replaced with `cubic-bezier(0.4, 0, 0.2, 1)` over 150ms with **no overshoot** for ALL presets.
- Drift animations are replaced with instant appearance (no motion).
- Bounce animations are replaced with default (no overshoot).

The agent never disables the motion entirely (users still need feedback that their click was received); it removes the *visual flair* — overshoot, bounce, drift — while keeping the *functional feedback* — the element moves to its new position.

See [TECH-reduced-motion.md](./TECH-reduced-motion.md) for the full prefers-reduced-motion contract.

## Cross-references

- [TECH-motion-taxonomy.md](./TECH-motion-taxonomy.md) — where spring fits among easings, page transitions, parallax, scroll-driven motion
- [TECH-motion-budgets.md](./TECH-motion-budgets.md) — how many simultaneous springs are tolerable per screen
- [TECH-motion-density.md](./TECH-motion-density.md) — when to apply springs aggressively vs sparingly per archetype
- [TECH-reduced-motion.md](./TECH-reduced-motion.md) — full degradation path for accessibility
- [TECH-tone-archetypes.md](./TECH-tone-archetypes.md) — archetype determines which spring is appropriate (luxury → heavy; playful → bounce)
- [skills/amw-design-principles/starter-components/animations.html](../starter-components/animations.html) — ~50-LOC timeline core that exposes these 5 presets by name
- [skills/amw-design-principles/ai-slop-avoid.md](../ai-slop-avoid.md) — bans `transition: all 200ms ease` and the framer-motion / GSAP dependencies these presets replace
- [agents/amw-motion-designer-agent.md](../../../agents/amw-motion-designer-agent.md) — agent that selects and applies these presets
- [agents/amw-wireframe-builder-agent.md](../../../agents/amw-wireframe-builder-agent.md) — Phase B emitter that wires the chosen preset into HTML
- [skills/amw-design-principles/SKILL.md](../SKILL.md) — orchestrator
