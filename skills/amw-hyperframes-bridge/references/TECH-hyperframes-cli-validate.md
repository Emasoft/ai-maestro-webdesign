---
name: TECH-hyperframes-cli-validate
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/validate.ts
also-in: SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md
---

# TECH: `hyperframes validate` — WCAG contrast audit

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Output](#output)
  - [When warnings appear](#when-warnings-appear)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

> For visual layout overflow checks (text overflow, container clipping), see [TECH-hyperframes-cli-inspect](TECH-hyperframes-cli-inspect.md). `validate` is strictly a WCAG color-contrast pass.

## What it does

Runs a WCAG-contrast audit on the composition by default. Seeks to 5 timestamps across the composition duration, screenshots the page, samples background pixels behind every text element, and computes contrast ratios. Failures appear as warnings. The audit uses the actual rendered output — not CSS-declared colors — so gradient backgrounds and translucent surfaces are evaluated correctly.

## When to use

Before every render. After every edit that touches color, background, or type. `validate` is the second gate in the bridge's pre-render sequence (`lint → validate → inspect → render`); `inspect` runs after `validate` for layout-overflow checks (see [TECH-hyperframes-cli-inspect](TECH-hyperframes-cli-inspect.md)), then `render` produces the MP4.

## How it works

```bash
npx hyperframes validate                # full audit (default)
npx hyperframes validate --no-contrast  # skip contrast check (iterating rapidly)
```

### Output

```
⚠ WCAG AA contrast warnings (3):
  · .subtitle "secondary text" — 2.67:1 (need 4.5:1, t=5.3s)
  · .caption "timestamp"       — 3.10:1 (need 4.5:1, t=8.0s)
  · .kicker "announcement"     — 2.95:1 (need 3.0:1 large, t=10.2s)
```

Thresholds:

- Normal text (< 18 px, or 18 px without bold): 4.5:1
- Large text (≥ 18.66 px bold, or ≥ 24 px): 3.0:1

### When warnings appear

- **Dark backgrounds:** brighten the failing text color until clear 4.5:1 (normal) / 3.0:1 (large)
- **Light backgrounds:** darken the failing color
- Stay within the palette family — don't invent a new color, adjust the existing one
- Re-run `validate` until clean

## Minimal example

```bash
# Initial run
$ npx hyperframes validate
⚠ WCAG AA contrast warnings (1):
  · .subtitle "address verified" — 3.8:1 (need 4.5:1, t=2.1s)

# Fix: brighten --muted from #64748B to #94A3B8 on the dark bg
# Edit CSS, save

# Re-run
$ npx hyperframes validate
✓ All checks passed
```

*Attributed to the hyperframes skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes/SKILL.md`.*

## Gotchas

- `validate` samples actual pixel data at 5 hard-coded timestamps — if a text element sits on a gradient that shifts behind it over time, only those 5 frames are checked. The five sample timestamps are hard-coded; for finer-grained or different sample positions, use `inspect --at <timestamps>` (which supports explicit timestamp selection but only checks layout overflow, not contrast). There is no equivalent timestamp override for `validate`.
- `--no-contrast` skips the audit but also skips other visual checks. Use sparingly.
- Warnings for text that fades from opacity 0 → 1 are evaluated at the moment of the sample. If the sample hits a 0.3-opacity frame, the result is misleading. Adjust sample timestamps to the fully-entered frames.

## Cross-references

- [TECH-hyperframes-cli-lint](TECH-hyperframes-cli-lint.md), [TECH-hyperframes-cli-preview](TECH-hyperframes-cli-preview.md), [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md)
  > [TECH-hyperframes-cli-render.md] What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
  > What it does · When to use · How it works · Minimal example · CI integration · Gotchas · Cross-references
- [TECH-hyperframes-cli-inspect](TECH-hyperframes-cli-inspect.md) — next gate after `validate` in the pre-render sequence; catches layout overflow
  > What it does · When to use · How it works · Flags · Output (JSON mode) · Minimal example · Opt-out attributes · Gotchas · Cross-references
- [TECH-hyperframes-capture-step-7-validate](TECH-hyperframes-capture-step-7-validate.md) — use in the capture pipeline
  > What it does · When to use · How it works · Validate sequence · Gate · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
