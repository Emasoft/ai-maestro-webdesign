---
name: TECH-hyperframes-non-negotiables
category: hyperframes-composition
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [The twelve rules](#the-twelve-rules)
  - [Determinism clause](#determinism-clause)
  - [Animation scope clause](#animation-scope-clause)
  - [Animation conflict clause](#animation-conflict-clause)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Non-negotiable composition rules

## What it does

Consolidates the twelve hyperframes rules that, if violated, produce broken compositions. Some are caught by `hyperframes lint`; others manifest as silent failures at render time.

## When to use

As a pre-render review checklist. Before running `hyperframes render`, scan the composition against this list.

## How it works

### The twelve rules

1. **Forget `window.__timelines` registration** — timeline never plays, no error.
2. **Use video for audio** — always muted `<video>` + separate `<audio>`.
3. **Nest video inside a timed div** — use a non-timed wrapper.
4. **Use `data-layer`** (use `data-track-index`) **or `data-end`** (use `data-duration`).
5. **Animate video element dimensions** — GSAP-animating `width`, `height`, `top`, `left` directly on a `<video>` causes Chrome to stop rendering frames. Animate a wrapper `<div>` instead.
6. **Call play / pause / seek on media** — framework owns playback.
7. **Create a top-level container without `data-composition-id`.**
8. **Use `repeat: -1`** on any timeline or tween — always finite repeats.
9. **Build timelines asynchronously** (inside `async`, `setTimeout`, `Promise`).
10. **Use `gsap.set()` on clip elements from later scenes** — they don't exist in the DOM at page load. Use `tl.set(selector, vars, timePosition)` inside the timeline at or after the clip's `data-start` time instead.
11. **Use `<br>` in content text** — forced line breaks don't account for actual rendered font width. Text that wraps naturally + a `<br>` produces an extra unwanted break → overlap. Let text wrap via `max-width`. Exception: short display titles where each word is deliberately on its own line (e.g. "THE\nIMMORTAL\nGAME" at 130px).
12. **Let composition duration shorter than the video** — composition duration equals `tl.duration()`. If the last GSAP animation ends at 8 s but the video is 283 s, the video cuts off at 8 s. Extend the timeline: `tl.set({}, {}, 283)` adds a zero-duration placeholder at 283 s without affecting any elements. Run `npx hyperframes compositions` to check resolved durations.

### Determinism clause

- **No `Math.random()`**, `Date.now()`, or time-based logic. Use a seeded PRNG (mulberry32) for pseudo-random values.

### Animation scope clause

- GSAP only animates visual properties (`opacity`, `x`, `y`, `scale`, `rotation`, `color`, `backgroundColor`, `borderRadius`, transforms). Never `visibility` / `display`. Never `video.play()` / `audio.play()`.

### Animation conflict clause

- Never animate the same property on the same element from multiple timelines simultaneously.

## Minimal example

Pre-render checklist:

```
[ ] All timelines registered as window.__timelines["<id>"]
[ ] Muted + playsinline on every video
[ ] No <audio> sharing a timed div with other content
[ ] No data-layer / data-end attributes
[ ] No .width / .height tweens on video elements (animate wrapper div)
[ ] No play()/pause()/seek() calls
[ ] Every top-level container has data-composition-id
[ ] No repeat: -1 anywhere (use finite repeat count)
[ ] All timeline construction synchronous (no await inside)
[ ] Late-clip .set() uses tl.set(selector, vars, t), never gsap.set()
[ ] No <br> in content (except deliberate multi-line display titles)
[ ] No Math.random() / Date.now()
[ ] No opacity/y exits before transitions (except final scene)
[ ] class="clip" on every timed <img> and <div> (omit on <video> and <audio>)
[ ] Timeline duration covers full video length (tl.set({}, {}, totalSeconds) if needed)
```

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Rule 10 (later-clip `.set()`) is the subtlest failure — the line runs, no error, but the target doesn't exist. The clip appears with its default opacity/position instead of the intended pre-set state.
- Rule 11 (`<br>`) only matters when text naturally wraps. Short titles with intentional per-word line breaks are the exception, not the rule.
- Rule 2 (`<video>` for audio) is common because the first muted-video has sound bundled into the same MP4. Separate out the audio into its own file, or point a second `<audio>` element at the same MP4 — the framework handles both.
- Forgetting rule 8 (`repeat: -1`) at the end of a long render job is the worst outcome — the lint errors catch it but the author ignored them.
- Rule 12 (timeline too short) is the most common complaint after first-time renders — "my video is only 8 seconds instead of 5 minutes". The linter does not catch this. Run `npx hyperframes compositions` to see resolved durations.

## Cross-references

- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md), [TECH-hyperframes-timeline-contract](TECH-hyperframes-timeline-contract.md), [TECH-hyperframes-data-attributes](TECH-hyperframes-data-attributes.md), [TECH-hyperframes-scene-transitions](TECH-hyperframes-scene-transitions.md)
- [TECH-hyperframes-cli-lint](TECH-hyperframes-cli-lint.md) — the linter that catches most of these
- `../SKILL.md`
