---
name: TECH-designlang-basic-extraction
category: designlang-url-extract
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: Basic URL extraction (`designlang <url>`)

## What it does

Runs `designlang` against a single URL with default options. Crawls the page with a headless browser (Playwright), extracts every computed style from the live DOM, and writes 8 token-output files in one pass: AI-optimized Markdown, a visual HTML preview, a Tailwind config, a React theme module, a shadcn/ui theme CSS, Figma Variables JSON, W3C Design Tokens, and CSS custom properties.

## When to use

The default entry point when the user names a single URL and wants tokens without further choices. Preferred over any flagged variant when the site renders fully server-side at desktop width and the user has no extra constraints (dark mode, responsive breakpoints, interactions).

## How it works

1. Playwright launches Chromium in headless mode, navigates to the URL, waits for network-idle.
2. `document.querySelectorAll('*')` plus `getComputedStyle` walk every element — colors, fonts, spacing, shadows, radii, z-indices, transitions.
3. Output is deduplicated, classified by usage context (button / card / nav), and emitted in eight formats so downstream tools (Tailwind, shadcn, Figma, React) get a drop-in file each.

Invocation inside the plugin:

```bash
bin/amw-designlang-wrapper.sh tokens https://stripe.com
# Writes to $TMPDIR/ai-maestro-webdesign-tokens/stripe-com/
```

## Minimal example

```bash
# Raw upstream form
npx designlang https://stripe.com

# Plugin-standard form (pinned output path)
bin/amw-designlang-wrapper.sh tokens https://stripe.com
```

Output directory contains: `stripe-com-design-language.md`, `stripe-com-preview.html`, `stripe-com-design-tokens.json`, `stripe-com-tailwind.config.js`, `stripe-com-variables.css`, `stripe-com-figma-variables.json`, `stripe-com-theme.js`, `stripe-com-shadcn-theme.css`.

*Attributed to designlang by ara.so — `designlang-design-extract/SKILL.md`.*

## Gotchas

- First invocation downloads `designlang` + a Playwright browser — 30-90 s one-off stall. Subsequent calls are cached.
- Utility-CSS sites (Tailwind marketing pages) can produce 500+ colors because every spacing/color utility is in the wild DOM. See TECH-designlang-score and TECH-designlang-flags if this happens — `--depth 0` or the `colors` wrapper subcommand keep it bounded.
- Never run the raw `npx designlang` form from inside the plugin — pin through `bin/amw-designlang-wrapper.sh` so downstream skills can locate the files.

## Cross-references

- `../SKILL.md` — design-extract entry point
- `../../../bin/amw-designlang-wrapper.sh` — wrapper that normalises the output path
- [TECH-designlang-full-mode](TECH-designlang-full-mode.md) — everything-at-once (`--full`) variant
- [TECH-designlang-dark-mode](TECH-designlang-dark-mode.md), [TECH-designlang-responsive](TECH-designlang-responsive.md), [TECH-designlang-interactions](TECH-designlang-interactions.md), [TECH-designlang-screenshots](TECH-designlang-screenshots.md) — individual capture flags
- [TECH-designlang-score](TECH-designlang-score.md), [TECH-designlang-diff](TECH-designlang-diff.md), [TECH-designlang-brands](TECH-designlang-brands.md) — evaluation subcommands
