---
name: TECH-hyperframes-capture-step-4-storyboard
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Asset audit table](#asset-audit-table)
- [Gate](#gate)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Step 4 — Write STORYBOARD.md

## What it does

Writes the per-beat creative direction — the document the engineer follows to build each composition. STORYBOARD.md specifies mood, camera, animations, transitions, assets, depth layers, and sound effects for every beat. It is the **creative north star** of the whole pipeline.

## When to use

After DESIGN.md (visual identity) and SCRIPT.md (narration backbone) exist. Before Step 5 (VO generation) and Step 6 (compositions).

## How it works

For each beat in SCRIPT.md, write:

- **Mood** — one-line atmospheric direction (tense / triumphant / quiet / urgent)
- **Camera** — framing / zoom / pan / hold
- **Key elements** — specific assets shown (product screenshot, logo, headline, stat)
- **Animations** — entrance motion + exit motion + ambient motion
- **Transition** — how this beat hands off to the next (crossfade, wipe, shader transition, hard cut)
- **Depth layers** — foreground / midground / background, with parallax hints
- **Sound** — narration timing, SFX cues, music cue points

### Asset audit table

The storyboard ends with a table listing every asset referenced across all beats, its source (captured in Step 1 / needs new asset / TTS output), and its status (ready / missing / needs edit).

## Gate

`STORYBOARD.md` exists with beat-by-beat direction AND an asset audit table showing every asset is either ready or has a plan to get ready.

## Minimal example

```markdown
# Acme — STORYBOARD.md

## Beat 1 (hook, 0-2.5 s) — "Address verification, in under 120 milliseconds."

- **Mood:** precise, quiet confidence
- **Camera:** static centered frame, subtle grain
- **Key elements:** large headline "120 ms" + small subtitle "address verified"
- **Animations:**
  - "120" counts up from 000 (duration 1.2 s, power2.out)
  - "ms" slides in from right (0.4 s, power1.out)
  - Subtitle fades in at t=1.8 (0.5 s opacity 0→1)
- **Transition to Beat 2:** shader transition — slow wipe, 0.6 s
- **Depth:** single layer (foreground only)
- **Sound:** narration starts at t=0.3; subtle tick at each integer during count-up

## Beat 2 (problem, 2.5-7.5 s) — ...
## ...

## Asset Audit

| Asset                   | Source                      | Status    |
|-------------------------|-----------------------------|-----------|
| hero-dashboard.png      | Step 1 capture              | ready     |
| logo-mark.svg           | Step 1 capture              | ready     |
| integration-diagram.png | Step 1 capture              | ready     |
| grain-overlay.png       | hyperframes-registry "grain"| needs install |
| narration.wav           | Step 5 TTS                  | pending   |
```

*Attributed to the website-to-hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Skipping STORYBOARD.md and going straight to compositions produces improvised per-beat direction, which is where unintentional overlap and layout bugs originate.
- "Mood" is not fluff — it constrains the engineer's motion choices. "Tense" rules out friendly bounces.
- The asset audit table catches missing assets before the compositions are built. A beat that says "show hero-dashboard.png" without that file on disk fails at Step 6.
- Transitions between beats MUST be specified. Jump cuts are banned by the hyperframes core rules.

## Cross-references

- [TECH-hyperframes-capture-step-3-script](TECH-hyperframes-capture-step-3-script.md), [TECH-hyperframes-capture-step-5-vo](TECH-hyperframes-capture-step-5-vo.md), [TECH-hyperframes-capture-step-6-build](TECH-hyperframes-capture-step-6-build.md)
  > What it does · When to use · How it works · Narration style rules · Format · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md)
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
- [TECH-hyperframes-scene-transitions](TECH-hyperframes-scene-transitions.md)
  > What it does · When to use · How it works · Rule 1 — ALWAYS use transitions between scenes · Rule 2 — ALWAYS use entrance animations on every scene · Rule 3 — NEVER use exit animations except on the final scene · Rule 4 — Final scene only may fade elements out · Wrong pattern · Right pattern · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
