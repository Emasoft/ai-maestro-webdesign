---
name: TECH-hyperframes-capture-step-3-script
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Narration style rules](#narration-style-rules)
  - [Format](#format)
- [Gate](#gate)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Step 3 — Write SCRIPT.md

## What it does

Writes the narration script — the story backbone the video hangs on. Scene durations come from the narration (Step 5 generates audio and measures it), not from guesswork at the storyboard stage.

## When to use

After DESIGN.md (Step 2) establishes brand voice. The script inherits that voice — if the brand is "technical, quietly proud", the narration isn't "Hey y'all, check this out!".

## How it works

Scripts have three parts:

- **Hook** — the first 2-3 seconds; must stop the scroll
- **Body** — problem → solution → proof, or a variant
- **CTA** — what the viewer does next

### Narration style rules

- Written for **spoken delivery**, not reading. Contractions, shorter sentences, natural cadence.
- **Scene durations emerge from the script**, not from a pre-decided "25 seconds divided into 5 beats of 5 seconds each". Natural speech + pauses = natural durations.
- **Voice matches DESIGN.md vibe** — technical brands don't use enthusiastic-startup-narrator voice, luxury brands don't use casual-vlog voice.

### Format

One beat per paragraph. Beats are numbered. Each beat has the narration text + optional cue markers (for Step 5 to align with visuals).

## Gate

`SCRIPT.md` exists. Read aloud — does it sound natural? Does it match the DESIGN.md voice? If either answer is no, rewrite.

## Minimal example

```markdown
# Acme — SCRIPT.md

## Beat 1 (hook)
"Address verification, in under 120 milliseconds."

## Beat 2 (problem)
"Bad addresses cost logistics teams real money — returned shipments, failed deliveries, wrong zones."

## Beat 3 (solution)
"Acme's API catches them before they hit your database. USPS DPV-confirmed. ZIP+4 verified. Rate-limit-aware."

## Beat 4 (proof)
"Powering 80,000 verifications a day for our own customers. Built for teams shipping 10K+ packages."

## Beat 5 (CTA)
"Full docs at acme.com slash docs."
```

Word count: ~80 words. At Kokoro 160 wpm default → ~30 seconds. Matches the requested 25-30s launch teaser.

*Attributed to the website-to-hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Writing a script in "read-on-screen" style produces robotic narration. Always read aloud during drafting.
- Attempting to fit exactly N seconds by counting words ignores natural pauses. Generate the audio (Step 5) before committing to per-beat visuals (Step 4).
- Every beat needs a narrative reason to exist. A beat that says "and we also have this" without purpose dilutes the entire video.
- Save the hook until last — once the body is written, the hook will be more specific.

## Cross-references

- [TECH-hyperframes-capture-step-2-design](TECH-hyperframes-capture-step-2-design.md), [TECH-hyperframes-capture-step-4-storyboard](TECH-hyperframes-capture-step-4-storyboard.md), [TECH-hyperframes-capture-step-5-vo](TECH-hyperframes-capture-step-5-vo.md)
  > What it does · When to use · How it works · Gate · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
