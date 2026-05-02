---
name: TECH-hyperframes-cli-lint
category: hyperframes-cli
source: external/hyperframes/packages/cli/src/commands/lint.ts
also-in:
---
## Table of Contents

- [What it does](#what-it-does)
- [When to use](#when-to-use)
- [How it works](#how-it-works)
- [Minimal example](#minimal-example)
  - [CI integration](#ci-integration)
- [Gotchas](#gotchas)
- [Cross-references](#cross-references)


# TECH: `hyperframes lint` — static validation

## What it does

Lints `index.html` and every file in `compositions/` against the hyperframes schema. Catches: missing `data-composition-id`, overlapping tracks, unregistered timelines, banned attributes (`data-layer`, `data-end`), invalid `data-composition-src` paths, and other structural errors.

## When to use

After every edit. First gate in the bridge's pre-render sequence (`lint → validate → inspect → render`). The linter is the cheapest, fastest gate — running it every few edits catches errors while they're still small. Upstream skills also reference `preview` as a developer-loop step; the bridge intentionally drops `preview` for unattended Phase B pipelines (see `../SKILL.md` gate-sequence note).

## How it works

```bash
npx hyperframes lint                # current directory
npx hyperframes lint ./my-project   # specific project
npx hyperframes lint --verbose      # info-level findings
npx hyperframes lint --json         # machine-readable
```

Output levels:

- **Errors** — must fix. The composition won't render correctly.
- **Warnings** — should fix. The composition may render but doesn't follow best practice.
- **Info** — `--verbose` only. Style hints, pattern suggestions.

The linter does NOT catch runtime issues (wrong ease, off-layout elements, slow animation) — those need `validate` (WCAG contrast + console errors during composition load) and `inspect` (visual layout overflow audit).

## Minimal example

```bash
# Clean composition
$ npx hyperframes lint
✓ Lint passed: 0 errors, 0 warnings

# Broken composition
$ npx hyperframes lint
✗ 2 errors, 1 warning:
  ERROR  index.html:47  data-composition-id missing on root element
  ERROR  compositions/hero.html:92  timeline for 'hero' not registered in window.__timelines
  WARN   compositions/hero.html:33  repeat: -1 detected on '.sweep' — use finite repeat count
```

### CI integration

```yaml
# .github/workflows/lint.yml
- name: Lint hyperframes compositions
  run: npx hyperframes lint --json > lint.json
  # Fails the job on any error
```

*Attributed to the hyperframes-cli skill — `SKILLS-TO-INTEGRATE/web-design/hyperframes/skills/hyperframes-cli/SKILL.md`.*

## Gotchas

- Passing lint is necessary but not sufficient. Layout overlaps and motion quality need preview.
- `--strict` on `render` fails on lint errors; `--strict-all` fails on errors + warnings. Useful for CI.
- Running lint from a parent directory lints all discovered hyperframes projects at once. Usually you want to `cd` into the project or pass an explicit path.

## Cross-references

- [TECH-hyperframes-cli-preview](TECH-hyperframes-cli-preview.md), [TECH-hyperframes-cli-render](TECH-hyperframes-cli-render.md), [TECH-hyperframes-cli-validate](TECH-hyperframes-cli-validate.md)
- [TECH-hyperframes-non-negotiables](TECH-hyperframes-non-negotiables.md) — rules the linter enforces
- `../SKILL.md`
