---
name: TECH-error-handling
category: svg-creator
---

# TECH-error-handling — Symptom → cause → fix table

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [Symptom table](#symptom-table)
- [Cross-references](#cross-references)

## What it does

Lists every known failure mode of the SVG render-verify-deliver loop with
its likely cause and a single canonical fix. The fixes are NOT improvisations
— they are the only correct response for each row.

## When to use

The moment the renderer produces unexpected output or `finish` refuses to
deliver. Match the symptom to a row below and apply the canonical fix.

## Symptom table

| Symptom | Likely cause | Fix |
|---|---|---|
| User asked for a mascot / character / avatar | Scope violation | Refuse, cite `ai-slop-avoid.md` item 3, offer placeholder box + ask for real asset. |
| `finish` refuses to deliver | `render` was never called | Run `../../bin/amw-svg-render.py render <file>` first, view the PNG, then `finish`. |
| Gradient bands visible | 2-stop gradient on a large fill | Rewrite as 4–8 stops with small hue shifts; confirm `color-interpolation="linearRGB"`. |
| Drop-shadow edges look dirty | Missing `color-interpolation-filters="linearRGB"` on `<filter>` | Add the attribute to the `<filter>` element. |
| Animation clips / transforms off-centre | Missing `transform-box: fill-box; transform-origin: center;` | Set both CSS properties on the animated element. |
| Reduced-motion users see flashing | Missing `prefers-reduced-motion` guard | Wrap CSS `@keyframes` in `@media (prefers-reduced-motion: no-preference)` or disable SMIL via `begin="indefinite"`. |
| SVG fails to parse | Unclosed tag, stray `&`, missing `xmlns` | Close all tags, escape `&` → `&amp;`, ensure `xmlns="http://www.w3.org/2000/svg"` on the root. |
| Logo illegible at 64 px | Detail density too high for small size | Simplify to 2–3 primitives; test at target size in the render-verify loop. |
| `cairosvg` import failure on first render | Fresh environment, first call | Re-run the command; `bin/amw-svg-render.py` auto-installs `cairosvg` on first use, but a second invocation may be needed on slow networks. |

## Cross-references

- [TECH-render-verify-loop](./TECH-render-verify-loop.md) — the loop these errors apply to.
- [TECH-reduced-motion](./TECH-reduced-motion.md) — the `prefers-reduced-motion` guard.
- [SKILL](../SKILL.md) — parent skill.
