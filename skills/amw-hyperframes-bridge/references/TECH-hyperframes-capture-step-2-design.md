---
name: TECH-hyperframes-capture-step-2-design
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in: SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md
---

# TECH: Step 2 — Write DESIGN.md

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Gate](#gate)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

Distills the captured site data into a brand reference every downstream composition reads before writing HTML. DESIGN.md is a cheat sheet, NOT a creative plan — the creative plan is Step 4 (STORYBOARD). DESIGN.md answers "what does this brand look and sound like", not "what should the video show".

## When to use

Immediately after Step 1 produces SITE.md. Creating DESIGN.md is non-negotiable — every hyperframes composition enforces the Visual Identity Gate: no HTML is written without a DESIGN.md (or equivalent visual-style.md or explicit user style direction).

## How it works

Six sections, ~90 lines total:

1. **Style Prompt** — one paragraph describing the overall look, feel, mood. Read by Step 4 (storyboard) when choosing camera/motion.
2. **Colors** — 3-5 hex values with roles (primary / accent / surface / text / muted). Pulled from Step 1's palette.
3. **Typography** — 1-2 families with weights. Heading + body.
4. **Motion / Easing** — default ease curves, typical durations, intensity (subtle / cinematic / kinetic).
5. **Visual Language** — signature effects (grain, glow, masking, shader transitions), imagery bias (photography / illustration / abstract), layout bias (grid / free / centered).
6. **What NOT to Do** — 3-5 anti-patterns specific to this brand (e.g. "no pure #FFFFFF surfaces", "no stock photos", "no rainbow gradients").

## Gate

`DESIGN.md` exists in the project directory. Every subsequent composition reads it before writing HTML.

## Minimal example

```markdown
# Acme DESIGN.md

## Style Prompt
Technical, confident, quietly proud. Precise geometry, cool slate backgrounds,
cyan accents. Motion is restrained — no bouncy springs. Think "aerospace
control panel", not "startup landing page".

## Colors
- --primary: #0F172A    (near-black, surfaces + headings)
- --accent: #38BDF8     (cyan, CTAs + highlights only)
- --surface: #F8FAFC    (off-white backgrounds)
- --text: #0F172A
- --muted: #64748B      (slate, secondary text)

## Typography
- Heading: Space Grotesk 600, tight tracking
- Body: Inter Tight 400/500

## Motion / Easing
- default ease: power2.out (entrance), power1.in (exit)
- default durations: entrance 0.6s, exit 0.4s
- intensity: subtle — no bounce, no elastic, no overshoot

## Visual Language
- grain overlay on backgrounds (subtle, 6% opacity)
- geometric shapes over photography
- product screenshots > illustrations > stock photos

## What NOT to Do
- No pure #FFFFFF surfaces (use --surface)
- No bright/saturated CTAs (cyan only)
- No bounce or elastic eases
- No rainbow or multi-color gradients
- No emoji in copy
```

*Attributed to the website-to-hyperframes + hyperframes skills — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Writing DESIGN.md after the compositions instead of before means every composition guessed at colors and motion. They'll all need rework.
- Generic "modern, clean, minimal" DESIGN.md is useless. Every field must be specific to this brand.
- The "What NOT to Do" section is the most load-bearing — it stops downstream compositions from drifting toward generic defaults.
- DESIGN.md is NOT the creative plan. If you find yourself writing "show product screenshot, zoom in, text enters from left" — that's STORYBOARD.md (Step 4), not here.

## Cross-references

- [TECH-hyperframes-capture-step-1-capture](TECH-hyperframes-capture-step-1-capture.md), [TECH-hyperframes-capture-step-3-script](TECH-hyperframes-capture-step-3-script.md)
  > [TECH-hyperframes-capture-step-3-script.md] What it does · When to use · How it works · Narration style rules · Format · Gate · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-identity-gate](TECH-hyperframes-identity-gate.md) — hard-gate rule this step satisfies
  > What it does · When to use · How it works · DESIGN.md exists in the project? · visual-style.md exists? · User named a style (e.g. "Swiss Pulse", "dark and techy", "luxury brand")? · None of the above? · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-visual-styles-library](TECH-hyperframes-visual-styles-library.md) — 8 named presets you can inherit from
  > What it does · When to use · How it works · Preset shape (each entry contains) · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
