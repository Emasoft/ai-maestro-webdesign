---
name: TECH-hyperframes-timeline-contract
category: hyperframes-composition
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---

# TECH: Timeline contract — GSAP integration

## What it does

Hyperframes uses GSAP for animation but imposes strict rules so the framework can deterministically seek, render, and capture. The contract documents what GSAP patterns are allowed, what must be registered, and what's banned.

## When to use

On every composition that has motion. The contract is enforced by `hyperframes lint` — violations fail the build.

## How it works

### Required pattern

- All timelines start `{ paused: true }` — the player controls playback
- Register every timeline: `window.__timelines["<composition-id>"] = tl`
- Framework auto-nests sub-timelines — do NOT manually add them to the parent
- Composition duration equals `tl.duration()` — NOT `data-duration`. If the composition contains a long video clip but the last GSAP animation ends early, the video is cut off. Extend the timeline explicitly:

```js
// Extend timeline to match video length (e.g. 283s)
tl.set({}, {}, 283);
```

`tl.set({}, {}, TIME)` adds a zero-duration tween at the specified time, extending the timeline without touching any elements.

### Banned patterns

| Banned | Why | Alternative |
|---|---|---|
| `Math.random()` | Non-deterministic — breaks seek + re-render | Seeded PRNG (e.g. mulberry32) |
| `Date.now()` / time-based logic | Same | Deterministic clock from timeline time |
| `repeat: -1` | Infinite loops break capture engine | Finite count: `Math.ceil(duration / cycleDuration) - 1` |
| Building timelines inside `async` / `setTimeout` / Promise | Capture reads `window.__timelines` synchronously after page load | Synchronous construction at script load |
| Animating `visibility` / `display` | These are not animatable reliably | Animate `opacity` |
| Calling `video.play()` / `audio.play()` | Framework owns playback | Let framework drive it |
| Animating video dimensions | Breaks video decoder | Animate a wrapper div |
| Animating the same property on the same element from multiple timelines | Conflict, undefined result | Single source per property |
| `gsap.set()` on clips from later scenes | Clip doesn't exist in DOM at page load | Use `tl.set(selector, vars, timePosition)` inside the timeline |

### Allowed GSAP properties

Animate only visual properties:

- `opacity`
- `x`, `y` (translate)
- `scale`, `rotation`
- `color`, `backgroundColor`
- `borderRadius`
- Transforms (translate / rotate / scale)

Do NOT animate layout properties (`width`, `height`, `top`, `left`, `padding`, `margin`).

## Minimal example

```html
<div data-composition-id="beat-1" data-width="1920" data-height="1080">
  <!-- content -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    // Required boilerplate
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });

    // Entrance (t=0.3, stagger via explicit offsets)
    tl.from('#title',    { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.3);
    tl.from('#subtitle', { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.6);
    tl.from('#logo',     { scale: 0.8, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.9);

    // Ambient motion (finite repeat)
    const sweepCycle = 2.0;
    const sweepRepeats = Math.ceil(4 / sweepCycle) - 1;
    tl.to('#sweep', { x: 100, duration: sweepCycle, ease: "sine.inOut", repeat: sweepRepeats, yoyo: true }, 0.3);

    // Register — MUST match data-composition-id
    window.__timelines['beat-1'] = tl;
  </script>
</div>
```

### Use `tl.set()` for later-scene clips

Late-DOM clips (from sub-compositions loaded mid-timeline) don't exist at page load. Use timeline-local `set()`:

```js
// Wrong — runs immediately, target doesn't exist yet
gsap.set('#clip-from-scene-3', { opacity: 0 });

// Correct — runs at timeline time 15 s
tl.set('#clip-from-scene-3', { opacity: 0 }, 15);
```

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Forgetting `window.__timelines[...] = tl` is the single most common composition bug — no animation plays, no error message.
- `repeat: -1` is tempting for "loop forever while the composition is on screen". Always calculate a finite repeat count based on the composition's `data-duration`.
- Async timeline construction (`await gsap.loadFont(...)` before `tl.from(...)`) defers registration past when the capture engine reads it — timeline is missing from the render.
- Animating `y` + `x` is fine. Animating `top` + `left` triggers layout recalc per frame and tanks performance.

## Cross-references

- `TECH-hyperframes-composition-core.md`, `TECH-hyperframes-layout-before-animation.md`, `TECH-hyperframes-data-attributes.md`
- `TECH-hyperframes-non-negotiables.md`
- `../SKILL.md`
