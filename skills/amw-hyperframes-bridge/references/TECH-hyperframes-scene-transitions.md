---
name: TECH-hyperframes-scene-transitions
category: hyperframes-composition
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---

# TECH: Scene transitions (non-negotiable rules)

## What it does

Defines the four rules every multi-scene composition MUST follow. Breaking any one of them is a broken composition. The rules exist because scenes without transitions feel like jump cuts, and exit animations before transitions empty the scene before the transition can use it.

## When to use

On every multi-scene composition. Single-scene compositions use subset (rules 2 and 4 still apply; rules 1 and 3 are moot).

## How it works

### Rule 1 — ALWAYS use transitions between scenes

No jump cuts. No exceptions. Available transition types: crossfades, wipes, reveals, shader transitions. Transition documentation lives in `external/hyperframes/docs/catalog/blocks/` — files matching `transitions-*.mdx` (one file per transition type, ~13 total). Shader transitions require the `@hyperframes/shader-transitions` package.

### Rule 2 — ALWAYS use entrance animations on every scene

Every element animates IN via `gsap.from()`. No element may appear fully-formed at its scene's start. If a scene has 5 elements, it needs 5 entrance tweens.

### Rule 3 — NEVER use exit animations except on the final scene

This means: NO `gsap.to()` that animates opacity to 0, y offscreen, scale to 0, or any other "out" animation before a transition fires. **The transition IS the exit.** The outgoing scene's content MUST be fully visible at the moment the transition starts.

### Rule 4 — Final scene only may fade elements out

The last scene MAY fade elements out (e.g. fade to black). This is the ONLY scene where `gsap.to(..., { opacity: 0 })` is allowed on content.

### Wrong pattern

```js
// BANNED — exits the scene before the transition can use it
tl.to('#s1-title',    { opacity: 0, y: -40, duration: 0.4 }, 6.5);
tl.to('#s1-subtitle', { opacity: 0, duration: 0.3 },        6.7);
// → transition at t=7.0 fires on empty frame
```

### Right pattern

```js
// Scene 1 entrance animations only
tl.from('#s1-title',    { y: 50, opacity: 0, duration: 0.7, ease: "power3.out" }, 0.3);
tl.from('#s1-subtitle', { y: 30, opacity: 0, duration: 0.5, ease: "power2.out" }, 0.6);

// NO exit tweens — transition at 7.2s (below) handles the scene change
// Transition fires at 7.2s

// Scene 2 entrance animations
tl.from('#s2-heading', { x: -40, opacity: 0, duration: 0.6, ease: "expo.out" }, 8.0);
```

## Minimal example

Two-scene composition skeleton:

```html
<div data-composition-id="multi" data-width="1920" data-height="1080">
  <div id="scene-1" class="scene">
    <h1 id="s1-title">Scene One</h1>
    <p id="s1-sub">Supporting copy</p>
  </div>
  <div id="scene-2" class="scene">
    <h1 id="s2-title">Scene Two</h1>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    // Scene 1 entrances
    tl.from('#s1-title', { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, 0.3);
    tl.from('#s1-sub',   { y: 40, opacity: 0, duration: 0.5, ease: "power3.out" }, 0.6);
    // Transition at t=7 — shader wipe (pseudo-code)
    tl.call(() => hyperframesTransition.wipe(7.0, 0.6), null, 7.0);
    // Scene 2 entrances
    tl.from('#s2-title', { x: -40, opacity: 0, duration: 0.6, ease: "expo.out" }, 7.6);
    // (no exit tweens anywhere except the final scene's fade-out)
    window.__timelines['multi'] = tl;
  </script>
</div>
```

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- The most common violation: scene N has exit tweens "just to polish the fade-out" at the end of its timeline window. The transition animation then fires on an already-faded scene. Delete the exit tweens.
- Transitions that are too fast (< 300 ms) feel like jump cuts again. Minimum 400 ms for crossfades; 600-900 ms for wipes / reveals.
- Shader transitions require `@hyperframes/shader-transitions` — a separate package in the external repo. Read its source for the API; the skill doesn't vendor it.
- Single-scene compositions are exempt from Rule 1 but must still follow Rule 2 (entrance animations).

## Cross-references

- `TECH-hyperframes-composition-core.md`, `TECH-hyperframes-timeline-contract.md`
- `TECH-hyperframes-non-negotiables.md`
- `../SKILL.md`
