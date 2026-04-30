---
name: TECH-hyperframes-capture-step-7-validate
category: hyperframes-capture-step
source: external/hyperframes/skills/website-to-hyperframes/SKILL.md
also-in:
---

# TECH: Step 7 — Validate & Deliver

> **Bridge note (v0.4.30+).** The bridge's pre-render gate sequence is `lint → validate → inspect → render` (see `../SKILL.md` and `TECH-hyperframes-cli-inspect.md`). This step file describes the upstream `website-to-hyperframes` pipeline, which predates the `inspect` command. For automated Phase B pipelines, insert `npx hyperframes inspect --json > inspect.json` between steps 2 (validate) and 3 (preview / render). `inspect` is the dedicated visual-layout-overflow audit; `validate` checks WCAG contrast + console errors during composition load only.

## What it does

The final ship gate. Runs `hyperframes lint` (structural checks), `hyperframes validate` (WCAG contrast audit), and (per the bridge note above) `hyperframes inspect` (visual layout overflow audit), previews the output in the studio, and creates a HANDOFF.md for multi-session continuity.

## When to use

After Step 6 builds every composition. No composition ships without passing both `lint` and `validate` with zero errors.

## How it works

### Validate sequence

1. **Lint** — `npx hyperframes lint`. Checks: missing `data-composition-id`, overlapping tracks, unregistered timelines, banned attributes (`data-layer`, `data-end`), banned timeline patterns (`repeat: -1`, async construction).
2. **Validate** — `npx hyperframes validate`. Runs a WCAG contrast audit: seeks to 5 timestamps across the composition duration, screenshots the page, samples background pixels behind every text element, computes contrast ratios. Warnings for anything below 4.5:1 (normal text) or 3:1 (large text ≥ 24 px or ≥ 19 px bold).
3. **Preview** — `npx hyperframes preview`. Open the studio, play through the composition, watch for:
   - Overlaps not caught by lint (content bleeding off-frame)
   - Transition misfires (beat 2 content visible during beat 1 exit)
   - Audio / visual desync
4. **HANDOFF.md** — document state for the next session or stakeholder: project intent, video type, duration, outstanding TODOs, known issues, delivery targets.

### Gate

`npx hyperframes lint` and `npx hyperframes validate` both pass with zero errors. Any warnings from `validate` are addressed or documented with rationale in HANDOFF.md.

## Minimal example

```bash
# From the composition project directory
npx hyperframes lint
# → "Lint passed: 0 errors, 0 warnings"

npx hyperframes validate
# → Sample output:
# ✓ All compositions parse
# ⚠ WCAG AA contrast warnings (1):
#   · .hero-subtitle "address verified" — 3.8:1 (need 4.5:1, t=2.1 s)

# Fix: brighten #64748B to #94A3B8 on dark bg → passes 4.7:1
# Re-run
npx hyperframes validate
# → ✓ All checks passed

# Preview to catch anything lint/validate missed
npx hyperframes preview
```

Sample HANDOFF.md:

```markdown
# Acme Launch Teaser — HANDOFF.md

## Intent
25-second Instagram Stories launch teaser for Acme's verified-address API.

## Video type / format
Launch teaser · 1080 × 1920 · 25 s

## State
- All 5 beats built, lint clean, validate clean
- Narration: af_nova voice, 25.1 s total
- Output: ./out/acme-launch.mp4

## Known issues
- None

## Next session
- If the client wants a landscape 1920x1080 version, re-export with --width 1920 --height 1080
- Compositions are parametric — swap narration.wav + transcript.json to re-use layout
```

*Attributed to the website-to-hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/website-to-hyperframes/SKILL.md`.*

## Gotchas

- Skipping `hyperframes validate` because "the contrast looked fine in preview" is how contrast bugs ship. The validator samples actual pixel data behind text, not CSS-declared colors.
- HANDOFF.md is often skipped. It's the only artifact a second developer or a future-you can use to resume work without re-reading every other file.
- Preview can miss audio-visual desync if you scrub instead of letting the timeline play through. Always play at 1x.
- Warnings from validate are not errors, but each one is a deliberate decision. Address or document.

## Cross-references

- `TECH-hyperframes-capture-step-6-build.md`
- `TECH-hyperframes-cli-lint.md`, `TECH-hyperframes-cli-render.md`
- `../SKILL.md`
