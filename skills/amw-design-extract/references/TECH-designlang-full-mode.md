---
name: TECH-designlang-full-mode
category: designlang-url-extract
source: SKILLS-TO-INTEGRATE/web-design/designlang-design-extract/SKILL.md
also-in:
---

# TECH: `--full` — everything-at-once extraction

## What it does

Enables all four optional capture modes in one run: dark mode, responsive breakpoints, interaction states, and component screenshots. Equivalent to combining `--dark --responsive --interactions --screenshots` on the command line.

## When to use

- Reference-site reverse engineering where the downstream workflow is unknown and you want every signal captured on first pass.
- Building a competitor-analysis corpus where partial extractions would require re-runs.
- One-shot "I want everything designlang can give me" requests from the user.

Skip `--full` when the user has a narrow need (tokens only, or just dark mode) — running all modes triples extraction time and produces files that won't be read.

## How it works

`--full` toggles the four optional pipelines inside designlang in sequence:

1. Default extraction at 1280×800.
2. Re-renders in dark mode if the page exposes a dark theme (via `prefers-color-scheme: dark` media query or a class/`data-theme` toggle).
3. Re-runs at 4 responsive breakpoints (mobile, tablet, desktop, wide).
4. Probes every interactive element for hover/focus/active state deltas.
5. Captures component screenshots (buttons, cards, nav, hero).

All eight token files are emitted once; the optional modes add supplementary files and sections to the Markdown report rather than replacing the base output.

## Minimal example

```bash
npx designlang https://stripe.com --full
```

*Attributed to designlang — `designlang-design-extract/SKILL.md`.*

## Gotchas

- Runtime is roughly 3-5x a plain extraction because breakpoint re-renders and per-element interaction probes are sequential.
- Sites that detect headless browsers and serve different markup (hCaptcha, bot walls) can produce empty dark-mode or responsive sections. Fall back to single-mode runs with a longer `--wait` window.
- The component-screenshot step hits the filesystem hard. Point `--out` at a tmpfs/`$TMPDIR` mount for large corpora to avoid blowing the project directory.

## Cross-references

- `TECH-designlang-basic-extraction.md` — non-`--full` default
- `TECH-designlang-dark-mode.md`, `TECH-designlang-responsive.md`, `TECH-designlang-interactions.md`, `TECH-designlang-screenshots.md` — the four modes `--full` enables
- `../SKILL.md`
