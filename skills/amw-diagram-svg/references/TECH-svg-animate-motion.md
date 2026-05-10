---
name: TECH-svg-animate-motion
category: svg-arrow-marker
source: SKILLS-TO-INTEGRATE/diagrams-skills/baybee-diagram/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Animate a dot along a path (data-in-transit pattern)](#animate-a-dot-along-a-path-data-in-transit-pattern)
  - [Blink a node (alert pattern)](#blink-a-node-alert-pattern)
  - [Pulse a ring (activation pattern)](#pulse-a-ring-activation-pattern)
- [Mandatory attributes](#mandatory-attributes)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH-svg-animate-motion

## What it does

Animates elements along paths or as blinking / pulsing nodes using SMIL
`<animateMotion>` and `<animate>` elements. Used subtly to suggest
flow — data packets moving along an edge, a heartbeat on a service
node, pulse markers on a queue.

## When to use

- **When the diagram is about flow** and the animation reinforces the
  point (data pipeline, message passing, request-response cadence).
- **Live embeds** (documentation sites, product marketing pages) where
  the animation plays naturally.
- **Never** in static exports (PNG, PDF, print) — the animation is lost;
  keep the diagram readable without it.

Do not use animation for decoration alone. If the reader wouldn't miss
the animation, remove it.

## How it works

### Animate a dot along a path (data-in-transit pattern)

```xml
<defs>
  <path id="flow-path" d="M 100 500 L 900 500"/>
</defs>

<!-- Dot travels along the path -->
<circle r="10" fill="#38bdf8">
  <animateMotion dur="2s" repeatCount="indefinite">
    <mpath href="#flow-path"/>
  </animateMotion>
</circle>
```

### Blink a node (alert pattern)

```xml
<circle cx="500" cy="500" r="60" fill="#38bdf8">
  <animate attributeName="opacity"
           values="1;0.3;1" dur="1.5s"
           repeatCount="indefinite"/>
</circle>
```

### Pulse a ring (activation pattern)

```xml
<circle cx="500" cy="500" r="40" fill="none"
        stroke="#38bdf8" stroke-width="4">
  <animate attributeName="r" values="40;70;40"
           dur="2s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;0;1"
           dur="2s" repeatCount="indefinite"/>
</circle>
```

## Mandatory attributes

Every animation element must set:

- `dur` — duration (e.g. `"2s"` or `"1.5s"`). Without it, the animation
  doesn't play.
- `repeatCount="indefinite"` — or a specific count like `"3"`.
  Omitting it plays the animation once and freezes; usually not what
  you want.

## Minimal example

Data pipeline with a packet animation:

```xml
<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10"
            refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#0f172a"/>
    </marker>
    <path id="pipe" d="M 250 500 L 750 500"/>
  </defs>

  <g id="nodes">
    <rect x="150" y="460" width="200" height="80" rx="20"
          fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
    <rect x="650" y="460" width="200" height="80" rx="20"
          fill="#f1f5f9" stroke="#0f172a" stroke-width="4"/>
  </g>

  <g id="connections">
    <line x1="350" y1="500" x2="650" y2="500"
          stroke="#0f172a" stroke-width="4"
          marker-end="url(#arrow)"/>

    <!-- Animated packet dot -->
    <circle r="8" fill="#38bdf8">
      <animateMotion dur="2s" repeatCount="indefinite"
                     path="M 350 500 L 650 500"/>
    </circle>
  </g>

  <g id="labels">
    <text x="250" y="510" text-anchor="middle" font-size="22"
          fill="#0f172a">Producer</text>
    <text x="750" y="510" text-anchor="middle" font-size="22"
          fill="#0f172a">Consumer</text>
  </g>
</svg>
```

## Gotchas

- **SMIL is deprecated in Chrome but still works.** Chrome has threatened
  to remove SMIL for years; as of 2026 it still renders. For truly long-
  lived artifacts, consider CSS animations or Web Animations API
  instead. For blog posts and short-term marketing, SMIL is fine.
- **Keep animations slow.** Under 1s per cycle reads as flickering; 1.5-
  2.5s is the sweet spot for "motion without distraction".
- **Animate ≤3 elements per diagram.** More than 3 simultaneous motions
  become a visual seizure trigger.
- **Respect `prefers-reduced-motion`.** Wrap animations in a CSS media
  query that disables them:
  ```css
  @media (prefers-reduced-motion: reduce) {
    animateMotion, animate { display: none; }
  }
  ```
  Note: CSS can't control SMIL directly; use JavaScript to remove the
  elements when `matchMedia('(prefers-reduced-motion)').matches`.
- **No external resources.** SMIL animations must stay self-contained —
  no external path references, no loaded fonts mid-animation.

## Cross-references

- [SKILL](../SKILL.md) — Optional Animation section
- [TECH-arrow-marker-def](TECH-arrow-marker-def.md) — arrow markers that pair with animations
  > What it does · When to use · How it works · Attribute breakdown · Minimal example · Gotchas · Cross-references
- [TECH-svg-group-structure](TECH-svg-group-structure.md) — animations live inside the
  > What it does · When to use · How it works · Why this order · Minimal example · Gotchas · Cross-references
  `#connections` group usually
- [ai-slop-avoid](../../amw-design-principles/ai-slop-avoid.md) — don't overanimate; one
  > I. Visual style · II. Typography · III. Layout · IV. Content and copy · V. Interaction and motion · VI. Color · Self-check workflow · VII. Content density principle (positive stance)
  > I. Visual style · Purple-blue / pink-purple gradient backgrounds · Rounded card + 4 px colored left-accent · AI-drawn SVG illustrations / mascots / scenes · Emoji overuse · Unrestrained glassmorphism · Cool-but-meaningless 3D decor · II. Typography · Default-font trap · Weight soup · Excessive script / handwriting fonts · III. Layout · Hero → 3-column features → CTA → footer, universal template · Alternating white / pale-gray section backgrounds · One icon per feature · Trust-marker carpet · Every card the same size · IV. Content and copy · Placeholder names / testimonials / numbers · Invented statistics · Filler paragraphs · Meaningless subtitles · Exclamation / question-mark fever · V. Interaction and motion · First-viewport blanket fade-in + Y-translate · Everything `hover: scale(1.05) + shadow` · Parallax everywhere · VI. Color · Saturation at the ceiling · Infinitely expanding palette · …(+8)
  moving dot is plenty
