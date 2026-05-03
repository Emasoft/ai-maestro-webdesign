---
name: TECH-hyperframes-capture-overview
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Video type reference](#video-type-reference)
  - [Format presets](#format-presets)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Website-to-Hyperframes capture — pipeline overview

## What it does

The 7-step pipeline that turns a URL into a professional video via Hyperframes. Each step produces an artifact that gates the next — skipping or weakening any step cascades into quality problems downstream. This TECH is the index; the seven step-specific TECH files document each step in detail.

## When to use

Whenever the user provides a website URL and asks for a video — product launch, social ad, feature announcement, brand reel, launch teaser. If the user pastes a URL and asks for "any kind of video content", this is the entry point.

## How it works

Seven steps, each with a gate:

| Step | Produces | Gate |
|---|---|---|
| 1. Capture & Understand | Site summary (name, colors, fonts, assets, vibe) | Summary printed |
| 2. Write DESIGN.md | Brand reference (6 sections, ~90 lines) | File exists |
| 3. Write SCRIPT | Narration script | `SCRIPT.md` exists |
| 4. Write STORYBOARD | Per-beat creative direction | `STORYBOARD.md` exists + asset audit table |
| 5. Generate VO + timing | Narration audio + word-level timestamps | `narration.wav` + `transcript.json` |
| 6. Build Compositions | Self-reviewed hyperframes HTML | Every composition self-reviewed |
| 7. Validate & Deliver | Lint + validate + preview + HANDOFF.md | `lint` + `validate` pass |

### Video type reference

| Type | Duration | Beats | Narration |
|---|---|---|---|
| Social ad (IG/TikTok) | 10-15 s | 3-4 | Optional hook sentence |
| Product demo | 30-60 s | 5-8 | Full narration |
| Feature announcement | 15-30 s | 3-5 | Full narration |
| Brand reel | 20-45 s | 4-6 | Optional, music focus |
| Launch teaser | 10-20 s | 2-4 | Minimal, high energy |

### Format presets

- Landscape — 1920 × 1080 (default)
- Portrait — 1080 × 1920 (Instagram Stories, TikTok)
- Square — 1080 × 1080 (Instagram feed)

## Minimal example

User: "Capture `https://example.com` and make me a 25-second product launch video for Instagram Stories"

Pipeline:

1. Capture the target site: extract colors, fonts, hero copy, product screenshots
2. DESIGN.md: distilled brand reference (palette, type, tone, anti-patterns)
3. SCRIPT.md: 25-sec narration, 5 beats: hook → problem → solution → proof → CTA
4. STORYBOARD.md: per-beat storyboard with camera, motion, assets
5. VO: Kokoro-82M generates narration.wav, transcript mapped to beats, actual durations recorded
6. Compositions: build each scene as hyperframes HTML, self-review each
7. Validate: `hyperframes lint`, `hyperframes validate`, preview, HANDOFF.md

Output: `output.mp4`, 1080×1920, 25 sec.

*Attributed to the website-to-hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Skipping Step 2 (DESIGN.md) and jumping to compositions produces ai-slop colors and generic type — the whole point of capture is to preserve the source brand's visual identity.
- Skipping Step 4 (STORYBOARD) means the engineer improvises per-beat visual direction, which is exactly when composition overlap and layout bugs creep in.
- Step 5 (VO + timing) must precede Step 6 (Build) because beat durations in STORYBOARD.md need real timestamps, not guessed seconds.
- Step 7 is non-negotiable — `hyperframes lint` and `hyperframes validate` are ship gates. A video that hasn't passed both has not been delivered.

## Cross-references

- [TECH-hyperframes-capture-step-1-capture](TECH-hyperframes-capture-step-1-capture.md)
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-2-design](TECH-hyperframes-capture-step-2-design.md)
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-3-script](TECH-hyperframes-capture-step-3-script.md)
  > What it does · When to use · How it works · Narration style rules · Format · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-4-storyboard](TECH-hyperframes-capture-step-4-storyboard.md)
  > What it does · When to use · How it works · Asset audit table · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-5-vo](TECH-hyperframes-capture-step-5-vo.md)
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-6-build](TECH-hyperframes-capture-step-6-build.md)
  > What it does · When to use · How it works · Per-composition workflow · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-7-validate](TECH-hyperframes-capture-step-7-validate.md)
  > What it does · When to use · How it works · Validate sequence · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md)
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
- [SKILL](../SKILL.md)
