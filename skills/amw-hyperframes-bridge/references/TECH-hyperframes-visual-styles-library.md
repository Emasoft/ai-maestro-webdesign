---
name: TECH-hyperframes-visual-styles-library
category: hyperframes-identity-gate
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Preset shape (each entry contains)](#preset-shape-each-entry-contains)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `visual-styles.md` — 8 named visual-style presets

## What it does

A curated library of 8 named visual styles that can be used as "quick-start" identities when the user names one (e.g. "make it Swiss Pulse") and no DESIGN.md exists. Each preset includes a hex palette, GSAP easing signatures, and shader pairings.

> **Naming trap:** `visual-styles.md` (plural, in the hyperframes skill directory) is the library. `visual-style.md` (singular, project-scoped) is the per-project style file. Different files.

## When to use

When the Visual Identity Gate finds no DESIGN.md, no visual-style.md, and the user has named a style by its library name. The gate reads this library, generates a minimal DESIGN.md from the matching preset, and proceeds.

## How it works

The 8 presets:

| Preset | Mood | Signature |
|---|---|---|
| **Swiss Pulse** | precise, rhythmic, modernist | Helvetica-adjacent sans, monochrome palette, snap entrances (ease: `power4.out`) |
| **Velvet Standard** | luxurious, cinematic, understated | Editorial serif + geometric sans, deep palette, slow fades (`power2.inOut`, 0.9 s) |
| **Deconstructed** | brutalist, raw, exposed | Mono stacks, unpolished typography, hard cuts + sudden reveals |
| **Maximalist Type** | loud, kinetic, display-first | Oversized display fonts, saturated palette, elastic + overshoot easings |
| **Data Drift** | technical, cool, data-first | Space Grotesk + JetBrains Mono, slate + cyan, gentle tabular-num counters |
| **Soft Signal** | calm, warm, reassuring | Fraunces / Nunito, cream + sage, long fades, minimal motion |
| **Folk Frequency** | organic, hand-made, tactile | Hand-drawn elements, earthy palette, organic easings (`power1.inOut`) |
| **Shadow Cut** | dark, sharp, confident | Deep-black surfaces, single bright accent, sharp ease-ins, clean hard cuts |

### Preset shape (each entry contains)

- **Style Prompt** — one paragraph describing the visual + motion language
- **Colors** — hex values with roles (primary, accent, surface, text, muted)
- **Typography** — 1-2 font families with weights
- **Motion / Easing** — default eases, typical durations, intensity
- **Transitions** — recommended inter-scene transitions
- **Shader pairings** — recommended shader transitions from `@hyperframes/shader-transitions`
- **What NOT to Do** — anti-patterns specific to the preset

## Minimal example

User: "Make it Swiss Pulse"

Gate flow:

```
Step 1: DESIGN.md exists? → no
Step 2: visual-style.md exists? → no
Step 3: User named a style — "Swiss Pulse" matches a preset in visual-styles.md
        → Read the preset's shape:

Style Prompt: Swiss typography, rhythmic beats, monochrome modernist restraint.
              Text snaps. Nothing bounces.
Colors: --primary #000; --accent #FF1744 (rare); --surface #F4F4F4; --text #000; --muted #888
Typography: Inter Tight 400/500/600, tight tracking
Motion: power4.out on entrances, power3.in on exits, 0.4-0.6 s durations
Transitions: hard cuts with typographic wipe
What NOT to Do: no bounce, no elastic, no gradients, no serifs, no warm palettes

Step 4: Generate DESIGN.md from preset, continue to compositions.
```

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- The preset list is NOT exhaustive — if the user names something not in the library ("cyberpunk", "retro 90s", "editorial minimal"), the gate falls back to asking the 3 questions (mood / light-or-dark / brand refs).
- Each preset is a STARTING POINT. User edits and brand tuning are expected. The preset exists to avoid "blank page" paralysis, not to be the final answer.
- Misspellings ("Swiss Pulz", "Velvet Std") shouldn't silently match — the gate should ask for clarification.

## Cross-references

- [TECH-hyperframes-identity-gate](TECH-hyperframes-identity-gate.md) — the gate that reads this library
  > What it does · When to use · How it works · DESIGN.md exists in the project? · visual-style.md exists? · User named a style (e.g. "Swiss Pulse", "dark and techy", "luxury brand")? · None of the above? · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-2-design](TECH-hyperframes-capture-step-2-design.md) — DESIGN.md creation
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
