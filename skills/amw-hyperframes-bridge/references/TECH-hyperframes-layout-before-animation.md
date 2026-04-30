---
name: TECH-hyperframes-layout-before-animation
category: hyperframes-composition
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---

# TECH: Layout Before Animation

## What it does

A core hyperframes authoring principle: position every element where it should be at its **most visible moment** — the "hero frame", the frame where it's fully entered, correctly placed, and not yet exiting. Write this as static HTML + CSS **first**. No GSAP yet. Then animate *from* offscreen/invisible *to* that CSS position.

## When to use

On every composition, always. This principle is the difference between "I'll see if this looks right when I render" and "the layout is correct by construction before motion is added".

## How it works

Four steps:

1. **Identify the hero frame** for each scene — the moment when the most elements are simultaneously visible. This is the layout you build.
2. **Write static CSS** for that frame. The `.scene-content` container MUST fill the full scene using `width: 100%; height: 100%; padding: Npx;` with `display: flex; flex-direction: column; gap: Npx; box-sizing: border-box`. Padding pushes content inward — NEVER `position: absolute; top: Npx` on a content container. Absolute-positioned content overflows when taller than the remaining space. Reserve `position: absolute` for decoratives only.
3. **Add entrances with `gsap.from()`** — animate FROM offscreen / invisible TO the CSS position. The CSS position is ground truth; the tween describes the journey to get there.
4. **Add exits with `gsap.to()`** — animate TO offscreen / invisible FROM the CSS position. (Exits apply ONLY on the final scene. Inter-scene transitions handle exits everywhere else.)

### Why this matters

If you position elements at their animated START state (offscreen, scaled to 0, opacity 0) and tween them to where you *think* they should land, you're guessing the final layout. Overlaps are invisible until the video renders. By building the end state first, layout problems are visible and fixable before motion is added.

## Minimal example

```css
/* scene-content fills the scene; padding positions content */
.scene-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 120px 160px;
  gap: 24px;
  box-sizing: border-box;
}
.title    { font-size: 120px; }
.subtitle { font-size: 42px; }
/* Container fills any scene size (1920x1080, 1080x1920, etc).
   Padding positions content. Flex + gap handles spacing. */
```

### Wrong pattern (hardcoded dimensions + absolute positioning)

```css
.scene-content {
  position: absolute;
  top: 200px;
  left: 160px;
  width: 1920px;
  height: 1080px;
  display: flex; /* ... */
}
```

```js
// Step 3: Animate INTO those positions
tl.from(".title",    { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, 0);
tl.from(".subtitle", { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.2);
tl.from(".logo",     { scale: 0.8, opacity: 0, duration: 0.4, ease: "power2.out" }, 0.3);

// Step 4: Animate OUT (final scene only; inter-scene transitions handle exits elsewhere)
tl.to(".title",    { y: -40, opacity: 0, duration: 0.4, ease: "power2.in" }, 3.0);
tl.to(".subtitle", { y: -30, opacity: 0, duration: 0.3, ease: "power2.in" }, 3.1);
```

### Layered + temporal intent

- **Intentional overlap** (glow behind text, background patterns, card stacks) — layered by design, acceptable.
- **Unintentional overlap** (two headlines land on top of each other due to a timing bug, content bleeds off-frame) — the layout step catches these.
- **Shared space across time** — if A exits before B enters in the same area, both have correct CSS positions for their hero frames; timeline ordering keeps them visually separated.

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Building layouts via `gsap.set()` at t=0 is NOT the same as static CSS. `gsap.set()` only fires when the timeline initializes; clips from later scenes may not be in the DOM yet.
- Absolute-positioned content containers with hardcoded dimensions break when the composition dimensions change (1920x1080 → 1080x1920 for portrait exports). Flex + padding are dimension-agnostic.
- "I'll animate from `opacity: 0` and figure out the end position with `gsap.to()`" inverts the principle. The end position is the CSS; the tween describes the journey.

## Cross-references

- `TECH-hyperframes-composition-core.md`
- `TECH-hyperframes-timeline-contract.md`
- `TECH-hyperframes-scene-transitions.md`
- `../SKILL.md`
