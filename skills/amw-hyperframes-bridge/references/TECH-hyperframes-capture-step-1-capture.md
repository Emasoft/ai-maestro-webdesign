---
name: TECH-hyperframes-capture-step-1-capture
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Gate](#gate)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Step 1 — Capture & Understand

## What it does

Runs the capture tooling against the target URL, extracts structured data (colors, typography, copy, assets, DOM structure), and produces a human-readable site summary the downstream pipeline treats as the source of truth.

## When to use

As the first step of every website-to-hyperframes run. Skip only if the user provides all of: DESIGN.md, product screenshots, and brand reference — in which case jump to Step 2 reading from provided files.

## How it works

- **Extract site data** via headless-browser capture (designlang is the recommended primitive — the hyperframes repo ships its own capture adapter but the output format is compatible).
- **Read the extracted data** — do not try to remember the whole site; use the write-down-and-forget method: summarize into SITE.md as you read, then reference SITE.md going forward.
- **Build the working summary** with five elements:
  - Site name + one-sentence positioning
  - Top 3-5 brand colors (hex, with role hints)
  - Font families (heading + body)
  - Key visual assets (hero images, product screenshots, logos)
  - One-sentence vibe — how the brand feels (cinematic / technical / warm / playful)

## Gate

Print the summary to chat. The pipeline does not advance until the user confirms the summary captures the brand correctly.

## Minimal example

```
## SITE.md — acme.com

**Name:** Acme — the verified-address API
**Positioning:** "Verified US postal addresses in under 120 ms for logistics teams"

**Palette:**
- #0F172A (near-black, primary)
- #38BDF8 (cyan, accent / CTA)
- #F8FAFC (off-white, surface)
- #64748B (slate, secondary text)

**Typography:**
- Heading: `Space Grotesk` (600 weight)
- Body: `Inter Tight` (400/500)

**Assets:**
- hero-dashboard.png (product screenshot)
- logo-mark.svg
- integration-diagram.png

**Vibe:** technical, confident, quietly proud — no marketing fluff
```

*Attributed to the website-to-hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Sites behind auth or paywalls capture as blank. Request a public-equivalent URL or an authenticated session cookie.
- SPA-only sites (React, Vue, Svelte without SSR) capture empty DOM unless the capture tool waits for hydration. Pass `--wait 3000` or equivalent.
- "Vibe" is subjective but consequential — it's the one-sentence brief Step 4 (storyboard) relies on. Don't skip it.
- Capturing too many assets (50+ images) wastes Step 4's audit time. Cap at 10-15 hero-quality assets.

## Cross-references

- [TECH-hyperframes-capture-step-2-design](TECH-hyperframes-capture-step-2-design.md)
- `../../amw-design-extract/SKILL.md` — the designlang primitive used for capture
- [TECH-hyperframes-capture-overview](TECH-hyperframes-capture-overview.md)
- `../SKILL.md`
