---
name: TECH-hyperframes-capture-step-6-build
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in: SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md
---

# TECH: Step 6 — Build Compositions

## What it does

Builds the actual HTML compositions, one per beat (or per scene grouping). Each composition reads DESIGN.md for identity, STORYBOARD.md for direction, transcript.json for timing. After each composition is written, run self-review for layout + asset placement + animation quality.

## When to use

After Steps 1-5 have produced DESIGN.md, SCRIPT.md, STORYBOARD.md, narration.wav, transcript.json. Never start here.

## How it works

### Per-composition workflow

1. **Read DESIGN.md** — colors, fonts, motion bias, anti-patterns
2. **Read the beat's STORYBOARD entry** — mood, camera, elements, animations, transition, depth, sound
3. **Read the beat's transcript slice** — actual start/end timestamps
4. **Write the composition HTML**:
   - Root `<div data-composition-id>` with `data-width`, `data-height` (duration is set by `tl.duration()` — NOT `data-duration`)
   - `.scene-content` container filling the scene (width/height 100%, padding + flex)
   - GSAP timeline registered via `window.__timelines["<id>"] = tl`
   - Layout built first (static CSS — the "Layout Before Animation" principle)
   - Entrance animations via `gsap.from()` to the CSS position
   - No exit animations except on the final scene — transitions handle exits
5. **Self-review** the composition:
   - Layout: no overlaps at the hero frame (the moment when the most elements are simultaneously visible)
   - Asset placement: every asset from STORYBOARD asset audit is present
   - Animation quality: entrance offset ≥ 0.1-0.3 s, at least 3 different eases, no repeat of the same entrance pattern
   - No `Math.random()` or `Date.now()` — compositions must be deterministic
   - No `repeat: -1` — infinite loops break the capture engine
   - No `<br>` for line wrapping — use `max-width` instead

### Gate

Every composition has been self-reviewed. No overlapping elements, no misplaced assets, no static images without motion. Each composition renders cleanly in `hyperframes preview`.

## Minimal example

Composition skeleton for Beat 1 (hook):

```html
<!DOCTYPE html>
<html>
<head><title>Beat 1</title></head>
<body>
<div data-composition-id="beat-1" data-width="1080" data-height="1920">
  <style>
    [data-composition-id="beat-1"] {
      width: 100%; height: 100%;
      background: #0F172A;
      color: #F8FAFC;
      font-family: 'Space Grotesk', sans-serif;
      font-feature-settings: 'tnum';
      display: flex; flex-direction: column;
      justify-content: center; align-items: center;
      padding: 120px 80px;
      box-sizing: border-box;
    }
    .hero-number { font-size: 360px; font-weight: 600; letter-spacing: -0.02em; color: #38BDF8; }
    .hero-unit   { font-size: 180px; font-weight: 600; margin-left: 0.3em; }
    .hero-subtitle { font-size: 42px; margin-top: 24px; color: #64748B; }
  </style>
  <div class="hero-row"><span class="hero-number" id="n">120</span><span class="hero-unit" id="u">ms</span></div>
  <div class="hero-subtitle" id="s">address verified</div>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    // Number count-up (integer) — deterministic
    const counter = { v: 0 };
    tl.to(counter, { v: 120, duration: 1.2, ease: "power2.out",
      onUpdate: () => document.getElementById('n').textContent = Math.round(counter.v) }, 0.0);
    tl.from('#u', { x: 80, opacity: 0, duration: 0.4, ease: "power1.out" }, 1.2);
    tl.from('#s', { opacity: 0, duration: 0.5, ease: "power2.out" }, 1.8);
    window.__timelines['beat-1'] = tl;
  </script>
</div>
</body>
</html>
```

*Attributed to the website-to-hyperframes + hyperframes skills — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`, `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Building compositions before self-reviewing DESIGN.md leads to colors drifting from brand. Read DESIGN.md FIRST every time.
- `scrollIntoView` is banned in compositions — corrupts the parent frame's scroll state in iframe hosts.
- Video elements must be `muted playsinline` — never rely on autoplay with sound in the composition.
- Never call `play()` / `pause()` / `seek()` on media — the framework owns playback.

## Cross-references

- `TECH-hyperframes-composition-core.md`, `TECH-hyperframes-layout-before-animation.md`, `TECH-hyperframes-data-attributes.md`, `TECH-hyperframes-timeline-contract.md`, `TECH-hyperframes-scene-transitions.md`, `TECH-hyperframes-non-negotiables.md`
- `TECH-hyperframes-capture-step-7-validate.md`
- `../SKILL.md`
