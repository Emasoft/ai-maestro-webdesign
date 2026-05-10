---
name: TECH-outer-canvas-border
category: infographic-template
source: image-generation/create-infographics/SKILL.md
also-in: image-generation/create-infographics/resources/style-details.md
---
## Table of Contents

- [What it does](#what-it-does)
- [Implementation 1 — body outline](#implementation-1-body-outline)
- [Implementation 2 — wrapping container border](#implementation-2-wrapping-container-border)
- [Implementation 3 — pseudo-element overlay](#implementation-3-pseudo-element-overlay)
- [When to use](#when-to-use)
- [When NOT to use](#when-not-to-use)
- [Color choice](#color-choice)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# Outer canvas border — thin accent-colored frame

## What it does

A thin 1-2px solid accent-colored border around the entire
infographic canvas. Common in game pieces. The frame asserts the
piece as a contained artifact, not a web page section.

## Implementation 1 — body outline

```css
/* source: image-generation/create-infographics/resources/style-details.md */
body {
  outline: 2px solid var(--primary);
  outline-offset: -2px;
}
```

`outline-offset: -2px` pulls the outline inside the element's
bounds — otherwise the outline sits outside and gets clipped at
the viewport edge.

## Implementation 2 — wrapping container border

```css
.canvas {
  border: 2px solid var(--primary);
  /* other styles */
}
```

Simpler, but requires wrapping all content in `<div class="canvas">`.

## Implementation 3 — pseudo-element overlay

```css
.canvas::before {
  content: '';
  position: fixed;
  inset: 0;
  border: 2px solid var(--primary);
  pointer-events: none;
  z-index: 999;
}
```

Useful when you want the border to persist above all content
(position: fixed) and not affect layout.

## When to use

- Game event guides, tournament posters, quest cheat sheets.
- Premium NFT showcases where the border acts as a frame.
- Anywhere the piece should feel like a printed artifact / poster.

## When NOT to use

- Standard tokenomics, whitepaper, or ecosystem pieces — the border
  feels like overkill.
- Light-mode aesthetic — accent borders on white feel decorative
  instead of frame-like.

## Color choice

- Use `var(--primary)` for brand identity.
- For game pieces, often gold `#F6A91A` or the game's title color.
- Keep opacity 1.0 — this is a frame, not a subtle element.

## Gotchas

- `outline` on `body` behaves differently than `border` — it
  doesn't affect box-model sizing but CAN be hidden by overflow.
- `outline-offset: -2px` is required when using `outline` — positive
  values push it outside the viewport.
- Double-bordering (body outline + canvas border) looks amateur.
  Pick one.

## Cross-references

- [TECH-game-overview-playbook](TECH-game-overview-playbook.md) — where this pattern is common.
  > What it does · When to use · Color system · Typography — two sub-variants · Standard game · Pixel / retro game · Standard component prevalence (across 25 pieces) · Visual properties · Signature layout pattern · Character card grid (signature pattern) · Light-mode sub-variant · CSS variables (standard) · CSS variables (pixel) · Reference template · Gotchas · Cross-references
- [TECH-cheat-sheet-archetype](TECH-cheat-sheet-archetype.md) — common archetype for game-event
  > What it does · When to use · The shape · CSS implementation · The mixed-layout rule · Flow connector between sections · Gotchas · Cross-references
  posters that use this frame.
- [TECH-bordered-section-component](TECH-bordered-section-component.md) — complementary interior
  > What it does · When to use · Left-accent variant (most common) · Full-border variant · Header styles · HTML · Minimum border opacity · Gotchas · Cross-references
  borders.
- [[SKILL](../SKILL.md)](../SKILL.md) — parent skill
