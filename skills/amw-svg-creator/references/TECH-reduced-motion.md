---
name: TECH-reduced-motion
category: svg-animation
source: image-generation/svg-creator/references/advanced-techniques.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [The minimum implementation](#the-minimum-implementation)
- [Why `0.01ms` instead of `0s`](#why-001ms-instead-of-0s)
- [SMIL equivalent](#smil-equivalent)
- [When it's OK to ignore](#when-its-ok-to-ignore)
- [When it's partially OK](#when-its-partially-ok)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# `prefers-reduced-motion` — mandatory accessibility override

## What it does

Users with vestibular disorders, photosensitive epilepsy, or just
motion sensitivity can set "reduce motion" in their OS. Animated
SVGs MUST respect this preference — ignoring it is an accessibility
violation.

## The minimum implementation

Include this in every animated SVG:

```xml
<!-- source: image-generation/svg-creator/references/advanced-techniques.md -->
<style>
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
</style>
```

This collapses all animations to 0.01ms — essentially instant.
Elements still end up in their post-animation state, but without
the motion.

## Why `0.01ms` instead of `0s`

Setting duration to `0s` can cause some browsers to skip the
animation entirely — elements end up stuck in their pre-animation
state. `0.01ms` runs the animation but is indistinguishable from
instant to the viewer.

## SMIL equivalent

For SMIL animations inside `<img src>` SVGs (where CSS doesn't
apply), no automatic `prefers-reduced-motion` support exists — you'd
need to ship two SVGs (animated and static) and detect the
preference in the host page.

In practice: for animated SVGs that will be `<img src>`-embedded,
prefer CSS animations inside inline SVG + the media query override.

## When it's OK to ignore

- **Never.** If an animation is essential to the diagram's meaning
  (e.g. an animated data visualization), offer a "pause" control
  or a static alternative.

## When it's partially OK

Subtle animations — fades, 1-2px shifts — can be kept at reduced
duration rather than removed entirely:

```css
@media (prefers-reduced-motion: reduce) {
  .essential-fade {
    animation-duration: 100ms !important;
  }
  .parallax, .twinkle, .rotate {
    animation: none !important;
  }
}
```

## Gotchas

- The `!important` is necessary — without it, more-specific
  animation rules override the media query.
- `*::before` and `*::after` capture pseudo-element animations —
  easy to forget.
- Test with the OS preference turned ON — browser devtools have an
  emulator but it's not always reliable.

## Cross-references

- [TECH-css-smil-animation](TECH-css-smil-animation.md) — the animations this governs.
- [TECH-atmospheric-effects](TECH-atmospheric-effects.md) — stars / rain that need this override.
- [TECH-character-incremental-construction](TECH-character-incremental-construction.md) — animated characters
  need it too.
- [`../SKILL.md`](../SKILL.md) — parent skill

