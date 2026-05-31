---
name: TECH-pattern-vocabulary
category: design-principles-reference
source: pattern NAMES adapted from taste-skill §10 "Reference Vocabulary" (Leonxlnx, MIT); one-line descriptions reworded; the "amw status" column, the slop-adjacent flags, and the animation-stack override are amw-specific (no verbatim copy)
license: this file = MIT (plugin license)
also-in: "amw-design-principles SKILL.md (shared naming for Phase A communication); TECH-microinteractions-catalog.md (implementation hub for the interaction patterns); ai-maestro-webdesign-main-agent (names patterns when reading the brief and proposing variants)"
---

# PATTERN VOCABULARY — shared names for the patterns the agent should know

## Table of Contents

- [What this is (and is not)](#what-this-is-and-is-not)
- [How to read the status column](#how-to-read-the-status-column)
- [Hero paradigms](#hero-paradigms)
- [Navigation & menus](#navigation--menus)
- [Layout & grids](#layout--grids)
- [Cards & containers](#cards--containers)
- [Scroll animations](#scroll-animations)
- [Galleries & media](#galleries--media)
- [Typography & text](#typography--text)
- [Micro-interactions & effects](#micro-interactions--effects)
- [Animation stack — our override](#animation-stack--our-override)
- [Cross-references](#cross-references)

## What this is (and is not)

A **vocabulary**, not a library. The point is shared naming: the orchestrator, the user, and the sub-agents can say "Asymmetric Split Hero" or "Sticky-Stack sections" and mean the same thing, communicate about a direction in Phase A without a paragraph of description, and reach for a named pattern when the [Design Read](two-mode-workflow.md) calls for it.

Implementations live in the plugin's existing skills (the status column points to them). This file does NOT contain code — it contains names + one-line meanings + where we stand on each. It complements the **graphic-style catalogue** (aesthetic systems: brutalism, editorial, etc.) — those are *looks*; these are *layout / interaction patterns*.

## How to read the status column

| Marker | Meaning |
|---|---|
| **→ `<file>`** | We ship implementation guidance; that reference is the hub. |
| **vocab-only** | Named here for communication; no shipped recipe yet. Build it from primitives if the brief calls for it. |
| **⚠ restraint** | Slop-adjacent. Allowed ONLY when it earns its place, with a reduced-motion gate; see [ai-slop-avoid](../ai-slop-avoid.md). Default to NOT using it. |
| **scroll-care** | Must respect `prefers-reduced-motion`, must not break native scroll or nest scrollbars, must not steal scroll inertia. |

When in doubt, a named pattern is a *candidate*, never a *requirement* — the three-variant rule and the dials decide whether it ships.

## Hero paradigms

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Asymmetric Split Hero** | Text on one side, asset on the other, generous whitespace. | → [TECH-landing-anatomy](TECH-landing-anatomy.md) |
| **Editorial Manifesto Hero** | Large type, no asset, almost a poster. | → [TECH-landing-anatomy](TECH-landing-anatomy.md) + [TECH-signature-move](TECH-signature-move.md) |
| **Video / Media-Mask Hero** | Type cut out as a mask over a video/media background. | vocab-only · scroll-care (autoplay + reduced-motion) |
| **Kinetic-Type Hero** | Animated typography as the primary visual. | → [TECH-signature-move](TECH-signature-move.md) · uses our [animation stack](#animation-stack--our-override) |
| **Curtain-Reveal Hero** | Hero parts on scroll like a curtain. | vocab-only · scroll-care |
| **Scroll-Pinned Hero** | Hero stays pinned while content scrolls behind. | → [TECH-motion-orchestration](TECH-motion-orchestration.md) · scroll-care |

## Navigation & menus

| Pattern | One-line meaning | amw status |
|---|---|---|
| **macOS Dock Magnification** | Edge nav; icons scale fluidly on hover. | vocab-only |
| **Magnetic Button** | Button nudges toward the cursor. | vocab-only · ⚠ restraint (gimmick unless it aids a primary CTA) |
| **Gooey Menu** | Sub-items detach like viscous liquid. | ⚠ restraint |
| **Dynamic Island** | Morphing pill for status / alerts. | vocab-only |
| **Contextual Radial Menu** | Circular menu expanding at the click point. | vocab-only |
| **Floating Speed Dial** | FAB springing into curved secondary actions. | vocab-only |
| **Mega-Menu Reveal** | Full-screen dropdown, stagger-fade content. | → [TECH-motion-orchestration](TECH-motion-orchestration.md) |

## Layout & grids

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Bento Grid** | Asymmetric tile grouping (Apple Control Center). | vocab-only (CSS Grid mixed cell sizes — no library) |
| **Masonry Layout** | Staggered grid, no fixed row height. | vocab-only (CSS columns / grid masonry) |
| **Chroma Grid** | Tiles with subtle animating gradient borders. | ⚠ restraint (animated gradient borders read as decoration) |
| **Split-Screen Scroll** | Two halves sliding in opposite directions. | scroll-care |
| **Sticky-Stack Sections** | Sections that pin and stack on scroll. | → [TECH-motion-orchestration](TECH-motion-orchestration.md) · scroll-care |

## Cards & containers

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Parallax Tilt Card** | 3D tilt tracking the mouse. | → [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) · ⚠ restraint (one signature card, not every card) |
| **Spotlight Border Card** | Border illuminates under the cursor. | vocab-only · ⚠ restraint |
| **Glassmorphism Panel** | Frosted glass with inner refraction. | ⚠ restraint (solid-fill fallback for `prefers-reduced-transparency` mandatory) |
| **Holographic Foil Card** | Iridescent rainbow shift on hover. | ⚠ restraint (decorative gimmick — rarely earns its place) |
| **Tinder Swipe Stack** | Physical card stack, swipe-away. | vocab-only (use only when the swipe *is* the product) |
| **Morphing Modal** | Button expands into its own dialog. | → [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) |

## Scroll animations

All entries here are **scroll-care**: gate on `prefers-reduced-motion`, never nest scrollbars (see the no-nested-scrollbars rule), never replace native scrolling outright.

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Sticky Scroll Stack** | Cards stick and physically stack. | → [TECH-motion-orchestration](TECH-motion-orchestration.md) |
| **Horizontal Scroll Hijack** | Vertical scroll drives a horizontal pan. | ⚠ restraint (hijacking scroll harms usability; needs a real reason) |
| **Locomotive / Sequence Scroll** | Image/3D sequence tied to the scrollbar. | ⚠ restraint (heavy; perf + a11y cost) |
| **Zoom Parallax** | Central background image zooms on scroll. | → [TECH-motion-taxonomy](TECH-motion-taxonomy.md) |
| **Scroll Progress Path** | SVG line drawing along scroll. | vocab-only |
| **Liquid Swipe Transition** | Page transition like viscous liquid. | ⚠ restraint |

## Galleries & media

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Dome Gallery** | 3D panoramic gallery. | vocab-only · ⚠ restraint (WebGL weight) |
| **Coverflow Carousel** | 3D carousel with angled edges. | vocab-only |
| **Drag-to-Pan Grid** | Boundless draggable canvas. | vocab-only |
| **Accordion Image Slider** | Narrow strips expanding on hover. | vocab-only |
| **Hover Image Trail** | Cursor leaves a popping image trail. | ⚠ restraint (custom-cursor decoration — banned by default in ai-slop-avoid Section X) |
| **Glitch Effect Image** | RGB-channel shift on hover. | ⚠ restraint (gimmick) |

## Typography & text

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Kinetic Marquee** | Endless text bands reversing on scroll. | → [TECH-signature-move](TECH-signature-move.md) · scroll-care |
| **Text-Mask Reveal** | Massive type as a transparent window to video/media. | vocab-only |
| **Text Scramble Effect** | Matrix-style decoding on load / hover. | ⚠ restraint (gimmick; never on body copy) |
| **Circular Text Path** | Text curving along a spinning circle. | → [`amw-pretext`](../../amw-pretext/SKILL.md) (text-on-path) |
| **Gradient Stroke Animation** | Outlined text with a running gradient. | ⚠ restraint |
| **Kinetic Typography Grid** | Letters dodging the cursor. | ⚠ restraint (custom-cursor-adjacent) |

## Micro-interactions & effects

| Pattern | One-line meaning | amw status |
|---|---|---|
| **Particle Explosion Button** | CTA shatters into particles on success. | ⚠ restraint (only on a genuine success moment, reduced-motion gated) |
| **Liquid Pull-to-Refresh** | Reload indicator like detaching droplets. | vocab-only · ⚠ restraint |
| **Skeleton Shimmer** | Shifting light across loading placeholders. | → [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) |
| **Directional Hover-Aware Button** | Fill enters from the cursor's exact side. | → [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) |
| **Ripple Click Effect** | Wave from the click coordinates. | → [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) |
| **Animated SVG Line Drawing** | Vectors drawing themselves in real time. | → [TECH-motion-taxonomy](TECH-motion-taxonomy.md) |
| **Mesh Gradient Background** | Organic lava-lamp blobs. | ⚠ restraint (generic mesh/aurora gradients are an AI-slop tell — see ai-slop-avoid) |
| **Lens-Blur Depth** | Background UI blurred to focus the foreground action. | → [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) |

## Animation stack — our override

> Taste-skill's §10 recommends Motion (`motion/react`), GSAP + ScrollTrigger, and Three.js. **This plugin does NOT adopt that recommendation.** Whenever a pattern above needs motion, build it with the plugin's stack, in this order:

1. **`starter-components/animations.html`** — the ~50-LOC timeline core covers sequence/stagger/reveal patterns.
2. **Native scroll-driven animations / CSS** (`@scroll-timeline`, `animation-timeline`, `:has()`, `view-transition`) for scroll-tied effects.
3. **Popmotion 11.0.5** — ONLY for physics / spring / drag / inertia that CSS cannot express (pinned CDN, reduced-motion gate at every call site).

**No Framer Motion, no GSAP, no Three.js as defaults.** The full rule and the Popmotion CDN pin live in [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) ("popmotion-physics-spring") and [TECH-motion-orchestration](TECH-motion-orchestration.md). Every motion pattern also obeys [TECH-reduced-motion](TECH-reduced-motion.md) and the per-tier caps in [TECH-motion-density](TECH-motion-density.md) / [TECH-motion-budgets](TECH-motion-budgets.md).

## Cross-references

- [ai-slop-avoid](../ai-slop-avoid.md) — why the ⚠ restraint patterns are constrained (incl. Section X production-test tells).
- [TECH-microinteractions-catalog](TECH-microinteractions-catalog.md) — implementation hub for card / button / micro-interaction patterns + the animation-stack rule.
- [TECH-motion-orchestration](TECH-motion-orchestration.md), [TECH-motion-taxonomy](TECH-motion-taxonomy.md), [TECH-motion-density](TECH-motion-density.md) — motion families, budgets, caps.
- [TECH-signature-move](TECH-signature-move.md) — when ONE hero/typography pattern becomes the page's signature.
- [TECH-landing-anatomy](TECH-landing-anatomy.md) — where hero/layout patterns sit in the nine canonical sections.
- [TECH-dial-configuration](TECH-dial-configuration.md) — MOTION_DRAMA / VISUAL_COMPLEXITY gate which patterns are even on the table.
