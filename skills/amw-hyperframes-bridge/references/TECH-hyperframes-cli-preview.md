---
name: TECH-hyperframes-cli-preview
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/preview.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

# TECH: `hyperframes preview` — live studio preview

## What it does

Serves the composition directory via a local dev server, opens the hyperframes studio in your default browser, and hot-reloads on file changes. The studio shows the composition timeline, scrubbable playback, per-track visibility toggles, and a live canvas.

## When to use

After every significant composition edit — especially new scenes, transitions, or asset swaps. Lint catches structural errors; preview catches layout, motion, and timing issues.

## How it works

```bash
npx hyperframes preview                  # serve current directory, port 3002
npx hyperframes preview --port 4567      # custom port
```

**Studio features**

- Timeline with per-clip blocks (click to jump)
- Playback controls (play / pause / scrub)
- Per-track mute / solo for audio, per-track hide / show for video + overlays
- Live canvas showing the current frame
- Hot reload on file save — no manual refresh

## Minimal example

```bash
# Start preview
npx hyperframes preview

# Studio opens at http://localhost:3002
# Edit compositions/hero.html, save → canvas re-renders instantly
```

Typical workflow:

1. `npx hyperframes preview` (opens studio, leave running)
2. Edit in your editor of choice
3. Save → watch canvas re-render
4. Repeat until the composition looks right
5. `npx hyperframes lint` to confirm structure
6. `npx hyperframes render` for final output

*Attributed to the hyperframes-cli skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md`.*

## Gotchas

- Preview opens in your **system browser** via the `open` package (`commands/preview.ts` lines 185, 282, 369, 388). The rendering path is NOT the same as `render` — `render` uses Puppeteer headless. Use `inspect` and `snapshot` for pre-render layout verification that matches the actual render path.
- Hot reload works for HTML / CSS / JS. Changing `hyperframes.json` or swapping large media files needs a manual reload.
- Multiple `preview` instances fight over the default port; always pass `--port` on the second one.

## Cross-references

- [TECH-hyperframes-cli-init](TECH-hyperframes-cli-init.md), [TECH-hyperframes-cli-lint](TECH-hyperframes-cli-lint.md), [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md), [TECH-hyperframes-cli-validate](TECH-hyperframes-cli-validate.md)
  > [TECH-hyperframes-cli-render.md] What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
  > [TECH-hyperframes-cli-validate.md] What it does · When to use · How it works · Output · When warnings appear · Minimal example · Gotchas · Cross-references
  > What it does · When to use · How it works · Registry templates (`--example`) · Side effects · Minimal example · Gotchas · Cross-references
- [SKILL](../SKILL.md)
