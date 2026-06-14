---
name: TECH-svg-animation-patterns
category: svg-animation
source: skills/amw-diagram-svg/SKILL.md
also-in:
---
## Table of Contents

- [When to animate](#when-to-animate)
- [Primitive 1 — data-flow pulse on a connector](#primitive-1--data-flow-pulse-on-a-connector)
- [Primitive 2 — blinking / pulsing active node](#primitive-2--blinking--pulsing-active-node)
- [Accessibility — prefers-reduced-motion guard](#accessibility--prefers-reduced-motion-guard)
- [Cross-references](#cross-references)

# TECH-svg-animation-patterns

The two canonical SMIL animation primitives this skill emits, plus the
mandatory reduced-motion guard. For the deeper SMIL catalogue (a third
pulse-ring pattern, the full attribute breakdown, deprecation notes) see
[TECH-svg-animate-motion](TECH-svg-animate-motion.md).

## When to animate

If the brief explicitly mentions movement, flow, or "show data moving", add
subtle SMIL animations to connection lines or active nodes. Every animation
MUST specify both `dur` (e.g. `1s`, `2s`, `3s`) and
`repeatCount="indefinite"`. Keep it low-key — the diagram must still read as
a static image when the animation freezes.

Keep animations to one or two focal elements. Animating every edge at once
turns the diagram into noise and is the fast-track to an AI-slop pattern.

## Primitive 1 — data-flow pulse on a connector

A small dot follows a `<path>` from source to target, repeating. Use
`<animateMotion>` attached to a `<circle>`, with `<mpath href="#…">` pointing
at the line path:

```xml
<path id="flow-a-b" d="M 200 500 L 400 500" stroke="#0f172a"
      stroke-width="4" fill="none" marker-end="url(#arrow)"/>
<circle r="6" fill="#38bdf8">
  <animateMotion dur="2s" repeatCount="indefinite">
    <mpath href="#flow-a-b"/>
  </animateMotion>
</circle>
```

## Primitive 2 — blinking / pulsing active node

An `<animate>` on `opacity` or `r` drives a gentle pulse on a focal component
(e.g. the node being described "right now"):

```xml
<circle cx="500" cy="500" r="40" fill="#38bdf8">
  <animate attributeName="opacity" values="1;0.4;1"
           dur="1.5s" repeatCount="indefinite"/>
</circle>
```

## Accessibility — prefers-reduced-motion guard

Any diagram with animation MUST include a CSS rule that pauses the animation
when the user has enabled reduced motion. Embed inside a single `<style>`
element inside the SVG:

```xml
<style>
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
    animate, animateMotion, animateTransform { display: none; }
  }
</style>
```

## Cross-references

- [SKILL](../SKILL.md) — the orchestration layer that routes here
- [TECH-svg-animate-motion](TECH-svg-animate-motion.md) — full SMIL catalogue (third pulse-ring pattern, attribute breakdown, deprecation notes)
  > What it does · When to use · How it works · Mandatory attributes · Minimal example · Gotchas · Cross-references
- [TECH-arrow-marker-def](TECH-arrow-marker-def.md) — arrow markers that pair with animated connectors
  > What it does · When to use · How it works · Minimal example · Gotchas · Cross-references
