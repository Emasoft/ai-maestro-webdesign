---
name: TECH-hyperframes-cli-inspect
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/layout.ts
also-in: external/hyperframes/packages/cli/src/commands/inspect.ts
---

# TECH: `hyperframes inspect` — visual layout audit

## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
  - [Flags](#flags)
  - [Output (JSON mode)](#output-json-mode)
- [Minimal example](#minimal-example)
- [Opt-out attributes](#opt-out-attributes)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)

> For WCAG contrast checks, see [TECH-hyperframes-cli-validate](TECH-hyperframes-cli-validate.md). `inspect` is a separate command focused on visual layout overflow, not color contrast.
> [TECH-hyperframes-cli-validate.md] What it does · When to use · How it works · Output · When warnings appear · Minimal example · Gotchas · Cross-references

## What it does

Runs a visual layout audit on the rendered composition by opening it in headless Chromium, seeking across the timeline, and reporting any text or container overflow. Each affected element is reported with its CSS selector, bounding box, pixel overflow amount, severity, and an agent-readable fix hint. The command is also available as `hyperframes layout` (compatibility alias).

## When to use

After `lint` and `validate` pass, and **before** `render`. `inspect` is the third gate in the pre-render sequence (`lint → validate → inspect → render`). Compositions that pass `lint` and `validate` can still ship visually broken output — text that overflows its container, a heading that clips at the edge of the canvas — and only `inspect` catches this before a potentially multi-minute render.

Run `inspect` after every edit that touches:
- Font size, line-height, letter-spacing, or font family
- Container dimensions (`width`, `height`, `max-width`, `overflow`)
- Text content length changes (especially VO-driven copy changes)
- Viewport or stage canvas dimensions

## How it works

```bash
# Default: 9 timeline samples, human-readable output
npx hyperframes inspect

# Agent-readable JSON (recommended for scripted gate checks)
npx hyperframes inspect --json

# Specific project directory
npx hyperframes inspect ./my-video

# Explicit hero-frame timestamps instead of auto-sampling
npx hyperframes inspect --at 1.5,4.0,7.25

# Fail on warnings as well as errors
npx hyperframes inspect --strict

# Compatibility alias (identical behavior)
npx hyperframes layout --json
```

### Flags

| Flag | Type | Default | Description |
|---|---|---|---|
| `dir` | positional | `.` (current dir) | Project directory to inspect |
| `--json` | boolean | false | Output agent-readable JSON (includes `schemaVersion`, `ok`, `issues[]`, `duration`, `samples`, `summary`) |
| `--samples N` | string | `"9"` | Number of midpoint samples to seek across the composition duration |
| `--at t1,t2,...` | string | — | Comma-separated explicit timestamps in seconds (e.g. `--at 1.5,4.0,7.25`). Overrides `--samples` when set. |
| `--tolerance N` | string | `"2"` | Allowed pixel overflow before an element is reported as an issue (default: 2 px) |
| `--timeout N` | string | `"5000"` | Milliseconds to wait for the runtime to initialize (default: 5000 ms) |
| `--collapse-static` | boolean | true | Collapse repeated static issues that appear identically across multiple samples (reduces noise) |
| `--max-issues N` | string | `"80"` | Maximum number of issues to include in output after static collapse |
| `--strict` | boolean | false | Exit non-zero on warnings as well as errors |

### Output (JSON mode)

When `--json` is passed, the output is a single JSON document. Relevant fields:

```json
{
  "schemaVersion": "1",
  "ok": true,
  "duration": 30.0,
  "samples": [0.5, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 27.0, 29.5],
  "tolerance": 2,
  "strict": false,
  "collapseStatic": true,
  "errorCount": 0,
  "warningCount": 0,
  "totalIssueCount": 0,
  "truncated": false,
  "issues": []
}
```

If issues exist, each entry in `issues[]` contains a CSS selector, bounding box, pixel overflow, severity, and fix hint.

`ok: true` means exit code 0 (no errors, or no errors/warnings if `--strict`). `ok: false` means exit code 1.

## Minimal example

```bash
# Pre-render gate (abort if inspect fails)
cd /path/to/my-project
npx hyperframes lint              || exit 1
npx hyperframes validate          || exit 1   # exits 1 on console errors during composition load; contrast warnings still surface
npx hyperframes inspect --json > inspect.json || true
node -e "
  const r = JSON.parse(require('fs').readFileSync('inspect.json','utf8'));
  if (!r.ok) { console.error('inspect failed:', r.errorCount, 'errors'); process.exit(1); }
"
npx hyperframes render --output out/final.mp4
```

Human-readable output when issues are found:
```
◆  Inspecting layout for my-video (9 timeline samples)

  ✗  .hero-title — overflows container by 14px (t=2.0s, t=6.0s)
     Fix: reduce font-size or increase container max-width

  ⚠  .subtitle — overflows container by 3px (t=4.0s)
     Fix: add overflow: hidden or reduce letter-spacing
```

## Opt-out attributes

When overflow on a specific element is intentional (e.g. a deliberately bleeding edge element, or an animated clip that exits the canvas), suppress the issue by adding HTML attributes directly:

| Attribute | Scope | Description |
|---|---|---|
| `data-layout-allow-overflow` | On the overflowing element | Suppresses all overflow reports for this element across all timeline samples. Use sparingly — it hides real bugs if applied broadly. |
| `data-layout-ignore` | On the overflowing element | Excludes the element from layout inspection entirely (neither overflow nor bounds are checked). |

Example:
```html
<!-- Intentional bleed — exit animation crosses the canvas edge -->
<div class="clip hero-graphic" data-layout-allow-overflow ...>...</div>
```

## Gotchas

- `inspect` requires headless Chrome (same as `render`). Hyperframes uses Puppeteer + `@puppeteer/browsers` (NOT Playwright) to manage its Chrome binary. If Chrome is not provisioned, it fails with a Puppeteer error — run `(cd external/hyperframes && npx hyperframes browser ensure)` to download Chrome Headless Shell.
- `--at` overrides `--samples`. Use `--at` for compositions where specific frames are critical (intro/outro beats, VO-cued text reveals).
- `--collapse-static` (default: true) deduplicates issues that appear at every sample. Turn it off with `--collapse-static false` only when debugging a flicker that appears at exactly one timestamp.
- `--tolerance 2` (default) means elements that overflow by 1–2 px (typical sub-pixel rounding) are not reported. Tighten to `--tolerance 0` for pixel-perfect audits.
- Exit code 1 on errors (always), and also on warnings when `--strict` is used. In CI, use `--strict` to treat any overflow as a gate failure.
- `inspect` does not check color contrast — that is `validate`. Run both.

## Cross-references

- [TECH-hyperframes-cli-validate](TECH-hyperframes-cli-validate.md) — WCAG contrast audit (runs before `inspect` in the gate sequence)
  > What it does · When to use · How it works · Output · When warnings appear · Minimal example · Gotchas · Cross-references
- [TECH-hyperframes-cli-lint](TECH-hyperframes-cli-lint.md) — static schema validation (runs first in the gate sequence)
  > What it does · When to use · How it works · Minimal example · CI integration · Gotchas · Cross-references
- [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md) — final step; only reached after `inspect` passes
  > What it does · When to use · How it works · Flags · Quality guidance · Transparent video · Minimal example · Workers tuning · Gotchas · Cross-references
- [SKILL](../SKILL.md) — bridge invocation pattern and full gate sequence
- [amw-video-producer-agent](../../../agents/amw-video-producer-agent.md) §6.7 — inspect as the mandatory pre-render gate in the video producer agent
