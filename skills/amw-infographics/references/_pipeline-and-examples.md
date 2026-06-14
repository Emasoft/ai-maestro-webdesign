---
name: _pipeline-and-examples
category: infographics-pipeline
source: skills/amw-infographics/SKILL.md
---
## Table of Contents

- [Prerequisites](#prerequisites)
- [Examples](#examples)
- [Output](#output)

## Prerequisites

- **runtime_binaries (system):** `python3 ≥ 3.8`.
- **runtime_binaries (installed via `/amw-init`):** Playwright + Chromium (`python3 -m playwright install chromium --with-deps`), optional Inkscape or pdf2svg for SVG export.
- **python_packages:** `playwright ≥ 1.40.0`.
- **npm_packages:** none required.
- **mcp_servers:** none.
- **CDN assets (run-time):** Google Fonts (Bebas Neue, Teko, Orbitron, Montserrat), Phosphor Icons, optional Chart.js. Offline environments need the CDN resolvable — `html-export.py` spins up a local HTTP server so Playwright resolves them cleanly.
- **Shared scripts:** `../../bin/amw-html-export.py` (PNG / PDF / SVG export), `../../bin/amw-preview-server.py` (Mode A live preview).

## Examples

`examples/` ships 15 rendered PNG reference outputs and `templates/` ships 24 fully-built reference HTML pieces with `{{PLACEHOLDER}}` variables.

**Token-economics example (One-Shot mode):** Input: a tokenomics brief with allocation %, vesting schedule, and brand color. Routing: `token-economics.html` template, [TECH-token-economics-playbook](TECH-token-economics-playbook.md), [TECH-stacked-reference-archetype](TECH-stacked-reference-archetype.md), [TECH-svg-pie-chart](TECH-svg-pie-chart.md), [TECH-progress-bar-vesting](TECH-progress-bar-vesting.md). Output: HTML + retina PNG + PDF at 1080×1440 with 11 content blocks.
> [TECH-progress-bar-vesting.md] What it does · When to use · HTML · CSS · The milestone marker trick · Labels row — above and below · Gradient fill · Gotchas · Cross-references
> [TECH-svg-pie-chart.md] What it does · The color rule · Primary shades (preferred) · Brand complementary (max 2-3 hues) · SVG arc math · Segment calculator · Template — 4 segments · Legend — side-by-side · Gotchas · Cross-references
> [TECH-stacked-reference-archetype.md] What it does · When to use · The shape · CSS implementation · The section-variety rule still applies · Gotchas · Cross-references
> [TECH-token-economics-playbook.md] What it does · When to use · Color system · Typography · Standard component prevalence (across 62 pieces) · Visual properties · Signature layout pattern (portrait-tall, 10+ content blocks) · CSS variables · Font pair · Reference template · Density rule · Gotchas · Cross-references

## Output

This skill produces TWO kinds of output:

1. **Artifact(s)** — HTML + retina PNG + print-ready PDF infographic posters. Output path determined by project inference per [project-output-routing](../../amw-design-principles/references/project-output-routing.md): user-supplied path → framework convention → existing `./design/<subtype>/` → generic fallback `./design/infographics/` → last-resort scratch `/tmp/amw-infographics-<slug>/`. Every artifact is listed with its path in the report.
> [project-output-routing.md] When to consult this doc · Detection order · Per-artifact-type default subpath · Reconciliation when multiple candidates match · Edge cases · Quick-reference algorithm (pseudo-code) · Cross-references

2. **Job-completion report** — markdown at `$MAIN_ROOT/reports/webdesigner/<YYYYMMDD_HHMMSS±HHMM>_<title-slug>_<8-char-hash>.md`. Contains: **Inputs** (user-provided + auto-detected), **Method** (TECH references consulted, pipeline steps), **Artifacts** (per-file bullet — `- <path> — <description> — How to use: <tip> — Next steps: <follow-up>`), **Checklist** (each item PASS/FAIL/N/A), **Deviations** (skipped or changed steps + rationale). The `<8-char-hash>` is the first 8 chars of SHA-256 of the inputs+artifacts list.

Resolve `$MAIN_ROOT` via `git worktree list | head -n1 | awk '{print $1}'`.

**Every artifact MUST be linked from the report.** If an artifact is produced but not listed, the run is incomplete. `reports/webdesigner/` is for user-facing job outputs (distinct from `reports/audit/` which is for build-time audit artifacts).
