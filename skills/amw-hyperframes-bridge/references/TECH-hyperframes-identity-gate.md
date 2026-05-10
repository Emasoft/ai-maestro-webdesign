---
name: TECH-hyperframes-identity-gate
category: hyperframes-identity-gate
source: external/hyperframes/skills/hyperframes/SKILL.md
also-in: SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md
---

# TECH: Visual Identity Gate (HARD-GATE)

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [1. DESIGN.md exists in the project?](#1-designmd-exists-in-the-project)
  - [2. visual-style.md exists?](#2-visual-stylemd-exists)
  - [3. User named a style (e.g. "Swiss Pulse", "dark and techy", "luxury brand")?](#3-user-named-a-style-eg-swiss-pulse-dark-and-techy-luxury-brand)
  - [4. None of the above?](#4-none-of-the-above)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

## What it does

A hard gate applied before **any** composition HTML is written. The gate ensures every composition traces its palette, typography, and motion back to an explicit source — DESIGN.md, visual-style.md, a named preset, or direct user input. Compositions with generic defaults (`#333`, `#3b82f6`, `Roboto`) are evidence the gate was skipped.

## When to use

Before every composition, without exception. The gate runs before Step 6 (Build) of the website-to-hyperframes pipeline, and before any one-off composition authoring outside that pipeline.

## How it works

Check in this order:

### 1. DESIGN.md exists in the project?
Read it. Use its exact colors, fonts, motion rules, and "What NOT to Do" constraints. This is the primary path.

### 2. visual-style.md exists?
Read it. Apply its `style_prompt_full` and structured fields.

> **Naming trap:** `visual-style.md` is the project-specific file. `visual-styles.md` (plural) is the style library with 8 named presets. Different files.

### 3. User named a style (e.g. "Swiss Pulse", "dark and techy", "luxury brand")?
Read `visual-styles.md` for the 8 named presets. Generate a minimal DESIGN.md with:
- `## Style Prompt` (one paragraph)
- `## Colors` (3-5 hex values with roles)
- `## Typography` (1-2 font families)
- `## What NOT to Do` (3-5 anti-patterns)

### 4. None of the above?
Ask 3 questions before writing any HTML:
- What's the mood? (explosive / cinematic / fluid / technical / chaotic / warm)
- Light or dark canvas?
- Any specific brand colors, fonts, or visual references?

Then generate a minimal DESIGN.md from the answers.

## Minimal example

User prompt: "Make a dark techy launch video for Acme"

Gate sequence:

```
1. DESIGN.md exists? → no (just-created project)
2. visual-style.md exists? → no
3. User named a style — "dark and techy" is a recognized style pattern
   → Read visual-styles.md, find "Shadow Cut" or "Data Drift" as candidates
   → Generate minimal DESIGN.md:

# Acme — DESIGN.md

## Style Prompt
Dark, technical, restrained. Cool slate bg, single cyan accent. Sharp geometry. No bounce.

## Colors
- --primary: #0F172A
- --accent: #38BDF8
- --surface: #0F172A
- --text: #F8FAFC
- --muted: #64748B

## Typography
- Heading: Space Grotesk 600
- Body: Inter Tight 400/500

## What NOT to Do
- No bouncy/elastic easings
- No pure white surfaces
- No rainbow gradients
- No emoji in copy

4. Write compositions using these tokens.
```

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- Writing compositions with "I'll pick colors as I go" is the gate's failure mode. Always generate DESIGN.md first even if minimal.
- The difference between `visual-style.md` (project) and `visual-styles.md` (library) trips every new Claude instance at least once.
- "Modern", "clean", "minimal" are not styles. They are adjectives. Push users to more specific language ("Swiss", "editorial", "brutalist") or ask concrete questions.

## Cross-references

- [TECH-hyperframes-composition-core](TECH-hyperframes-composition-core.md)
  > What it does · When to use · How it works · Approach (narrative order) · Single-file skeleton · Visual Identity Gate (MUST — before writing HTML) · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-2-design](TECH-hyperframes-capture-step-2-design.md) — writing DESIGN.md in the capture pipeline
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-visual-styles-library](TECH-hyperframes-visual-styles-library.md) — 8 named presets
  > What it does · When to use · How it works · Preset shape (each entry contains) · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
